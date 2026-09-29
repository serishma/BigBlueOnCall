┌─────────────────────┐
│     Verification    │
│                     │
│ Pod → Running       │
└─────────────────────┘
```

**before the images.**

### 2. Immediately after that, add:

```markdown
## 📸 Screenshots

### 🚨 Dashboard

[Your uploaded dashboard image]

### 🔴 Failed Pod Detection

[Your uploaded failed-pod image]

### 🔎 Incident Investigation

[Your uploaded investigation image]

### 👤 Human Approval

[Your uploaded approval image]

### ✅ Incident Resolved

[Your uploaded resolved image]
```

However, since GitHub has already uploaded your images, **don't upload them again**.

When you dragged them into the README, GitHub inserted lines beginning with:

```html
<img width="1725" height="915" alt="Screenshot ..." src="https://github.com/user-attachments/assets/...">
```

Those lines are correct.

### 3. The important part

Your README should look structurally like this:

````markdown
## 🔄 How It Works

```text
┌─────────────────────┐
│   Kubernetes        │
│      Cluster        │
└──────────┬──────────┘
           │
           ▼
        ...
           │
           ▼
┌─────────────────────┐
│     Verification    │
│                     │
│ Pod → Running       │
└─────────────────────┘
```

## 📸 Screenshots

### 🚨 Dashboard

<img width="1725" height="915" alt="Screenshot 2026-09-29 at 10 30 22 PM" src="https://github.com/user-attachments/assets/729887c0-a171-4f66-9197-1df370b7280b" />


### 🔴 Failed Pod Detection

<img width="1725" height="915" alt="Screenshot 2026-09-29 at 10 30 33 PM" src="https://github.com/user-attachments/assets/6a67f5bc-b4f8-457e-a11a-980633829448" />


### 🔎 Incident Investigation

<img width="1725" height="915" alt="Screenshot 2026-09-29 at 10 30 46 PM" src="https://github.com/user-attachments/assets/a5df6755-e798-4912-8498-24c797180068" />

### 👤 Human Approval

<img width="1725" height="915" alt="Screenshot 2026-09-29 at 10 30 58 PM" src="https://github.com/user-attachments/assets/979d078a-9000-4748-8f72-161eaba1f9f8" />

<img width="1725" height="915" alt="Screenshot 2026-09-29 at 10 31 10 PM" src="https://github.com/user-attachments/assets/9ab8e8e2-7acf-44a7-acdc-5fcca9ad4add" />

### ✅ Incident Resolved

<img width="1725" height="915" alt="Screenshot 2026-09-29 at 10 34 35 PM" src="https://github.com/user-attachments/assets/9586e803-6d3f-4b7e-9b93-a8d6ef0cf6bf" />
<img width="1725" height="915" alt="Screenshot 2026-09-29 at 10 34 47 PM" src="https://github.com/user-attachments/assets/f97d2183-9531-4400-bdcb-b874c43f4720" />

