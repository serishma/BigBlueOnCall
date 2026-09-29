# 🚨 BigBlueOnCall

### Kubernetes Incident Investigation & SRE Assistant

BigBlueOnCall is a Kubernetes/SRE assistant designed to help engineers investigate Kubernetes incidents, understand the root cause, propose remediation, and safely execute approved fixes.

The project follows a **human-in-the-loop remediation model**, where remediation commands are displayed to the operator and require explicit approval before execution.

---

## 🎯 What is BigBlueOnCall?

During a Kubernetes incident, an SRE often needs to run multiple commands:

- Check unhealthy pods
- Inspect pod details
- Review Kubernetes events
- Check container logs
- Identify the root cause
- Decide on a remediation
- Execute the fix
- Verify that the workload recovered

BigBlueOnCall brings these steps into a single workflow.

---

## 🔄 How It Works

```text
┌─────────────────────┐
│   Kubernetes        │
│      Cluster        │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   Detect Incident   │
│                     │
│ Find unhealthy pods │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│    Investigation    │
│                     │
│ • Pod Details       │
│ • Events            │
│ • Container Logs    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│      Diagnosis      │
│                     │
│ • Evidence          │
│ • Root Cause        │
│ • Contributing      │
│   Factors           │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Remediation Proposal│
│                     │
│ Show exact commands │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ 👤 Human Approval   │
│                     │
│ Review & approve    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Execute Remediation │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│     Verification    │
│                     │
│ Pod → Running       │
└─────────────────────┘
<img width="1725" height="915" alt="Screenshot 2026-09-29 at 10 30 22 PM" src="https://github.com/user-attachments/assets/614f67a2-0e82-403f-bd23-32a3ffc559a3" />
<img width="1725" height="915" alt="Screenshot 2026-09-29 at 10 30 33 PM" src="https://github.com/user-attachments/assets/007e74b3-6ff6-490a-a55f-8e60f7e896ce" />
<img width="1725" height="915" alt="Screenshot 2026-09-29 at 10 30 46 PM" src="https://github.com/user-attachments/assets/fc97a4fe-4c5b-4221-be4b-173d00a17ffb" />
<img width="1725" height="915" alt="Screenshot 2026-09-29 at 10 30 58 PM" src="https://github.com/user-attachments/assets/1f1a78f5-5655-4417-af8d-b00065c136de" />
<img width="1725" height="915" alt="Screenshot 2026-09-29 at 10 31 10 PM" src="https://github.com/user-attachments/assets/c982a515-712c-456a-9054-7fd1040d6ff2" />
