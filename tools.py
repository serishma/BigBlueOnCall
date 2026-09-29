from kubernetes import client, config

config.load_kube_config()
v1 = client.CoreV1Api()


def list_pods(namespace: str = "default") -> str:
    """List all pods in a namespace with their status and restart count."""
    lines = []
    for p in v1.list_namespaced_pod(namespace).items:
        status = p.status.phase
        restarts = 0
        if p.status.container_statuses:
            cs = p.status.container_statuses[0]
            restarts = cs.restart_count
            if cs.state.waiting:
                status = cs.state.waiting.reason
        lines.append(f"{p.metadata.name} | {status} | restarts={restarts}")
    return "\n".join(lines) or "No pods found"
def get_events(pod_name: str, namespace: str = "default") -> str:
    """Get Kubernetes events for a pod. Shows why it failed to start or pull."""
    events = v1.list_namespaced_event(
        namespace, field_selector=f"involvedObject.name={pod_name}"
    )
    lines = [f"{e.type} | {e.reason} | {e.message}" for e in events.items]
    return "\n".join(lines[-10:]) or "No events found"
def describe_pod(pod_name: str, namespace: str = "default") -> str:
    try:
        pod = v1.read_namespaced_pod(pod_name, namespace)

        result = [
            f"Pod: {pod.metadata.name}",
            f"Namespace: {pod.metadata.namespace}",
            f"Phase: {pod.status.phase}",
            f"Node: {pod.spec.node_name}",
        ]

        for container in pod.spec.containers:
            result.append(f"Container: {container.name}")
            result.append(f"Image: {container.image}")

        for container_status in pod.status.container_statuses or []:
            result.append(
                f"ContainerStatus: {container_status.name} "
                f"ready={container_status.ready} "
                f"restarts={container_status.restart_count}"
            )

            if container_status.state.waiting:
                result.append(
                    f"WaitingReason: {container_status.state.waiting.reason}"
                )
                result.append(
                    f"WaitingMessage: {container_status.state.waiting.message}"
                )

        return "\n".join(result)

    except client.exceptions.ApiException as e:
        return f"Could not describe pod: {e.reason}"


def get_logs(
    pod_name: str,
    namespace: str = "default",
    previous: bool = False
) -> str:
    try:
        logs = v1.read_namespaced_pod_log(
            pod_name,
            namespace,
            tail_lines=50,
            previous=previous
        )

        return logs or "No logs available"

    except client.exceptions.ApiException as e:
        return f"Could not get logs: {e.reason}"
