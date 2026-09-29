def diagnose(status, description, events, logs):
    findings = []

    if "ImagePullBackOff" in status:
        findings.append("Pod is unable to start because the container image cannot be pulled.")

    if "doesnotexist" in description:
        findings.append("The configured image tag appears invalid: nginx:doesnotexist.")

    if "lookup registry-1.docker.io" in events:
        findings.append("Kubernetes node is also experiencing DNS resolution failures for Docker Hub.")

    if "Could not get logs" in logs:
        findings.append("Container logs are unavailable because the container never successfully started.")

    print("\n" + "=" * 60)
    print("BIGBLUEONCALL - DIAGNOSIS")
    print("=" * 60)

    for i, finding in enumerate(findings, 1):
        print(f"{i}. {finding}")

    print("\nRecommended investigation:")
    print("1. Verify the configured container image and tag.")
    print("2. Verify registry/DNS connectivity from the Kubernetes node.")
    print("3. Retry the deployment after correcting the image or registry issue.")


if __name__ == "__main__":
    print("Diagnosis module ready.")
