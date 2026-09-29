from google import genai

client = genai.Client()


def generate_report(evidence):
    prompt = f"""
You are BigBlueOnCall, a Kubernetes SRE incident investigator.

Analyze ONLY the evidence below.

Produce:

## Incident
## Root Cause
## Evidence
## Contributing Factors
## Recommended Remediation
## Confidence

Rules:
- Do not invent facts.
- Separate confirmed evidence from possible contributing factors.
- If logs are unavailable, explain why.
- Keep the report concise and suitable for an SRE on-call engineer.

KUBERNETES EVIDENCE:
{evidence}
"""

    response = client.interactions.create(
        model="gemini-3.8-flash",
        input=prompt,
    )

    return response.output_text
