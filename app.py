import streamlit as st
import sqlite3
import pandas as pd
import datetime
import random
import time

# --- PAGE SETUP ---
st.set_page_config(page_title="GullakCoin Pro", page_icon="🪙", layout="wide")

# --- CUSTOM CSS (Clean Light Theme & High Visibility) ---
st.markdown("""
<style>
    /* Global App Background & Text */
    .stApp { background-color: #ffffff; color: #111827; font-family: 'Inter', sans-serif; }
    [data-testid="stSidebar"] { background-color: #f1f5f9; border-right: 1px solid #cbd5e1; }
    [data-testid="stSidebar"] * { color: #111827 !important; }
    [data-testid="stMetricValue"] { font-size: 24px; color: #059669 !important; font-weight: 700; }
    
    /* Input Fields Visibility */
    .stTextInput input, .stSelectbox select {
        background-color: #ffffff !important; color: #111827 !important; border: 1px solid #cbd5e1 !important; border-radius: 8px;
    }
    
    .auth-container {
        background: #f8fafc;
        padding: 40px; border-radius: 20px; border: 1px solid #cbd5e1;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05); max-width: 480px; margin: 0 auto;
    }
    .logo-container { text-align: center; margin-bottom: 25px; }
    .logo-badge {
        display: inline-block; background: linear-gradient(135deg, #059669, #0284c7); color: #ffffff;
        font-weight: 900; font-size: 28px; padding: 12px 20px; border-radius: 16px;
        box-shadow: 0 8px 20px rgba(5, 150, 105, 0.2); letter-spacing: 1px;
    }
    .brand-title { font-size: 28px; font-weight: 800; color: #111827; margin-top: 15px; }
    .brand-tagline { font-size: 13px; color: #4b5563; margin-top: 5px; font-style: italic; }
    
    .plan-card {
        background-color: #f8fafc; padding: 25px; border-radius: 15px; border: 1px solid #cbd5e1;
        height: 220px; display: flex; flex-direction: column; justify-content: flex-start; margin-bottom: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
    }
    .detail-card {
        background-color: #f8fafc; padding: 20px; border-radius: 10px; border: 1px solid #059669;
        text-align: center; margin-top: 15px; margin-bottom: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.02);
    }
    .plan-title { font-size: 22px; font-weight: bold; margin-bottom: 10px; color: #111827;}
    .plan-desc { font-size: 13px; color: #4b5563; margin-bottom: 15px; line-height: 1.5; }
    .plan-target { font-size: 20px; font-weight: bold; color: #059669; margin-top: auto; }
    .disclaimer { font-size: 11px; color: #dc2626; font-style: italic; }
    .locked-box {
        background-color: #fef3c7; border: 1px solid #f59e0b; padding: 20px; border-radius: 10px; text-align: center; margin-top: 20px; color: #78350f;
    }
    .strict-rule-box {
        background-color: #fee2e2; border: 1px solid #f87171; padding: 15px; border-radius: 8px; color: #991b1b; font-size: 13px; margin-bottom: 20px;
    }
    .comparison-box {
        background-color: #d1fae5; border: 1px solid #34d399; padding: 15px; border-radius: 8px; color: #065f46; font-size: 13px; margin-bottom: 20px;
    }
    .alert-failed {
        background-color: #fee2e2; border: 1px solid #f87171; padding: 15px; border-radius: 8px; color: #991b1b; margin-bottom: 15px;
    }
    .support-card {
        background-color: #f8fafc; padding: 20px; border-radius: 12px; border: 1px solid #cbd5e1; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.02);
    }
    .gamification-box {
        background: linear-gradient(135deg, #fef3c7, #d1fae5);
        border: 1px solid #f59e0b; padding: 20px; border-radius: 15px; margin-bottom: 20px; color: #111827;
    }
</style>
""", unsafe_allow_html=True)

# --- DATABASE LOGIC ---
def init_db():
    conn = sqlite3.connect('gullakcoin_advanced.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                 id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT, investor_id TEXT, kyc_status TEXT, pan TEXT, aadhar TEXT, bank_acc TEXT, ifsc TEXT, branch TEXT, bank_mobile TEXT)''')
    
    # Safe migration to add columns if they don't exist in older DB
    existing_cols = [col[1] for col in c.execute("PRAGMA table_info(users)").fetchall()]
    if 'aadhar' not in existing_cols:
        c.execute("ALTER TABLE users ADD COLUMN aadhar TEXT")
    if 'ifsc' not in existing_cols:
        c.execute("ALTER TABLE users ADD COLUMN ifsc TEXT")
    if 'branch' not in existing_cols:
        c.execute("ALTER TABLE users ADD COLUMN branch TEXT")
    if 'bank_mobile' not in existing_cols:
        c.execute("ALTER TABLE users ADD COLUMN bank_mobile TEXT")

    c.execute('''CREATE TABLE IF NOT EXISTS transactions (
                 id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, trans_type TEXT, category TEXT, amount REAL, status TEXT, date TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS subscriptions (
                 id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, plan_name TEXT, target_amount INTEGER, frequency TEXT, installment_amt REAL, date TEXT)''')
    conn.commit()
    conn.close()

def get_user_profile(username):
    conn = sqlite3.connect('gullakcoin_advanced.db')
    c = conn.cursor()
    c.execute("SELECT investor_id, kyc_status, pan, aadhar, bank_acc, ifsc, branch, bank_mobile FROM users WHERE username=?", (username,))
    res = c.fetchone()
    conn.close()
    return res

def update_kyc(username, pan, aadhar, bank_acc, ifsc, branch, bank_mobile):
    conn = sqlite3.connect('gullakcoin_advanced.db')
    c = conn.cursor()
    if bank_mobile.strip() == username.strip():
        kyc_status = 'Verified (Approved)'
    else:
        kyc_status = 'Pending (Mobile Mismatch)'
        
    c.execute("UPDATE users SET pan=?, aadhar=?, bank_acc=?, ifsc=?, branch=?, bank_mobile=?, kyc_status=? WHERE username=?", 
              (pan, aadhar, bank_acc, ifsc, branch, bank_mobile, kyc_status, username))
    conn.commit()
    conn.close()
    return kyc_status

def update_password(username, new_pass):
    conn = sqlite3.connect('gullakcoin_advanced.db')
    c = conn.cursor()
    c.execute("UPDATE users SET password=? WHERE username=?", (new_pass, username))
    conn.commit()
    conn.close()

def get_data(username):
    conn = sqlite3.connect('gullakcoin_advanced.db')
    df_tx = pd.read_sql_query(f"SELECT * FROM transactions WHERE username='{username}'", conn)
    df_sub = pd.read_sql_query(f"SELECT * FROM subscriptions WHERE username='{username}' ORDER BY id DESC LIMIT 1", conn)
    conn.close()
    return df_tx, df_sub

def add_subscription(username, plan_name, target_amount, frequency_text, installment_amt):
    conn = sqlite3.connect('gullakcoin_advanced.db')
    c = conn.cursor()
    dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute('INSERT INTO subscriptions (username, plan_name, target_amount, frequency, installment_amt, date) VALUES (?, ?, ?, ?, ?, ?)', 
              (username, plan_name, target_amount, frequency_text, installment_amt, dt))
    c.execute('INSERT INTO transactions (username, trans_type, category, amount, status, date) VALUES (?, ?, ?, ?, ?, ?)', 
              (username, 'Income', 'Investment', installment_amt, 'Success', dt))
    conn.commit()
    conn.close()

def log_failed_transaction(username, installment_amt):
    conn = sqlite3.connect('gullakcoin_advanced.db')
    c = conn.cursor()
    dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute('INSERT INTO transactions (username, trans_type, category, amount, status, date) VALUES (?, ?, ?, ?, ?, ?)', 
              (username, 'Expense', 'Failed SIP', installment_amt, 'Failed (Insufficient Balance)', dt))
    conn.commit()
    conn.close()

init_db()

# --- SESSION STATE ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'current_user' not in st.session_state: st.session_state.current_user = ""
if 'otp_generated' not in st.session_state: st.session_state.otp_generated = ""
if 'auth_stage' not in st.session_state: st.session_state.auth_stage = "none"
if 'selected_plan' not in st.session_state: st.session_state.selected_plan = None
if 'forgot_user' not in st.session_state: st.session_state.forgot_user = ""

# --- AUTHENTICATION SCREEN ---
if not st.session_state.logged_in:
    st.write("")
    st.markdown("<div class='auth-container'>", unsafe_allow_html=True)
    st.markdown("""
        <div class="logo-container">
            <div class="logo-badge">GC</div>
            <div class="brand-title">GullakCoin Pro</div>
            <div class="brand-tagline">“Architecting Tomorrow’s Yield, One Micro-Milestone at a Time.”</div>
        </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["Secure Login", "Create Account", "🔑 Forgot Password"])
    
    with tab1:
        st.write("")
        l_user = st.text_input("Registered Email or Mobile Number", key="l_user")
        l_pass = st.text_input("Secure Password", type="password", key="l_pass")
        st.write("")
        
        if st.button("Request Login OTP", use_container_width=True, type="primary"):
            conn = sqlite3.connect('gullakcoin_advanced.db')
            c = conn.cursor()
            c.execute("SELECT * FROM users WHERE username=? AND password=?", (l_user, l_pass))
            user_exists = c.fetchone()
            conn.close()
            
            if user_exists:
                otp = str(random.randint(100000, 999999))
                st.session_state.otp_generated = otp
                st.session_state.auth_stage = "login_otp"
                st.success(f"🔐 Security OTP Sent: **{otp}** (Simulated SMS)")
            else:
                st.error("Invalid credentials.")
        
        if st.session_state.auth_stage == "login_otp":
            l_otp_input = st.text_input("Enter 6-Digit Verification Code", key="l_otp")
            if st.button("Verify & Access Dashboard", type="primary", use_container_width=True):
                if l_otp_input == st.session_state.otp_generated:
                    st.session_state.logged_in = True
                    st.session_state.current_user = l_user
                    st.session_state.auth_stage = "none"
                    st.rerun()
                else:
                    st.error("Invalid verification code.")
                    
    with tab2:
        st.write("")
        s_user = st.text_input("Email or Mobile Number", key="s_user")
        s_pass = st.text_input("Create Secure Password", type="password", key="s_pass")
        st.write("")
        
        if st.button("Request Registration OTP", use_container_width=True):
            if s_user and s_pass:
                conn = sqlite3.connect('gullakcoin_advanced.db')
                c = conn.cursor()
                c.execute("SELECT * FROM users WHERE username=?", (s_user,))
                if c.fetchone():
                    st.error("Account already exists.")
                else:
                    otp = str(random.randint(100000, 999999))
                    st.session_state.otp_generated = otp
                    st.session_state.auth_stage = "signup_otp"
                    st.success(f"🔐 Registration OTP Sent: **{otp}** (Simulated SMS)")
                conn.close()
            else:
                st.warning("Please fill in all fields.")
        
        if st.session_state.auth_stage == "signup_otp":
            s_otp_input = st.text_input("Enter 6-Digit Verification Code", key="s_otp")
            if st.button("Verify & Complete Registration", type="primary", use_container_width=True):
                if s_otp_input == st.session_state.otp_generated:
                    investor_id = f"GC-PRO-{random.randint(100000, 999900)}"
                    conn = sqlite3.connect('gullakcoin_advanced.db')
                    c = conn.cursor()
                    c.execute("INSERT INTO users (username, password, investor_id, kyc_status, pan, aadhar, bank_acc, ifsc, branch, bank_mobile) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                              (s_user, s_pass, investor_id, 'Pending', '', '', '', '', '', ''))
                    conn.commit()
                    conn.close()
                    st.success(f"🎉 Account created successfully! Your Investor ID is {investor_id}. Please login.")
                    st.session_state.auth_stage = "none"
                    time.sleep(3)
                    st.rerun()
                else:
                    st.error("Invalid verification code.")

    with tab3:
        st.write("")
        f_user = st.text_input("Enter Your Registered Email or Mobile Number", key="f_user")
        st.write("")
        
        if st.button("Send Password Reset OTP", use_container_width=True):
            if f_user:
                conn = sqlite3.connect('gullakcoin_advanced.db')
                c = conn.cursor()
                c.execute("SELECT * FROM users WHERE username=?", (f_user,))
                user_record = c.fetchone()
                conn.close()
                
                if user_record:
                    otp = str(random.randint(100000, 999999))
                    st.session_state.otp_generated = otp
                    st.session_state.forgot_user = f_user
                    st.session_state.auth_stage = "forgot_otp"
                    st.success(f"🔐 Password Reset OTP Sent: **{otp}** (Simulated SMS)")
                else:
                    st.error("Account not found with this mobile number/email.")
            else:
                st.warning("Please enter your registered number or email.")
                
        if st.session_state.auth_stage == "forgot_otp":
            f_otp_input = st.text_input("Enter 6-Digit Reset OTP", key="f_otp")
            new_pass_1 = st.text_input("New Password", type="password", key="n_pass1")
            new_pass_2 = st.text_input("Confirm New Password", type="password", key="n_pass2")
            
            if st.button("Reset Password & Save", type="primary", use_container_width=True):
                if f_otp_input == st.session_state.otp_generated:
                    if new_pass_1 and new_pass_1 == new_pass_2:
                        update_password(st.session_state.forgot_user, new_pass_1)
                        st.success("🎉 Password updated successfully! Please go to Secure Login.")
                        st.session_state.auth_stage = "none"
                        st.session_state.forgot_user = ""
                        time.sleep(3)
                        st.rerun()
                    else:
                        st.error("Passwords do not match or empty.")
                else:
                    st.error("Invalid verification code.")
                    
    st.markdown("</div>", unsafe_allow_html=True)

# --- MAIN DASHBOARD ---
else:
    username = st.session_state.current_user
    user_prof = get_user_profile(username)
    investor_id = user_prof[0] if user_prof and user_prof[0] else "GC-PRO-PENDING"
    kyc_status = user_prof[1] if user_prof else "Pending"
    pan_num = user_prof[2] if user_prof else ""
    aadhar_num = user_prof[3] if user_prof else ""
    bank_acc = user_prof[4] if user_prof else ""
    ifsc_code = user_prof[5] if user_prof else ""
    branch_name = user_prof[6] if user_prof else ""
    bank_mobile = user_prof[7] if user_prof else ""

    df_tx, df_sub = get_data(username)

    portfolio_value = df_tx[(df_tx['category'] == 'Investment') & (df_tx['trans_type'] == 'Income') & (df_tx['status'] == 'Success')]['amount'].sum() if not df_tx.empty else 0
    target_value = 0
    active_plan = None
    balance_target = 0
    estimated_maturity = 0

    def calculate_payout(target, freq):
        if 'Daily' in freq: roi = 0.08
        elif 'Weekly' in freq: roi = 0.10
        else: roi = 0.18
        
        success_tx_count = len(df_tx[df_tx['status'] == 'Success']) if not df_tx.empty else 0
        streak_bonus = 0.01 if success_tx_count >= 3 else 0.0
        
        effective_roi = roi + streak_bonus
        maturity = target + (target * effective_roi)
        fee = maturity * 0.02
        gst = fee * 0.18
        net_payout = maturity - fee - gst
        net_profit = net_payout - target
        return maturity, fee, gst, net_payout, net_profit, streak_bonus

    if not df_sub.empty:
        active_plan = df_sub.iloc[0]
        target_value = active_plan['target_amount']
        balance_target = max(target_value - portfolio_value, 0)
        estimated_maturity, _, _, _, _, _ = calculate_payout(target_value, active_plan['frequency'])

    # SIDEBAR
    st.sidebar.markdown(f"**👤 {username}**")
    st.sidebar.markdown(f"🆔 `{investor_id}`")
    st.sidebar.markdown(f"🛡️ KYC: **{kyc_status}**")
    st.sidebar.markdown("---")
    st.sidebar.markdown("## 🪙 GullakCoin Pro")
    st.sidebar.markdown("INVESTOR PORTAL")
    
    menu = st.sidebar.radio("", ["📦 Product offerings", "📊 My Portfolio", "📝 Transaction History", "👤 Profile & KYC", "💬 Support & Help", "❓ FAQs"])
    st.sidebar.markdown("---")
    if st.sidebar.button("🚪 Logout", type="primary", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.current_user = ""
        st.session_state.selected_plan = None
        st.rerun()

    # HEADER METRICS
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("Portfolio Value", f"₹ {portfolio_value:,.2f}")
    with col2: st.metric("Target Value", f"₹ {target_value:,.0f}")
    with col3: st.metric("Balance Target", f"🔒 ₹ {balance_target:,.2f}" if balance_target > 0 else "✅ Completed")
    
    with col4:
        if portfolio_value >= target_value and target_value > 0:
            st.metric("Estimated Maturity", f"₹ {estimated_maturity:,.0f}")
        else:
            st.metric("Estimated Maturity", "🔒 Locked")
            
    st.markdown("---")

    # DASHBOARD CONTENT
    if menu == "📦 Product offerings":
        if st.session_state.selected_plan is None:
            st.markdown("## Auto-Invest in Promising Startups.")
            st.markdown("<p style='color: #4b5563; font-size: 16px; margin-bottom: 5px;'>Select a structured allocation plan below to view projections and E-Mandate frequencies.</p>", unsafe_allow_html=True)
            
            st.markdown("""
            <div class="comparison-box">
                <b>💡 Why choose GullakCoin Pro over traditional Bank FD / Savings Account?</b><br>
                While a standard bank savings account or short-term FD yields a nominal 3% to 7% p.a., our 4-month structured milestone model (3 Months SIP + 1 Month Hold) targets significantly higher net growth through diversified startup allocations. Lock in your funds for 120 days to unlock superior returns compared to traditional banking.
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<p class='disclaimer'>*Disclaimer: All target yields are estimates based on quantitative models and carry market risks.</p>", unsafe_allow_html=True)
            st.write("")
            
            plans = [
                ("GullakCoin Seed", 5000, "Best for early-stage startup exposure with balanced micro-tickets.", "seed"),
                ("GullakCoin Growth", 25000, "For dynamically scaling an emerging startup portfolio.", "growth"),
                ("GullakCoin Plus", 50000, "Advanced access into mid-stage startup rounds.", "plus"),
                ("GullakCoin Superplus", 100000, "Exclusive curated high-net-worth venture allocations.", "superplus")
            ]
            
            cols = st.columns(4)
            for i, (title, target_amt, desc, key_id) in enumerate(plans):
                with cols[i]:
                    st.markdown(f"""
                    <div class="plan-card">
                        <div class="plan-title">{title}</div>
                        <div class="plan-desc">{desc}</div>
                        <div class="plan-target">🎯 Target: ₹ {target_amt:,.0f}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button(f"Explore {title.split()[-1]}", key=f"expl_{key_id}", use_container_width=True):
                        st.session_state.selected_plan = {"title": title, "target": target_amt, "desc": desc}
                        st.rerun()
        else:
            plan = st.session_state.selected_plan
            target_amt = plan['target']
            title = plan['title']
            
            if st.button("⬅️ Back to All Plans"):
                st.session_state.selected_plan = None
                st.rerun()
                
            st.markdown(f"<h1>{title} <span style='color: #059669;'>| Target: ₹ {target_amt:,.0f}</span></h1>", unsafe_allow_html=True)
            st.write(plan['desc'])
            
            st.markdown("""
            <div class="strict-rule-box">
                <b>⚠️ Important Lock-in & E-Mandate Rule:</b><br>
                Once you authorize AutoPay, installments deduct automatically. <b>You cannot withdraw</b> your funds until the full Target Principal and maturity cycle are 100% completed. In case of insufficient bank balance, a 5-day grace period applies before cycle timeline extension.
            </div>
            """, unsafe_allow_html=True)
            
            st.subheader("Configure AutoPay E-Mandate Frequency:")
            
            freqs = [
                ("Daily", target_amt / 90, 0.08),
                ("Weekly", (target_amt / 90) * 7, 0.10),
                ("Monthly", target_amt / 3, 0.18)
            ]
            
            f_cols = st.columns(3)
            for i, (f_name, f_amt, f_roi) in enumerate(freqs):
                maturity, fee, gst, net_payout, net_profit, bonus = calculate_payout(target_amt, f_name)
                with f_cols[i]:
                    bonus_text = f" (+{bonus*100:.1f}% AI Streak Bonus)" if bonus > 0 else ""
                    st.markdown(f"""
                    <div class="detail-card">
                        <h3 style='margin-bottom:0;'>{f_name} SIP</h3>
                        <p style='color: #4b5563;'>Deduction: <b>₹ {f_amt:,.2f}</b></p>
                        <hr style='border-color: #cbd5e1;'>
                        <p style='text-align: left; font-size: 13px; color: #111827;'>
                            <b>Target Yield Est.:</b> {f_roi*100:.0f}%{bonus_text}<br>
                            <b>Gross Maturity:</b> ₹ {maturity:,.2f}<br>
                            <span style='color: #d97706;'><b>Tenure:</b> 3 Months</span><br>
                            <span style='color: #d97706;'><b>Lock-in Period:</b> 1 Month</span><br>
                            <b>Platform Fee + GST:</b> -₹ {fee+gst:,.2f}<br><br>
                            <span style='color: #059669; font-size: 16px;'><b>Est. Net Payout: ₹ {net_payout:,.2f}</b></span>
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button(f"Authorize {f_name} AutoPay", key=f"sub_{f_name}", type="primary", use_container_width=True):
                        add_subscription(username, title, target_amt, f_name, f_amt)
                        st.success(f"✅ E-Mandate registered successfully for {title} via {f_name} SIP!")
                        st.session_state.selected_plan = None
                        time.sleep(2)
                        st.rerun()

    elif menu == "📊 My Portfolio":
        st.subheader("Active Asset Allocation & Projections")
        if active_plan is not None:
            success_count = len(df_tx[df_tx['status'] == 'Success']) if not df_tx.empty else 0
            streak_days = success_count * 3
            badge_level = "🔥 Gold Investor Streak" if success_count >= 3 else "🌱 Silver Streak (Build up to unlock +1% Yield Boost)"
            
            st.markdown(f"""
            <div class="gamification-box">
                <h4 style="color: #d97706; margin-top:0;">🤖 AI Yield Predictor & Gamification</h4>
                <p style="margin-bottom: 5px;"><b>Active Streak:</b> {streak_days} Days Consistent AutoPay</p>
                <p style="margin-bottom: 5px;"><b>Investor Status Badge:</b> {badge_level}</p>
                <p style="font-size: 12px; color: #4b5563; margin-bottom:0;">Maintain consistent deductions to qualify for AI-modeled yield bonuses and VIP fee waivers.</p>
            </div>
            """, unsafe_allow_html=True)

            failed_txs = df_tx[df_tx['status'] == 'Failed (Insufficient Balance)']
            
            if not failed_txs.empty:
                st.markdown(f"""
                <div class="alert-failed">
                    <b>⚠️ AutoPay E-Mandate Failure Detected!</b><br>
                    Your recent installment of <b>₹ {active_plan['installment_amt']:,.2f}</b> failed due to insufficient bank balance. A 5-day grace period is active. Please clear your missed payment to prevent timeline extension.
                </div>
                """, unsafe_allow_html=True)
                
                if st.button("💳 Pay Missed Installment Now (Manual UPI/Card)", type="primary"):
                    conn = sqlite3.connect('gullakcoin_advanced.db')
                    c = conn.cursor()
                    dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    c.execute('INSERT INTO transactions (username, trans_type, category, amount, status, date) VALUES (?, ?, ?, ?, ?, ?)', 
                              (username, 'Income', 'Investment', active_plan['installment_amt'], 'Success', dt))
                    conn.commit()
                    conn.close()
                    st.success("✅ Missed installment cleared successfully! Your cycle is back on track.")
                    time.sleep(2)
                    st.rerun()

            p_col1, p_col2, p_col3 = st.columns(3)
            with p_col1: st.info(f"**Active Plan:** {active_plan['plan_name']}")
            with p_col2: st.info(f"**Target Principal:** ₹ {active_plan['target_amount']:,.0f}")
            with p_col3: st.info(f"**Frequency:** {active_plan['frequency']}")
                
            st.progress(min(portfolio_value / target_value, 1.0))
            st.write(f"Accumulated via AutoPay: **₹ {portfolio_value:,.2f}** out of ₹ {target_value:,.0f}")
            st.markdown("---")
            
            start_date = pd.to_datetime(active_plan['date'])
            completion_date = start_date + pd.Timedelta(days=90)
            withdrawal_date = completion_date + pd.Timedelta(days=30)
            current_time = pd.Timestamp.now()
            
            is_target_completed = portfolio_value >= target_value
            is_lockin_passed = current_time >= withdrawal_date
            
            st.subheader("Maturity & Redemption Portal")
            
            if not is_target_completed:
                st.markdown(f"""
                <div class="locked-box">
                    <h3 style="color: #b45309; margin-bottom: 5px;">🔒 Maturity & Withdrawal Locked</h3>
                    <p style="color: #78350f; font-size: 14px;">Your SIP deductions are ongoing. Withdrawals remain strictly locked until your <b>Target Principal of ₹ {target_value:,.0f}</b> is fully accumulated.</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                if "Verified" not in kyc_status:
                    st.error("🚨 Withdrawal Blocked: Your Bank Details & KYC Verification is Pending/Mismatch. Please go to 'Profile & KYC' to complete verification with your registered mobile number.")
                else:
                    w_col1, w_col2 = st.columns(2)
                    with w_col1:
                        st.success("✅ Target 100% Achieved & Bank Verified!")
                        st.write(f"📅 **Target Completion Date:** {completion_date.strftime('%d %B %Y')}")
                        st.write(f"🔓 **Redemption Unlock Date:** {withdrawal_date.strftime('%d %B %Y')}")
                        
                    with w_col2:
                        maturity, fee, gst, net_payout, net_profit, _ = calculate_payout(target_value, active_plan['frequency'])
                        st.metric("Achieved Maturity Value", f"₹ {maturity:,.2f}")
                        
                        if not is_lockin_passed:
                            st.warning(f"⏳ Withdrawal unlocks on {withdrawal_date.strftime('%d %B %Y')} (1-month hold period active).")
                            st.button("Initiate Withdrawal Request", disabled=True, use_container_width=True)
                        else:
                            if st.button("Initiate Withdrawal Request", type="primary", use_container_width=True):
                                st.success("✅ Redemption request queued successfully for bank transfer.")
                                st.code(f"""
Gross Maturity Amount : ₹ {maturity:,.2f}
- Processing Fee (2%) : ₹ {fee:,.2f}
- GST on Fee (18%)    : ₹ {gst:,.2f}
-----------------------------------
Net Bank Credit       : ₹ {net_payout:,.2f}
Estimated Net Gain    : ₹ {net_profit:,.2f}
                                """)
        else:
            st.warning("No active capital allocations found. Explore product offerings to initiate a plan.")

    elif menu == "📝 Transaction History":
        st.subheader("Automated E-Mandate Audit Logs")
        
        if not df_sub.empty:
            with st.expander("🛠️ Developer Sandbox: Simulate E-Mandate Failure"):
                if st.button("Simulate Insufficient Balance (Fail Next Installment)", type="secondary"):
                    active_inst = df_sub.iloc[0]['installment_amt']
                    log_failed_transaction(username, active_inst)
                    st.warning("⚠️ Simulated E-Mandate failure recorded! Check 'My Portfolio'.")
                    time.sleep(1)
                    st.rerun()

        if not df_tx.empty: 
            st.dataframe(df_tx[['date', 'trans_type', 'category', 'amount', 'status']].sort_values(by='date', ascending=False), use_container_width=True, hide_index=True)
        else:
            st.info("No ledger entries found.")

    elif menu == "👤 Profile & KYC":
        st.subheader("User Profile & KYC Verification")
        st.markdown(f"""
        * **Registered Account / Mobile:** `{username}`
        * **Permanent Investor ID:** `👤 {investor_id}`
        * **Current KYC & Bank Status:** **{kyc_status}**
        """)
        st.markdown("---")
        
        st.subheader("Update PAN, Aadhaar & Bank Details")
        st.markdown("<p style='font-size: 13px; color: #4b5563;'><b>Rule:</b> Bank Account verification requires your bank registered mobile number to match your login mobile number (<b>" + username + "</b>) for automatic approval. Otherwise KYC remains Pending.</p>", unsafe_allow_html=True)
        
        with st.form("kyc_form"):
            new_pan = st.text_input("PAN Card Number", value=pan_num, placeholder="ABCDE1234F")
            new_aadhar = st.text_input("Aadhaar Card Number", value=aadhar_num, placeholder="12 Digit Aadhaar Number")
            new_bank = st.text_input("Bank Account Number", value=bank_acc, placeholder="Enter Bank Account Number")
            new_ifsc = st.text_input("IFSC Code", value=ifsc_code, placeholder="SBIN000XXXX")
            new_branch = st.text_input("Branch Name", value=branch_name, placeholder="Main Branch City")
            new_bmobile = st.text_input("Bank Registered Mobile Number", value=bank_mobile, placeholder="Must match login mobile")
            
            submit_kyc = st.form_submit_button("Submit KYC & Bank Details for Verification", type="primary")
            
            if submit_kyc:
                if new_pan and new_aadhar and new_bank and new_ifsc and new_branch and new_bmobile:
                    res_status = update_kyc(username, new_pan, new_aadhar, new_bank, new_ifsc, new_branch, new_bmobile)
                    if "Verified" in res_status:
                        st.success("✅ Bank details & KYC verified successfully! Account Approved.")
                    else:
                        st.warning("⚠️ KYC updated as Pending. Bank registered mobile number must match your login mobile number for approval.")
                    time.sleep(2)
                    st.rerun()
                else:
                    st.warning("Please fill in all KYC and banking fields completely.")

    elif menu == "💬 Support & Help":
        st.subheader("Customer Support & Assistance")
        st.write("We are here to help you 24/7 with your investments and E-Mandates.")
        st.write("")
        
        s_col1, s_col2, s_col3 = st.columns(3)
        with s_col1:
            st.markdown("""
            <div class="support-card">
                <h3>💬 WhatsApp Support</h3>
                <p style="color: #4b5563; font-size: 13px;">Instant chat assistance with our executive.</p>
                <a href="https://wa.me/919876543210" target="_blank"><button style="background-color: #25D366; color: white; border: none; padding: 10px 20px; border-radius: 8px; font-weight: bold; cursor: pointer;">Chat on WhatsApp</button></a>
            </div>
            """, unsafe_allow_html=True)
            
        with s_col2:
            st.markdown("""
            <div class="support-card">
                <h3>🤖 Telegram Bot</h3>
                <p style="color: #4b5563; font-size: 13px;">Get automated updates via our Telegram Bot.</p>
                <a href="https://t.me/GullakCoinSupportBot" target="_blank"><button style="background-color: #0088cc; color: white; border: none; padding: 10px 20px; border-radius: 8px; font-weight: bold; cursor: pointer;">Join Telegram Bot</button></a>
            </div>
            """, unsafe_allow_html=True)
            
        with s_col3:
            st.markdown("""
            <div class="support-card">
                <h3>📧 Email Support</h3>
                <p style="color: #4b5563; font-size: 13px;">Write to us at support@gullakcoin.pro</p>
                <a href="mailto:support@gullakcoin.pro"><button style="background-color: #059669; color: white; border: none; padding: 10px 20px; border-radius: 8px; font-weight: bold; cursor: pointer;">Send Email</button></a>
            </div>
            """, unsafe_allow_html=True)

    elif menu == "❓ FAQs":
        st.subheader("Frequently Asked Questions")
        with st.expander("Q: What is the AI Yield Predictor & Streak Tracker?"):
            st.write("A: Our AI system tracks your AutoPay discipline. Maintaining consistent successful installments increases your streak counter and qualifies your portfolio for AI-modeled yield bonuses and investor badges.")
        with st.expander("Q: What is my Investor ID and how is it generated?"):
            st.write("A: Your Investor ID (e.g., GC-PRO-XXXXXX) is a unique permanent identifier generated automatically upon account registration.")
        with st.expander("Q: Why should I lock my funds for 4 months instead of a Bank FD?"):
            st.write("A: Unlike traditional bank FDs yielding 3-7% p.a., GullakCoin Pro's structured 120-day milestone model targets significantly higher net returns through startup allocations.")
        with st.expander("Q: What happens if my E-Mandate fails due to insufficient balance?"):
            st.write("A: You receive a 5-day grace period to clear your installment manually via UPI/Card in your 'My Portfolio' tab.")
