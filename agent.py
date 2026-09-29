import json
from google import genai

from tools import list_pods, describe_pod, get_events, get_logs

client = genai.Client()

TOOLS = {
    "list_pods": list_pods,
    "describe_pod": describe_pod,
    "get_events": get_events,
    "get_logs": get_logs,
}


def run_tool(action, arguments):
    if action not in TOOLS:
        return f"Unknown tool: {action}"

    try:
        return TOOLS[action](**arguments)
    except Exception as e:
        return f"Tool error: {e}"


def ask_gemini(prompt):
    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt,
        config={
            "tools": [],
            "automatic_function_calling": {
                "disable": True
            },
        },
    )
    return response.text


def investigate():
    evidence = ""

    prompt = """
You are BigBlueOnCall, an AI Kubernetes SRE incident investigator.

Investigate unhealthy Kubernetes workloads using these diagnostic tools:

- list_pods(namespace)
- describe_pod(pod_name, namespace)
- get_events(pod_name, namespace)
- get_logs(pod_name, namespace, previous)

You must choose ONE action at a time.

Return exactly:

ACTION: <tool name>
ARGS: <JSON arguments>

When enough evidence has been collected, return:

FINAL:
<root cause and recommended remediation>

Start by investigating unhealthy pods in the default namespace.
"""

    for step in range(6):
        response = ask_gemini(
            prompt + "\n\nCURRENT EVIDENCE:\n" + evidence
        )

        print("\n" + "=" * 60)
        print(f"AGENT STEP {step + 1}")
        print("=" * 60)
        print(response)

        if response.startswith("FINAL:"):
            break

        action = None
        arguments = {}

        for line in response.splitlines():
            if line.startswith("ACTION:"):
                action = line.split(":", 1)[1].strip()

            elif line.startswith("ARGS:"):
                try:
                    arguments = json.loads(
                        line.split(":", 1)[1].strip()
                    )
                except json.JSONDecodeError:
                    arguments = {}

        if not action:
            print("Could not understand agent action.")
            break

        print(f"\n🔧 Executing: {action}")
        print(f"Arguments: {arguments}")

        result = run_tool(action, arguments)

        print("\n📊 Kubernetes evidence:")
        print(result)

        evidence += (
            f"\n\nACTION: {action}\n"
            f"ARGUMENTS: {arguments}\n"
            f"RESULT:\n{result}\n"
        )


if __name__ == "__main__":
    print("=" * 60)
    print("       BIGBLUEONCALL AI AGENT")
    print("=" * 60)

    investigate()
