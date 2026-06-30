#  API-Penetrator: Automated Security Assessment Framework

An automated API penetration testing tool designed to identify and exploit vulnerabilities listed in the **OWASP API Security Top 10**. This framework demonstrates modern **Exploit Chaining** by linking input validation flaws with broken authorization controls to simulate a realistic application-layer breach.

---

##  Technical Architecture & Attack Chain

Instead of testing vulnerabilities in isolation, **API-Penetrator** chains multiple security flaws together to maximize testing efficiency:

1. **Phase 1: Recon & SQLi Scanning**  
   Audits the public product search API parameter using custom SQL injection strings to force database exposure states.
2. **Phase 2: Authentication Bypass**  
   Injects malicious payloads into the POST login interface to bypass backend identity validation, automatically capturing the Administrative **JWT Bearer Token**.
3. **Phase 3: BOLA/IDOR Exfiltration**  
   Injects the hijacked token into downstream authenticated request headers, fuzzing sequential user IDs to dump private profile data (Names, Cities, and Phone numbers).

---

##  OWASP API Top 10 Risk Mapping

The framework specifically aligns its automated offensive actions with global cybersecurity standards:

| Threat Vector | OWASP Reference | Risk Severity | Target Endpoint Matrix |
| :--- | :--- | :--- | :--- |
| **Broken Object Level Authorization (BOLA)** | API1:2023 | 🚨 Critical | `/api/Addresss/{id}` |
| **Broken Authentication** | API2:2023 | 🔥 High | `/rest/user/login` |
| **SQL Injection (SQLi)** | Global Flaw | ⚡ High | `/rest/products/search` |

---

##  Repository Components & Structure

* **`api_scanner.py`**: The core command-line penetration testing engine that runs the exploitation pipeline and outputs direct terminal logs.
* **`app.py`**: The interactive web dashboard interface engineered using Streamlit to visualize metrics and captured data streams.
* **`api_report.txt`**: The automatically generated physical text log containing timestamps and confirmed Proof-of-Concept (PoC) states.

---

##  Laboratory Setup Guide

To safely validate and test the capabilities of this engine, use the official open-source vulnerable environment **OWASP Juice Shop**.

###  Prerequisites
* **Python 3.10+** (Core runtime environment)
* **Docker Desktop** (Virtualization container sandbox)

### 1. Deploy the Target Sandbox Container
Spin up the decoupled vulnerable application layer locally mapped to port 3000:
```bash
docker run -d -p 3000:3000 bkimminich/juice-shop
