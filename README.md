#  API-Penetrator: Automated OWASP API Top 10 Exploitation Framework

<p align="center">
  <img src="https://img.shields.io/badge/Security-Auditing-red?style=for-the-badge&logo=cyberdefenders" alt="Security">
  <img src="https://img.shields.io/badge/Automation-Python%203-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Dashboard-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/Environment-Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker">
</p>

---

##  Project Overview

**API-Penetrator** is an advanced, automated API penetration testing tool designed to identify, exploit, and document critical security flaws outlined in the **OWASP API Security Top 10**. 

Unlike basic vulnerability scanners that test individual endpoints in isolation, this framework demonstrates real-world threat impact by implementing an automated **Exploit Chain**. It links input validation flaws with broken authorization controls to hijack administrative sessions and exfiltrate sensitive data.

---

##  System Architecture & Exploit Chain Pipeline

The core power of this tool lies in its multi-stage attack pipeline, mimicking the exact workflow of an advanced persistent threat (APT) or an expert penetration tester:

```text
[ STAGE 1: SQLi DISCOVERY ]  Scans the public product search API to detect unsanitized input vulnerabilities.
            │
            ▼
[ STAGE 2: AUTH BYPASS ]     Injects malicious query payloads into the POST login interface.
            │                 Bypasses password validation and captures the Admin's JWT Bearer Token.
            ▼
[ STAGE 3: BOLA EXPLOITATION]  Mounts the stolen administrative JWT token into authenticated request headers.
                              Fuzzes sequential object IDs to exfiltrate private user payment/profile records.