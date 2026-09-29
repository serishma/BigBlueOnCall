import subprocess


def get_proposed_fix(pod_name, status, description, events):

    if "ImagePullBackOff" not in status:
        return None

    if "nginx:doesnotexist" not in description:
        return None

    commands = [
        [
            "kubectl",
            "set",
            "image",
            "deployment/broken",
            "nginx=nginx:latest",
        ],
        [
            "kubectl",
            "patch",
            "deployment",
            "broken",
            "--type=json",
            "-p",
            '[{"op":"replace","path":"/spec/template/spec/containers/0/imagePullPolicy","value":"IfNotPresent"}]',
        ],
        [
            "kubectl",
            "rollout",
            "status",
            "deployment/broken",
            "--timeout=60s",
        ],
    ]

    return {
        "title": "Replace invalid container image",
        "reason": (
            "The deployment is configured with the invalid image "
            "nginx:doesnotexist. A known-good nginx image is available "
            "locally in the cluster."
        ),
        "commands": commands,
        "display": """kubectl set image deployment/broken nginx=nginx:latest

kubectl patch deployment broken --type=json -p '[{"op":"replace","path":"/spec/template/spec/containers/0/imagePullPolicy","value":"IfNotPresent"}]'

kubectl rollout status deployment/broken --timeout=60s""",
    }


def execute_fix(commands):

    results = []

    for command in commands:

        try:

            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=90,
            )

            results.append(
                {
                    "command": " ".join(command),
                    "returncode": result.returncode,
                    "stdout": result.stdout,
                    "stderr": result.stderr,
                }
            )

            if result.returncode != 0:
                break

        except Exception as e:

            results.append(
                {
                    "command": " ".join(command),
                    "returncode": -1,
                    "stdout": "",
                    "stderr": str(e),
                }
            )

            break

    return results
