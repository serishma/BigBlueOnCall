from tools import list_pods, describe_pod, get_events, get_logs
from diagnosis import diagnose


def investigate(namespace="default"):
    print("=" * 60)
    print("BIGBLUEONCALL - INCIDENT INVESTIGATION")
    print("=" * 60)

    print("\n🔎 Checking pods...")
    pods = list_pods(namespace)
    print(pods)

    for line in pods.splitlines():
        parts = line.split(" | ")

        if len(parts) < 2:
            continue

        pod_name = parts[0]
        status = parts[1]

        if status in ["Running", "Succeeded"]:
            continue

        print("\n" + "=" * 60)
        print(f"🚨 UNHEALTHY POD: {pod_name}")
        print(f"STATUS: {status}")
        print("=" * 60)

        description = describe_pod(pod_name, namespace)
        events = get_events(pod_name, namespace)
        logs = get_logs(pod_name, namespace)

        print("\n📋 Pod description:")
        print(description)

        print("\n📅 Kubernetes events:")
        print(events)

        print("\n📜 Container logs:")
        print(logs)

        diagnose(
            status=status,
            description=description,
            events=events,
            logs=logs,
        )


if __name__ == "__main__":
    investigate()
