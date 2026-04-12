# Brute Force Detection - SOC Use Case

## 📌 Scenario

Multiple failed login attempts detected on a Windows endpoint, potentially indicating a brute force attack.

---

## 🎯 Objective

Detect and investigate repeated authentication failures to identify potential unauthorized access attempts.

---

## 📊 Log Source

- Windows Security Event Logs
- Sysmon (optional correlation)

---

## 🔑 Relevant Event IDs

| Event ID | Description |
|--------|-------------|
| 4625 | Failed login attempt |
| 4624 | Successful login |
| 4672 | Special privileges assigned |

---

## 🧠 Detection Logic

Trigger alert when:

- More than **5 failed login attempts (Event ID 4625)**  
- Within **5–10 minutes**  
- From the same IP or targeting the same user  

---

## 🔍 Example Log (Event 4625)
