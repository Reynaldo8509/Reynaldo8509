# Brute Force Detection - SOC Use Case

## 📌 Scenario
Multiple failed login attempts detected on a Windows endpoint, potentially indicating a brute force attack.

---

## 🎯 Objective
Detect repeated authentication failures and identify unauthorized access attempts.

---

## 📊 Log Source
- Windows Security Event Logs
- Sysmon (optional correlation)

---

## 🔑 Relevant Event IDs

| Event ID | Description |
|----------|------------|
| 4625     | Failed login attempt |
| 4624     | Successful login |
| 4672     | Special privileges assigned |

---

## 🧠 Detection Logic

Alert when:

- More than **5 failed login attempts**
- Within **5–10 minutes**
- Same source IP or same user targeted

---

## 🔍 Example Log
Account Name: admin
Source Network Address: 192.168.1.50
Failure Reason: Unknown user name or bad password


---

## ⚠️ Triage (SOC Tier 1)

1. Validate alert
2. Identify source IP
3. Check targeted account
4. Look for successful login after failures (Event ID 4624)

---

## 🧪 Investigation (SOC Tier 2)

- Correlate logs across timeline
- Detect lateral movement
- Analyze account behavior
- Verify if account was compromised

---

## 🚨 Response Actions

- Lock affected account
- Block malicious IP
- Enforce password reset
- Escalate incident if necessary

---

## 🧬 MITRE ATT&CK

- T1110 — Brute Force

---

## 🧠 Analyst Notes

Repeated failed login attempts followed by a successful login may indicate account compromise.

This detection helps identify early-stage attacks targeting authentication systems.



