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
