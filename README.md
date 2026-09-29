# 🚨 BigBlueOnCall

### Kubernetes Incident Investigation & SRE Assistant

BigBlueOnCall is a Kubernetes/SRE assistant that helps engineers detect unhealthy workloads, investigate incidents, understand the likely cause, propose remediation, and safely execute approved fixes.

The project follows a **human-in-the-loop remediation model**: BigBlueOnCall shows the operator exactly what commands it plans to execute, and the operator must explicitly approve them before any remediation is performed.

---

## 🎯 What is BigBlueOnCall?

During a Kubernetes incident, an SRE typically needs to:

- Identify the unhealthy workload
- Inspect pod status
- Review Kubernetes events
- Check container logs
- Determine the likely root cause
- Decide on remediation
- Execute the remediation
- Verify that the workload has recovered

BigBlueOnCall brings these steps together into a single incident-response workflow.

---

## 🔄 How It Works

```text
                    ┌──────────────────────┐
                    │    Kubernetes        │
                    │       Cluster        │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Detect Incident    │
                    │                      │
                    │ Find unhealthy pods  │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │    Investigation     │
                    │                      │
                    │ • Pod Details        │
                    │ • Kubernetes Events  │
                    │ • Container Logs     │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │      Diagnosis       │
                    │                      │
                    │ • Evidence           │
                    │ • Root Cause         │
                    │ • Contributing       │
                    │   Factors            │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Remediation Proposal │
                    │                      │
                    │ Show exact commands  │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │  👤 Human Approval   │
                    │                      │
                    │ Review & approve     │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Execute Remediation  │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │     Verification     │
                    │                      │
                    │ Pod → Running        │
                    └──────────────────────┘
```

### Incident Response Flow

**Detect → Investigate → Diagnose → Propose → Approve → Execute → Verify**

---

## 🚨 Example Incident

For demonstration, BigBlueOnCall can investigate a Kubernetes deployment with an invalid container image.

```bash
kubectl set image deployment/broken nginx=nginx:doesnotexist
```

The affected pod enters:

```text
ImagePullBackOff
```

Example:

```text
NAME                       STATUS
broken-xxxxx               ImagePullBackOff
hello-xxxxx                Running
```

BigBlueOnCall detects the unhealthy workload during the cluster scan.

---

## 🔎 Incident Investigation

When an unhealthy pod is detected, BigBlueOnCall collects Kubernetes evidence.

### 📋 Pod Details

Example:

```text
Pod: broken-xxxxx
Namespace: default
Phase: Pending
Node: bigblueoncall-control-plane
Container: nginx
Image: nginx:doesnotexist
Ready: false
WaitingReason: ImagePullBackOff
```

### 📅 Kubernetes Events

BigBlueOnCall retrieves events associated with the failed pod.

Example:

```text
Normal   Scheduled
Normal   Pulling
Warning  Failed
Warning  ErrImagePull
Normal   BackOff
Warning  Failed
```

These events help identify why Kubernetes was unable to start the workload.

### 📜 Container Logs

BigBlueOnCall also attempts to retrieve container logs.

If the container never successfully starts, application logs may not be available.

Instead of treating this as a failed investigation, BigBlueOnCall explains:

> Application logs are unavailable because the container has not successfully started. Kubernetes Events contain the relevant failure information.

---

## 🧠 Diagnosis

BigBlueOnCall analyzes the collected evidence and identifies relevant findings.

For the example incident:

```text
The pod cannot start because Kubernetes
cannot pull the configured container image.

Configured image:

nginx:doesnotexist
```

The investigation can also identify additional evidence such as registry or DNS failures when they are present in Kubernetes events.

The system distinguishes between:

- Confirmed evidence
- Likely causes
- Contributing factors
- Missing information

---

## 🛠️ Proposed Remediation

After investigating the incident, BigBlueOnCall proposes a controlled remediation.

Example:

```bash
kubectl set image deployment/broken nginx=nginx:latest

kubectl patch deployment broken --type=json ...

kubectl rollout status deployment/broken --timeout=60s
```

The exact commands are displayed to the operator **before execution**.

---

## 👤 Human-in-the-Loop Approval

BigBlueOnCall does not automatically execute remediation.

The operator must explicitly approve the proposed commands.

```text
┌─────────────────────────────────────────────┐
│ 👤 Human Approval Required                  │
│                                             │
│ Review the proposed commands.               │
│                                             │
│ ☑ I have reviewed these commands and        │
│   approve the remediation.                  │
│                                             │
│       🚀 APPROVE & FIX INCIDENT             │
└─────────────────────────────────────────────┘
```

Only after approval are the controlled remediation commands executed.

This prevents the AI/investigation layer from having unrestricted permission to make changes to the Kubernetes cluster.

---

## 🚀 Remediation Execution

After approval, BigBlueOnCall executes the approved remediation and displays the command output.

Example:

```text
✓ Image updated
✓ Deployment rollout completed
✓ Workload verification started
```

The operator can see exactly what was executed and whether each command succeeded or failed.

---

## ✅ Verification

After remediation, BigBlueOnCall checks the workload again.

The incident lifecycle becomes:

```text
ImagePullBackOff
       ↓
Investigation
       ↓
Root Cause Identified
       ↓
Remediation Proposed
       ↓
Human Approval
       ↓
Remediation Executed
       ↓
Verification
       ↓
Running
       ↓
🎉 INCIDENT RESOLVED
```

---

# 📸 Screenshots

## 🚨 Dashboard

BigBlueOnCall provides a dashboard showing cluster workloads, healthy workloads, active incidents, and resolved incidents.

<img width="1725" height="915" alt="BigBlueOnCall Dashboard" src="https://github.com/user-attachments/assets/729887c0-a171-4f66-9197-1df370b7280b" />

---

## 🔴 Failed Pod Detection

An unhealthy Kubernetes workload is detected as an active incident.

<img width="1725" height="915" alt="Failed Pod Detection" src="https://github.com/user-attachments/assets/6a67f5bc-b4f8-457e-a11a-980633829448" />

---

## 🔎 Incident Investigation

BigBlueOnCall collects pod details, Kubernetes events, and container logs and presents the investigation in the UI.

<img width="1725" height="915" alt="Incident Investigation" src="https://github.com/user-attachments/assets/a5df6755-e798-4912-8498-24c797180068" />

---

## 👤 Human Approval

The proposed remediation commands are displayed before execution. The operator explicitly approves the remediation.

<img width="1725" height="915" alt="Human Approval" src="https://github.com/user-attachments/assets/979d078a-9000-4748-8f72-161eaba1f9f8" />

<img width="1725" height="915" alt="Approval Workflow" src="https://github.com/user-attachments/assets/9ab8e8e2-7acf-44a7-acdc-5fcca9ad4add" />

---

## ✅ Incident Resolved

After approval, the remediation is executed and the workload is verified.

<img width="1725" height="915" alt="Incident Resolved" src="https://github.com/user-attachments/assets/9586e803-6d3f-4b7e-9b93-a8d6ef0cf6bf" />

<img width="1725" height="915" alt="Verification" src="https://github.com/user-attachments/assets/f97d2183-9531-4400-bdcb-b874c43f4720" />

---

# 🏗️ Architecture

```text
                         BigBlueOnCall
                              │
                              ▼
                     ┌─────────────────┐
                     │   Streamlit UI  │
                     └────────┬────────┘
                              │
                              ▼
                     ┌─────────────────┐
                     │  Investigation  │
                     │      Tools      │
                     └────────┬────────┘
                              │
                  ┌───────────┼───────────┐
                  ▼           ▼           ▼
                Pods        Events       Logs
                  │           │           │
                  └───────────┼───────────┘
                              ▼
                     ┌─────────────────┐
                     │    Diagnosis    │
                     └────────┬────────┘
                              │
                              ▼
                     ┌─────────────────┐
                     │   Remediation   │
                     │    Proposal     │
                     └────────┬────────┘
                              │
                              ▼
                     ┌─────────────────┐
                     │ Human Approval  │
                     └────────┬────────┘
                              │
                              ▼
                     ┌─────────────────┐
                     │ Safe Executor   │
                     └────────┬────────┘
                              │
                              ▼
                         Kubernetes
                              │
                              ▼
                         Verification
```

---

# 📁 Project Structure

```text
BigBlueOnCall/
│
├── app.py
│   └── Streamlit dashboard and incident workflow
│
├── tools.py
│   └── Kubernetes investigation tools
│
├── diagnosis.py
│   └── Incident diagnosis logic
│
├── remediation.py
│   └── Controlled remediation proposals and execution
│
├── investigator.py
│   └── Incident investigation workflow
│
├── agent.py
│   └── Agent experimentation
│
├── ai_report.py
│   └── Gemini-based incident analysis
│
├── .gitignore
└── README.md
```

---

# 🧰 Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application and automation |
| Kubernetes | Container orchestration |
| Kubernetes Python Client | Cluster investigation |
| kind | Local Kubernetes cluster |
| Docker | Container runtime |
| Streamlit | Web interface |
| Google Gemini | AI-assisted analysis |
| GitHub Codespaces | Development environment |

---

# 🚀 Getting Started

## Prerequisites

- Docker
- Kubernetes
- kubectl
- kind
- Python 3.x

## Create the Kubernetes Cluster

```bash
kind create cluster --name bigblueoncall
```

Verify:

```bash
kubectl get nodes
```

## Install Dependencies

```bash
pip install kubernetes streamlit google-genai
```

## Start BigBlueOnCall

```bash
streamlit run app.py
```

The Streamlit application runs on:

```text
http://localhost:8501
```

For GitHub Codespaces, forward port `8501`.

---

# 🧪 Test the Incident Workflow

Create an intentionally broken image configuration:

```bash
kubectl set image deployment/broken nginx=nginx:doesnotexist
```

Check the workload:

```bash
kubectl get pods
```

Expected:

```text
broken-xxxxx   0/1   ImagePullBackOff
```

Open BigBlueOnCall and click:

```text
🔍 Scan Cluster
```

Then follow:

```text
Detect
  ↓
Investigate
  ↓
Review Pod Details
  ↓
Review Events
  ↓
Review Logs
  ↓
Review Diagnosis
  ↓
Review Proposed Commands
  ↓
👤 Human Approval
  ↓
🚀 Approve & Fix
  ↓
✅ Verify
```

---

# 🛡️ Safety Model

BigBlueOnCall uses a human-in-the-loop approach for remediation.

```text
Evidence
   ↓
Diagnosis
   ↓
Remediation Proposal
   ↓
Human Review
   ↓
Explicit Approval
   ↓
Controlled Execution
   ↓
Verification
```

The remediation layer is intentionally controlled rather than allowing unrestricted AI-generated shell commands to execute against the Kubernetes cluster.

---

# 🤖 AI Roadmap

The project is being extended toward an agentic SRE workflow where AI can assist with:

- Incident investigation
- Evidence correlation
- Root-cause analysis
- Incident summarization
- Remediation recommendations
- SRE troubleshooting assistance

Future incident scenarios include:

- CrashLoopBackOff
- OOMKilled
- Pending pods
- Readiness/liveness probe failures
- Node health issues
- Deployment rollout failures
- Certificate expiry
- Kubernetes networking failures

Potential integrations include:

- Prometheus
- Grafana
- Slack
- Kubernetes metrics
- Incident history and audit trails

---

# 🎯 Project Goals

BigBlueOnCall demonstrates practical SRE and cloud engineering concepts:

- Kubernetes troubleshooting
- Incident investigation
- Observability
- SRE automation
- Infrastructure reliability
- Human-in-the-loop automation
- Controlled remediation
- Agentic AI concepts

---

# 💡 Design Philosophy

> **Automate investigation and reduce SRE toil while keeping humans in control of infrastructure changes.**

BigBlueOnCall is designed to assist an on-call engineer rather than replace the engineer's judgment.

---

# 👩‍💻 Author

**Serishma Pera**

Kubernetes | SRE | Cloud Infrastructure | Automation

---

## 🚧 Project Status

**Active Development**

### Current capabilities

- ✅ Kubernetes workload detection
- ✅ Failed pod investigation
- ✅ Pod details
- ✅ Kubernetes event collection
- ✅ Container log collection
- ✅ Incident diagnosis
- ✅ Remediation proposal
- ✅ Human approval
- ✅ Controlled remediation execution
- ✅ Post-remediation verification
- 🚧 AI-powered investigation and reasoning
- 🚧 Additional Kubernetes incident scenarios
