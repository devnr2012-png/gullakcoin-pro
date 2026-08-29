import datetime
import random
import sqlite3
import time
import urllib.parse
import pandas as pd
import requests
import streamlit as st

# --- PAGE SETUP ---
st.set_page_config(page_title="GullakCoin Pro", page_icon="🪙", layout="wide")

# --- MOCK PAYMENT GATEWAY CONFIGURATION (TEST MODE) ---
CASHFREE_APP_ID = "TEST_APP_ID_MOCK"
CASHFREE_SECRET_KEY = "TEST_SECRET_KEY_MOCK"
CASHFREE_ENV = "TEST"
TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
TELEGRAM_CHAT_ID = "YOUR_TELEGRAM_CHAT_ID"

# --- TWILIO SMS API CONFIGURATION ---
TWILIO_ACCOUNT_SID = "AC6ee8959f0b00dd9d5b8648baeddda119"
TWILIO_API_KEY_SID = "SK051e4ca445f1469c93174d5f794a0089"
TWILIO_API_SECRET = "LTMfWNFvjS60bethokwAvmAdleQvgS0I"
TWILIO_PHONE_NUMBER = "+17372212163"

# --- OWNER CONTACT CONFIGURATION ---
MY_WHATSAPP_NUMBER = "919140046797"
MY_TELEGRAM_USERNAME = "9140046797"
MY_EMAIL = "devnr2012@gmail.com"


# --- CUSTOM CSS ---
st.markdown(
    """
<style>
    .stApp { 
        background: linear-gradient(135deg, #061a14 0%, #0d281e 50%, #02100a 100%); 
        color: #f8fafc; 
        font-family: 'Inter', sans-serif; 
    }
    [data-testid="stSidebar"] { background-color: #04120e; border-right: 1px solid #064e3b; }
    [data-testid="stSidebar"] * { color: #f8fafc !important; }
    
    [data-testid="stMetricValue"] { 
        font-size: 30px !important; 
        color: #38bdf8 !important; 
        font-weight: 900 !important; 
        text-shadow: 0 0 12px rgba(56, 189, 248, 0.4); 
    }
    [data-testid="stMetricLabel"] {
        color: #93c5fd !important;
        font-size: 15px !important;
        font-weight: 700 !important;
    }
    
    [data-testid="stSidebar"] code {
        background: linear-gradient(135deg, #34d399, #059669) !important;
        color: #061a14 !important;
        font-weight: 900 !important;
        padding: 4px 8px !important;
        border-radius: 6px !important;
        border: 1px solid #6ee7b7 !important;
    }
    
    [data-testid="stSidebar"] .stButton button {
        background: linear-gradient(135deg, #f43f5e, #be123c) !important;
        color: #ffffff !important;
        font-weight: 900 !important;
        border: 1px solid #fda4af !important;
        border-radius: 10px !important;
        box-shadow: 0 6px 20px rgba(244, 63, 94, 0.4) !important;
    }
    
    .stButton button {
        background: linear-gradient(135deg, #34d399, #059669) !important;
        color: #061a14 !important;
        font-weight: 800 !important;
        border: 1px solid #6ee7b7 !important;
        border-radius: 10px !important;
        box-shadow: 0 4px 15px rgba(52, 211, 153, 0.3) !important;
    }
    .stButton button:hover {
        background: linear-gradient(135deg, #6ee7b7, #10b981) !important;
        color: #02100a !important;
    }
    
    .stTextInput label, .stSelectbox label {
        color: #34d399 !important;
        font-weight: 700 !important;
        font-size: 14px !important;
    }
    
    .stTextInput input, .stSelectbox select {
        background-color: #0b2920 !important; 
        color: #38bdf8 !important; 
        border: 1px solid #059669 !important; 
        border-radius: 8px; 
        font-weight: 600;
    }
    
    [data-testid="stChatInput"] textarea {
        color: #38bdf8 !important;
        background-color: #0b2920 !important;
        font-weight: 600;
    }
    [data-testid="stChatInput"] {
        background-color: #0b2920 !important;
        border: 1px solid #34d399 !important;
        border-radius: 12px;
    }
    
    [data-testid="stChatMessage"] * {
        color: #ffffff !important;
    }
    
    /* Permanent Fix: Hide empty containers */
    .element-container:empty, div[data-testid="stVerticalBlock"] > div:empty {
        display: none !important;
    }
    
    /* Make Radio / Auth Mode text pure White */
    div[row-widget="stRadio"] label p, .stRadio label p {
        color: #ffffff !important;
        font-weight: 800 !important;
        font-size: 15px !important;
    }
    
    .auth-container .stButton button[kind="primary"], .auth-container .stButton button {
        background: linear-gradient(135deg, #a7f3d0, #6ee7b7) !important;
        color: #1e3a8a !important;
        font-weight: 800 !important;
        border: 1px solid #34d399 !important;
        border-radius: 10px !important;
        box-shadow: 0 6px 20px rgba(110, 231, 183, 0.3) !important;
    }

    .auth-container {
        background: rgba(11, 41, 32, 0.92);
        backdrop-filter: blur(16px);
        padding: 30px 35px; 
        border-radius: 20px; 
        border: 2px solid #34d399;
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.7); 
        width: 100%; 
    }
    
    .left-hero-panel {
        padding: 40px 20px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        height: 100%;
    }
    
    .growth-stage-banner {
        background: linear-gradient(135deg, #0b2920, #042f22);
        border: 1px solid #34d399;
        padding: 16px 20px;
        border-radius: 14px;
        text-align: center;
        margin-top: 20px;
        box-shadow: 0 8px 25px rgba(52, 211, 153, 0.25);
    }
    .growth-stages {
        display: flex;
        justify-content: space-around;
        align-items: center;
        font-size: 24px;
        color: #34d399;
        font-weight: bold;
    }
    .growth-label {
        font-size: 12px;
        color: #93c5fd;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-top: 6px;
        font-weight: 700;
    }

    .logo-container { text-align: center; margin-bottom: 15px; }
    .logo-badge {
        display: inline-block; 
        background: linear-gradient(135deg, #34d399, #059669); 
        color: #061a14;
        font-weight: 900; 
        font-size: 28px; 
        padding: 12px 24px; 
        border-radius: 16px;
        box-shadow: 0 10px 25px rgba(52, 211, 153, 0.4); 
        letter-spacing: 1.5px;
    }
    .brand-title { font-size: 28px; font-weight: 900; color: #ffffff; margin-top: 12px; }
    .brand-tagline { font-size: 13px; color: #34d399; margin-top: 4px; font-style: italic; font-weight: 700; }
    
    .plan-card {
        background-color: #0b2920; padding: 25px; border-radius: 16px; border: 1px solid #047857;
        height: 230px; display: flex; flex-direction: column; justify-content: flex-start; margin-bottom: 12px;
    }
    .calc-card {
        background-color: rgba(5, 150, 105, 0.12); padding: 20px; border-radius: 14px; border: 1px solid #34d399;
        margin-top: 15px; margin-bottom: 15px;
    }
    .gateway-inline-box {
        background: rgba(11, 41, 32, 0.98);
        border: 2px solid #38bdf8;
        padding: 25px;
        border-radius: 16px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.8);
        margin-top: 20px;
        margin-bottom: 20px;
    }
    .plan-title { font-size: 22px; font-weight: 800; margin-bottom: 10px; color: #ffffff;}
    .plan-desc { font-size: 13px; color: #cbd5e1; margin-bottom: 15px; line-height: 1.6; }
    .plan-target { font-size: 20px; font-weight: 800; color: #34d399; margin-top: auto; }
    .disclaimer { font-size: 11px; color: #f87171; font-style: italic; }
    .locked-box {
        background-color: #1c1917; border: 1px solid #fbbf24; padding: 20px; border-radius: 12px; text-align: center; margin-top: 20px; color: #fef3c7;
    }
    .strict-rule-box {
        background-color: rgba(239, 68, 68, 0.15); border: 1px solid #ef4444; padding: 16px; border-radius: 10px; color: #fca5a5; font-size: 13px; margin-bottom: 20px;
    }
    .comparison-box {
        background-color: rgba(5, 150, 105, 0.15); border: 1px solid #34d399; padding: 16px; border-radius: 10px; color: #e2e8f0; font-size: 13px; margin-bottom: 20px;
    }
    .alert-failed {
        background-color: rgba(239, 68, 68, 0.2); border: 1px solid #ef4444; padding: 16px; border-radius: 10px; color: #fca5a5; margin-bottom: 15px;
    }
    .support-card {
        background-color: #0b2920; padding: 22px; border-radius: 14px; border: 1px solid #047857; text-align: center;
    }
    .gamification-box {
        background: linear-gradient(135deg, rgba(251, 191, 36, 0.12), rgba(5, 150, 105, 0.2));
        border: 1px solid #fbbf24; padding: 22px; border-radius: 16px; margin-bottom: 20px; color: #f8fafc;
    }
    .autopilot-box {
        background: linear-gradient(135deg, rgba(56, 189, 248, 0.12), rgba(5, 150, 105, 0.25));
        border: 1px solid #38bdf8; padding: 22px; border-radius: 16px; margin-bottom: 20px; color: #f8fafc;
    }
</style>
""",
    unsafe_allow_html=True,
)


# --- MICRO-PLUGINS (INLINE ARCHITECTURE) ---
class GamificationPlugin:

  @staticmethod
  def render_widget(df_tx):
    success_count = (
        len(df_tx[df_tx["status"] == "Success"]) if not df_tx.empty else 0
    )
    streak_days = success_count * 3
    badge_level = (
        "🔥 Gold Investor Streak"
        if success_count >= 3
        else "🌱 Silver Streak (Build up to unlock +1% Yield Boost)"
    )
    st.markdown(
        f"""
            <div class="gamification-box">
                <h4 style="color: #fbbf24; margin-top:0;">🤖 AI Yield Predictor & Gamification Plugin</h4>
                <p style="margin-bottom: 5px;"><b>Active Streak:</b> {streak_days} Days Consistent AutoPay</p>
                <p style="margin-bottom: 5px;"><b>Investor Status Badge:</b> {badge_level}</p>
                <p style="font-size: 12px; color: #cbd5e1; margin-bottom:0;">Modular plugin architecture active.</p>
            </div>
            """,
        unsafe_allow_html=True,
    )


class RiskAgentPlugin:

  @staticmethod
  def evaluate_query(query):
    q = query.lower()
    if any(k in q for k in ["fail", "payment fail", "insufficient"]):
      return (
          "⚠️ **Failed E-Mandate Resolution (Risk Plugin Agent)**: If an"
          " installment fails due to insufficient bank balance, a **5-day grace"
          " period** becomes active. Clear missed installments manually using"
          " UPI/Card."
      )
    return None


class MasterAutopilotAgent:

  @staticmethod
  def run_autopilot_routine(username, df_sub, kyc_status):
    actions_taken = []
    conn = sqlite3.connect("gullakcoin_advanced.db")
    df_tx = pd.read_sql_query(
        f"SELECT * FROM transactions WHERE username='{username}'", conn
    )
    conn.close()

    if not df_tx.empty:
      failed_count = len(
          df_tx[df_tx["status"] == "Failed (Insufficient Balance)"]
      )
      if failed_count > 0 and not df_sub.empty:
        plan_name = df_sub.iloc[0]["plan_name"]
        inst_amt = df_sub.iloc[0]["installment_amt"]
        conn = sqlite3.connect("gullakcoin_advanced.db")
        c = conn.cursor()
        dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c.execute(
            "INSERT INTO transactions (username, trans_type, category, amount,"
            " status, plan_ref, date) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (username, "Income", "Investment", inst_amt, "Success", plan_name, dt),
        )
        conn.commit()
        conn.close()
        actions_taken.append(
            f"⚡ **Auto-Healed Failed SIP ({plan_name})**: Automatically cleared"
            f" ₹ {inst_amt:,.2f} using backup liquidity reserve."
        )

    if "Pending" in kyc_status:
      actions_taken.append(
          "🛡️ **Compliance Guard**: KYC status is pending. Ensure bank"
          " mobile matches login ID for auto-approval."
      )
    else:
      actions_taken.append(
          "🛡️ **Compliance Guard**: KYC is 100% Verified & Approved."
      )

    success_count = (
        len(df_tx[df_tx["status"] == "Success"]) if not df_tx.empty else 0
    )
    if success_count >= 3:
      actions_taken.append(
          "🔥 **Yield Maximizer**: Gold Investor Streak active! +1.0% AI"
          " Yield Boost automatically applied across all active plans."
      )
    else:
      actions_taken.append(
          "🌱 **Yield Optimizer**: Maintain consistent deductions to unlock"
          " the +1.0% AI Yield Boost."
      )

    return actions_taken


# --- DATABASE SETUP ---
def init_db():
  conn = sqlite3.connect("gullakcoin_advanced.db")
  c = conn.cursor()
  c.execute(
      """CREATE TABLE IF NOT EXISTS users (
                 id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT, investor_id TEXT, kyc_status TEXT, pan TEXT, aadhar TEXT, bank_acc TEXT, ifsc TEXT, branch TEXT, bank_mobile TEXT)"""
  )

  existing_cols = [
      col[1] for col in c.execute("PRAGMA table_info(users)").fetchall()
  ]
  if "aadhar" not in existing_cols:
    c.execute("ALTER TABLE users ADD COLUMN aadhar TEXT")
  if "ifsc" not in existing_cols:
    c.execute("ALTER TABLE users ADD COLUMN ifsc TEXT")
  if "branch" not in existing_cols:
    c.execute("ALTER TABLE users ADD COLUMN branch TEXT")
  if "bank_mobile" not in existing_cols:
    c.execute("ALTER TABLE users ADD COLUMN bank_mobile TEXT")

  c.execute(
      """CREATE TABLE IF NOT EXISTS transactions (
                 id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, trans_type TEXT, category TEXT, amount REAL, status TEXT, plan_ref TEXT, date TEXT)"""
  )
  tx_cols = [
      col[1] for col in c.execute("PRAGMA table_info(transactions)").fetchall()
  ]
  if "plan_ref" not in tx_cols:
    c.execute("ALTER TABLE transactions ADD COLUMN plan_ref TEXT")

  c.execute(
      """CREATE TABLE IF NOT EXISTS subscriptions (
                 id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, plan_name TEXT, target_amount INTEGER, frequency TEXT, installment_amt REAL, date TEXT)"""
  )
  conn.commit()
  conn.close()


def send_telegram_alert(message):
  if TELEGRAM_BOT_TOKEN == "YOUR_TELEGRAM_BOT_TOKEN":
    return
  url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
  payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
  try:
    requests.post(url, json=payload, timeout=3)
  except Exception:
    pass


def get_user_profile(username):
  conn = sqlite3.connect("gullakcoin_advanced.db")
  c = conn.cursor()
  c.execute(
      "SELECT investor_id, kyc_status, pan, aadhar, bank_acc, ifsc, branch,"
      " bank_mobile FROM users WHERE username=?",
      (username,),
  )
  res = c.fetchone()
  conn.close()
  return res


def update_kyc(
    username, pan, aadhar, bank_acc, ifsc, branch, bank_mobile
):
  conn = sqlite3.connect("gullakcoin_advanced.db")
  c = conn.cursor()
  kyc_status = (
      "Verified (Approved)"
      if bank_mobile.strip() == username.strip()
      else "Pending (Mobile Mismatch)"
  )
  c.execute(
      "UPDATE users SET pan=?, aadhar=?, bank_acc=?, ifsc=?, branch=?,"
      " bank_mobile=?, kyc_status=? WHERE username=?",
      (
          pan,
          aadhar,
          bank_acc,
          ifsc,
          branch,
          bank_mobile,
          kyc_status,
          username,
      ),
  )
  conn.commit()
  conn.close()
  return kyc_status


def update_password(username, new_pass):
  conn = sqlite3.connect("gullakcoin_advanced.db")
  c = conn.cursor()
  c.execute(
      "UPDATE users SET password=? WHERE username=?", (new_pass, username)
  )
  conn.commit()
  conn.close()


def get_data(username):
  conn = sqlite3.connect("gullakcoin_advanced.db")
  df_tx = pd.read_sql_query(
      f"SELECT * FROM transactions WHERE username='{username}'", conn
  )
  df_sub = pd.read_sql_query(
      f"SELECT * FROM subscriptions WHERE username='{username}'", conn
  )
  conn.close()
  return df_tx, df_sub


def add_subscription(
    username, plan_name, target_amount, frequency_text, installment_amt
):
  conn = sqlite3.connect("gullakcoin_advanced.db")
  c = conn.cursor()
  dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  c.execute(
      "INSERT INTO subscriptions (username, plan_name, target_amount,"
      " frequency, installment_amt, date) VALUES (?, ?, ?, ?, ?, ?)",
      (
          username,
          plan_name,
          target_amount,
          frequency_text,
          installment_amt,
          dt,
      ),
  )
  c.execute(
      "INSERT INTO transactions (username, trans_type, category, amount,"
      " status, plan_ref, date) VALUES (?, ?, ?, ?, ?, ?, ?)",
      (
          username,
          "Income",
          "Investment",
          installment_amt,
          "Success",
          plan_name,
          dt,
      ),
  )
  conn.commit()
  conn.close()
  send_telegram_alert(
      f"🚀 New E-Mandate Alert: {username} subscribed to {plan_name} via"
      f" {frequency_text} SIP (Amt: ₹{installment_amt:,.2f})"
  )


def log_withdrawal_request(username, plan_name, amount, status):
  conn = sqlite3.connect("gullakcoin_advanced.db")
  c = conn.cursor()
  dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  c.execute(
      "INSERT INTO transactions (username, trans_type, category, amount,"
      " status, plan_ref, date) VALUES (?, ?, ?, ?, ?, ?, ?)",
      (username, "Withdrawal", "Redemption", amount, status, plan_name, dt),
  )
  conn.commit()
  conn.close()


def log_failed_transaction(username, plan_name, installment_amt):
  conn = sqlite3.connect("gullakcoin_advanced.db")
  c = conn.cursor()
  dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  c.execute(
      "INSERT INTO transactions (username, trans_type, category, amount,"
      " status, plan_ref, date) VALUES (?, ?, ?, ?, ?, ?, ?)",
      (
          username,
          "Expense",
          "Failed SIP",
          installment_amt,
          "Failed (Insufficient Balance)",
          plan_name,
          dt,
      ),
  )
  conn.commit()
  conn.close()


# --- TEXT REPORT GENERATOR ---
def generate_text_summary(username, investor_id, kyc_status, df_sub, df_tx):
  report = []
  report.append("==================================================")
  report.append("      GULLAKCOIN PRO - STATEMENT OF ACCOUNT")
  report.append("==================================================")
  report.append(f"Investor Account ID : {investor_id}")
  report.append(f"Registered User/Mob : {username}")
  report.append(f"KYC & Bank Status   : {kyc_status}")
  report.append(
      f"Report Generated On : {datetime.datetime.now().strftime('%d %B %Y, %H:%M')}"
  )
  report.append("--------------------------------------------------\n")

  report.append("ACTIVE PORTFOLIO PLANS & E-MANDATE SCHEDULE:")
  report.append("--------------------------------------------------")
  if not df_sub.empty:
    for _, row in df_sub.iterrows():
      start_dt = pd.to_datetime(row["date"])
      comp_dt = start_dt + pd.Timedelta(days=90)
      w_dt = comp_dt + pd.Timedelta(days=30)
      report.append(f"• Plan Name       : {row['plan_name']}")
      report.append(f"  Frequency       : {row['frequency']}")
      report.append(f"  Target Principal: Rs {row['target_amount']:,.0f}")
      report.append(f"  Installment     : Rs {row['installment_amt']:,.2f}")
      report.append(f"  Maturity Date   : {comp_dt.strftime('%d-%m-%Y')}")
      report.append(f"  Withdrawal Date : {w_dt.strftime('%d-%m-%Y')}")
      report.append("")
  else:
    report.append("No active portfolio subscriptions found.\n")

  report.append("--------------------------------------------------")
  report.append("TRANSACTION LEDGER & E-MANDATE HIT HISTORY:")
  report.append("--------------------------------------------------")
  if not df_tx.empty:
    for _, row in df_tx.iterrows():
      p_ref = (
          str(row["plan_ref"]) if pd.notnull(row["plan_ref"]) else "General"
      )
      report.append(
          f"[{row['date']}] | Plan: {p_ref} | Type: {row['trans_type']}"
          f" ({row['category']}) | Amt: Rs {row['amount']:,.2f} | Status:"
          f" {row['status']}"
      )
  else:
    report.append("No transaction records found.")

  report.append("\n==================================================")
  report.append("        End of Certified Statement of Account")
  report.append("==================================================")
  return "\n".join(report)


init_db()

# --- SESSION STATE ---
if "logged_in" not in st.session_state:
  st.session_state.logged_in = False
if "current_user" not in st.session_state:
  st.session_state.current_user = ""
if "forgot_user" not in st.session_state:
  st.session_state.forgot_user = ""
if "selected_plan" not in st.session_state:
  st.session_state.selected_plan = None
if "pending_checkout" not in st.session_state:
  st.session_state.pending_checkout = None

# --- AUTHENTICATION SCREEN ---
if not st.session_state.logged_in:
  col_left, col_right = st.columns([1.1, 1.1], gap="large")

  with col_left:
    st.markdown(
        """
        <div class="left-hero-panel">
            <h1 style="color: #ffffff; font-size: 42px; font-weight: 900; line-height: 1.2; margin-bottom: 10px;">
                Nurturing Wealth <br><span style="color: #34d399;">Across Generations</span>
            </h1>
            <p style="color: #cbd5e1; font-size: 16px; line-height: 1.6; margin-bottom: 25px;">
                GullakCoin Pro is a next-generation structured milestone wealth platform. Watch your small savings grow from a delicate seedling into a majestic financial tree through multi-plan automated startup allocations.
            </p>
            <div class="growth-stage-banner" style="text-align: left; padding: 20px;">
                <div class="growth-stages" style="justify-content: flex-start; gap: 20px;">
                    <span>🌱 Seedling</span> ➔ <span>🌿 Growth</span> ➔ <span>🌳 Plus</span> ➔ <span>🌲 Superplus</span>
                </div>
                <div class="growth-label" style="text-align: left; margin-top: 8px;">Automated Multi-Plan 120-Day Wealth Cycles</div>
            </div>
        </div>
    """,
        unsafe_allow_html=True,
    )

  with col_right:
    st.markdown("<div class='auth-container'>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class="logo-container">
            <div class="logo-badge"><span style="font-size: 24px; vertical-align: middle;">🌱</span> GC</div>
            <div class="brand-title">GullakCoin Pro</div>
            <div class="brand-tagline">“Nurturing Your Wealth, From a Seedling to a Grand Tree.”</div>
        </div>
    """,
        unsafe_allow_html=True,
    )

    auth_mode = st.radio(
        "", ["Secure Login", "Create Account", "🔑 Forgot Password"], horizontal=True
    )
    st.write("")

    if auth_mode == "Secure Login":
      l_user = st.text_input("Registered Email or Mobile Number", key="l_user")
      l_pass = st.text_input("Secure Password", type="password", key="l_pass")
      use_biometric = st.checkbox(
          "🔑 Quick Login via Device Passkey / Biometric Simulator"
      )
      st.write("")

      if st.button(
          "Login to Dashboard", use_container_width=True, type="primary"
      ):
        conn = sqlite3.connect("gullakcoin_advanced.db")
        c = conn.cursor()
        c.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (l_user, l_pass),
        )
        user_exists = c.fetchone()
        conn.close()

        if use_biometric and l_user:
          st.session_state.logged_in = True
          st.session_state.current_user = l_user
          st.success("🔓 Biometric Passkey Verified Successfully!")
          time.sleep(1)
          st.rerun()
        elif user_exists:
          st.session_state.logged_in = True
          st.session_state.current_user = l_user
          st.success("✅ Login Successful! Redirecting...")
          time.sleep(1)
          st.rerun()
        else:
          st.error("Invalid credentials or user does not exist.")

    elif auth_mode == "Create Account":
      s_user = st.text_input("Email or Mobile Number", key="s_user")
      s_pass = st.text_input(
          "Create Secure Password", type="password", key="s_pass"
      )
      st.write("")

      if st.button("Register Account", use_container_width=True):
        if s_user and s_pass:
          conn = sqlite3.connect("gullakcoin_advanced.db")
          c = conn.cursor()
          c.execute("SELECT * FROM users WHERE username=?", (s_user,))
          if c.fetchone():
            st.error("Account already exists.")
          else:
            investor_id = f"GC-PRO-{random.randint(100000, 999900)}"
            c.execute(
                "INSERT INTO users (username, password, investor_id,"
                " kyc_status, pan, aadhar, bank_acc, ifsc, branch, bank_mobile)"
                " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    s_user,
                    s_pass,
                    investor_id,
                    "Pending",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                ),
            )
            conn.commit()
            conn.close()
            st.success(
                f"🎉 Account created successfully! Your Investor ID is"
                f" {investor_id}. Please switch to Secure Login."
            )
          conn.close()
        else:
          st.warning("Please fill in all fields.")

    elif auth_mode == "🔑 Forgot Password":
      f_user = st.text_input(
          "Enter Your Registered Email or Mobile Number", key="f_user"
      )
      new_pass_1 = st.text_input("New Password", type="password", key="n_pass1")
      new_pass_2 = st.text_input(
          "Confirm New Password", type="password", key="n_pass2"
      )
      st.write("")

      if st.button(
          "Reset Password & Save", type="primary", use_container_width=True
      ):
        if f_user:
          conn = sqlite3.connect("gullakcoin_advanced.db")
          c = conn.cursor()
          c.execute("SELECT * FROM users WHERE username=?", (f_user,))
          user_record = c.fetchone()
          conn.close()

          if user_record:
            if new_pass_1 and new_pass_1 == new_pass_2:
              update_password(f_user, new_pass_1)
              st.success(
                  "🎉 Password updated successfully! Please switch to Secure"
                  " Login."
              )
            else:
              st.error("Passwords do not match or empty.")
          else:
            st.error("Account not found with this mobile number/email.")
        else:
          st.warning("Please enter your registered number or email.")

    st.markdown("</div>", unsafe_allow_html=True)

# --- MAIN DASHBOARD ---
else:
  username = st.session_state.current_user
  user_prof = get_user_profile(username)
  investor_id = (
      user_prof[0] if user_prof and user_prof[0] else "GC-PRO-PENDING"
  )
  kyc_status = user_prof[1] if user_prof else "Pending"
  pan_num = user_prof[2] if user_prof else ""
  aadhar_num = user_prof[3] if user_prof else ""
  bank_acc = user_prof[4] if user_prof else ""
  ifsc_code = user_prof[5] if user_prof else ""
  branch_name = user_prof[6] if user_prof else ""
  bank_mobile = user_prof[7] if user_prof else ""

  df_tx, df_sub = get_data(username)

  portfolio_value = (
      df_tx[
          (df_tx["category"] == "Investment")
          & (df_tx["trans_type"] == "Income")
          & (df_tx["status"] == "Success")
      ]["amount"].sum()
      if not df_tx.empty
      else 0
  )

  total_target_value = (
      df_sub["target_amount"].sum() if not df_sub.empty else 0
  )
  balance_target = max(total_target_value - portfolio_value, 0)

  active_sub_count = 0
  if not df_sub.empty:
    for _, s_row in df_sub.iterrows():
      s_name = s_row["plan_name"]
      s_target = s_row["target_amount"]
      s_contrib = (
          df_tx[
              (df_tx["plan_ref"] == s_name)
              & (df_tx["category"] == "Investment")
              & (df_tx["status"] == "Success")
          ]["amount"].sum()
          if not df_tx.empty
          else 0
      )
      if s_contrib < s_target:
        active_sub_count += 1


  def calculate_payout(target, freq):
    if "Daily" in freq:
      roi = 0.08
    elif "Weekly" in freq:
      roi = 0.10
    else:
      roi = 0.18

    success_tx_count = (
        len(df_tx[df_tx["status"] == "Success"]) if not df_tx.empty else 0
    )
    streak_bonus = 0.01 if success_tx_count >= 3 else 0.0
    effective_roi = roi + streak_bonus
    maturity = target + (target * effective_roi)
    fee = maturity * 0.02
    gst = fee * 0.18
    net_payout = maturity - fee - gst
    net_profit = net_payout - target
    return maturity, fee, gst, net_payout, net_profit, streak_bonus


  def calculate_detailed_metrics(target, freq):
    if "Daily" in freq:
      roi = 0.08
      installments_count = 90
      inst_amt = target / 90
    elif "Weekly" in freq:
      roi = 0.10
      installments_count = 13
      inst_amt = (target / 90) * 7
    else:
      roi = 0.18
      installments_count = 3
      inst_amt = target / 3

    success_tx_count = (
        len(df_tx[df_tx["status"] == "Success"]) if not df_tx.empty else 0
    )
    streak_bonus = 0.01 if success_tx_count >= 3 else 0.0
    effective_roi = roi + streak_bonus

    maturity = target + (target * effective_roi)
    fee = maturity * 0.02
    gst = fee * 0.18
    net_payout = maturity - fee - gst
    net_profit = net_payout - target

    start_dt = datetime.datetime.now()
    comp_dt = start_dt + datetime.timedelta(days=90)
    w_dt = comp_dt + datetime.timedelta(days=30)

    return (
        inst_amt,
        installments_count,
        effective_roi,
        maturity,
        fee,
        gst,
        net_payout,
        net_profit,
        comp_dt,
        w_dt,
    )


  # SIDEBAR
  st.sidebar.markdown(f"**👤 {username}**")
  st.sidebar.markdown(f"🆔 `{investor_id}`")
  st.sidebar.markdown(f"🛡️ KYC: **{kyc_status}**")
  st.sidebar.markdown("---")
  st.sidebar.markdown("## 🪙 GullakCoin Pro")
  st.sidebar.markdown("INVESTOR PORTAL")

  menu = st.sidebar.radio(
      "",
      [
          "⚡ AI Master Autopilot",
          "📦 Product offerings",
          "📊 My Portfolio",
          "📝 Transaction History",
          "🤖 AI Wealth Advisor",
          "👤 Profile & KYC",
          "💬 Support & Help",
          "❓ FAQs",
      ],
  )
  st.sidebar.markdown("---")
  if st.sidebar.button("🚪 Logout", type="primary", use_container_width=True):
    st.session_state.logged_in = False
    st.session_state.current_user = ""
    st.session_state.selected_plan = None
    st.session_state.pending_checkout = None
    st.rerun()

  # HEADER METRICS
  col1, col2, col3, col4 = st.columns(4)
  with col1:
    st.metric("Total Portfolio Value", f"₹ {portfolio_value:,.2f}")
  with col2:
    st.metric("Total Target Value", f"₹ {total_target_value:,.0f}")
  with col3:
    st.metric(
        "Balance Target",
        f"🔒 ₹ {balance_target:,.2f}"
        if balance_target > 0
        else "✅ Completed",
    )
  with col4:
    st.metric("Active Subscriptions", f"{active_sub_count} Plans")

  st.markdown("---")

  # DASHBOARD CONTENT
  if menu == "⚡ AI Master Autopilot":
    st.subheader("⚡ AI Master Autopilot Agent (Fully Automated)")
    st.markdown(
        "<p style='color: #cbd5e1;'>This intelligent agent continuously"
        " monitors all active multi-plan portfolios, auto-heals failed"
        " E-Mandates, and manages compounding wealth.</p>",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="autopilot-box">
            <h4 style="color: #38bdf8; margin-top:0;">🤖 Autonomous Multi-Plan Operations Center</h4>
            <p style="margin-bottom: 5px;">Status: <b style="color: #34d399;">🟢 ACTIVE & MONITORING</b></p>
            <p style="font-size: 13px; color: #cbd5e1; margin-bottom:0;">The AI Agent executes routine compliance, transaction healing, and yield boost checks in real time.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("🚀 Run Full Autopilot Diagnostic & Optimization", type="primary"):
      with st.spinner(
          "🤖 Master AI Agent is scanning all active plans and executing"
          " automated workflows..."
      ):
        time.sleep(1.5)
        actions = MasterAutopilotAgent.run_autopilot_routine(
            username, df_sub, kyc_status
        )
      st.success("✅ Autopilot diagnostic completed successfully!")
      st.markdown("### 📋 Executed Automated Actions:")
      for action in actions:
        st.markdown(f"- {action}")

  elif menu == "📦 Product offerings":
    if st.session_state.pending_checkout is not None:
      pc = st.session_state.pending_checkout
      st.markdown(
          f"""
            <div class="gateway-inline-box">
                <h3 style="color: #38bdf8; margin-top: 0;">🏦 Secure E-Mandate Payment Gateway (Cashfree Test Node)</h3>
                <p style="color: #ffffff; font-size: 16px;"><b>Selected Plan:</b> {pc['title']}</p>
                <p style="color: #cbd5e1; font-size: 14px;"><b>Frequency:</b> {pc['freq']} | <b>Installment Amount:</b> <span style="color: #34d399; font-weight: bold;">₹ {pc['inst_amt']:,.2f}</span></p>
                <p style="color: #cbd5e1; font-size: 13px;">Authorize automated recurring e-mandate via your linked bank account (UPI / NetBanking / Debit Card).</p>
            </div>
            """,
          unsafe_allow_html=True,
      )

      gw_col1, gw_col2 = st.columns(2)
      with gw_col1:
        if st.button(
            "✅ Confirm & Authenticate E-Mandate",
            type="primary",
            use_container_width=True,
            key="confirm_mandate_btn",
        ):
          with st.spinner(
              "🔒 Securely registering E-Nach / AutoPay mandate with banking"
              " network..."
          ):
            time.sleep(1.5)
            add_subscription(
                username, pc["title"], pc["target"], pc["freq"], pc["inst_amt"]
            )
          st.success(
              f"🎉 E-Mandate successfully authorized and activated for"
              f" **{pc['title']}**!"
          )
          st.session_state.pending_checkout = None
          st.session_state.selected_plan = None
          time.sleep(2)
          st.rerun()
      with gw_col2:
        if st.button(
            "❌ Cancel Gateway",
            use_container_width=True,
            type="secondary",
            key="cancel_mandate_btn",
        ):
          st.session_state.pending_checkout = None
          st.rerun()
      st.markdown("---")

    if st.session_state.selected_plan is None:
      st.markdown("## Auto-Invest in Promising Startups.")
      st.markdown(
          "<p style='color: #cbd5e1; font-size: 16px; margin-bottom: 5px;'>Select"
          " a structured allocation plan below to view projections and E-Mandate"
          " frequencies. (Note: You cannot re-subscribe to a plan until its"
          " active EMIs are fully completed).</p>",
          unsafe_allow_html=True,
      )

      st.markdown(
          """
            <div class="comparison-box">
                <b>💡 Why choose GullakCoin Pro over traditional Bank FD / Savings Account?</b><br>
                While a standard bank savings account or short-term FD yields a nominal 3% to 7% p.a., our 4-month structured milestone model (3 Months SIP + 1 Month Hold) targets significantly higher net growth through diversified startup allocations. Lock in your funds for 120 days to unlock superior returns compared to traditional banking.
            </div>
            """,
          unsafe_allow_html=True,
      )

      st.markdown(
          "<p class='disclaimer'>*Disclaimer: All target yields are estimates"
          " based on quantitative models and carry market risks.</p>",
          unsafe_allow_html=True,
      )
      st.write("")

      plans = [
          (
              "GullakCoin Seed",
              5000,
              (
                  "Best for early-stage startup exposure with balanced"
                  " micro-tickets."
              ),
              "seed",
          ),
          (
              "GullakCoin Growth",
              25000,
              "For dynamically scaling an emerging startup portfolio.",
              "growth",
          ),
          (
              "GullakCoin Plus",
              50000,
              "Advanced access into mid-stage startup rounds.",
              "plus",
          ),
          (
              "GullakCoin Superplus",
              100000,
              "Exclusive curated high-net-worth venture allocations.",
              "superplus",
          ),
      ]

      active_plan_status = {}
      if not df_sub.empty:
        for _, sub_r in df_sub.iterrows():
          p_n = sub_r["plan_name"]
          p_t = sub_r["target_amount"]
          p_c = (
              df_tx[
                  (df_tx["plan_ref"] == p_n)
                  & (df_tx["category"] == "Investment")
                  & (df_tx["status"] == "Success")
              ]["amount"].sum()
              if not df_tx.empty
              else 0
          )
          if p_c < p_t:
            active_plan_status[p_n] = True

      cols = st.columns(4)
      for i, (title, target_amt, desc, plan_key) in enumerate(plans):
        is_running = active_plan_status.get(title, False)
        with cols[i]:
          badge_html = (
              "<span style='color: #fbbf24; font-weight: bold;'>🔒 Active"
              " (Running)</span>"
              if is_running
              else "<span style='color: #34d399;'>🟢 Available</span>"
          )
          st.markdown(
              f"""
                    <div class="plan-card">
                        <div class="plan-title">{title}</div>
                        <div class="plan-desc">{desc}</div>
                        <div style="font-size: 12px; margin-bottom: 5px;">Status: {badge_html}</div>
                        <div class="plan-target">🎯 Target: ₹ {target_amt:,.0f}</div>
                    </div>
                    """,
              unsafe_allow_html=True,
          )

          if is_running:
            st.markdown(
                "<p style='color: #94a3b8; font-size: 11px; text-align:"
                " center;'>EMIs ongoing. Cannot re-subscribe.</p>",
                unsafe_allow_html=True,
            )
          else:
            if st.button(
                f"Explore {title.split()[-1]}",
                key=f"expl_{plan_key}",
                use_container_width=True,
            ):
              st.session_state.selected_plan = {
                  "title": title,
                  "target": target_amt,
                  "desc": desc,
                  "key": plan_key,
              }
              st.rerun()
    else:
      plan = st.session_state.selected_plan
      target_amt = plan["target"]
      title = plan["title"]
      plan_key = plan["key"]

      if st.button("⬅️ Back to All Plans", key="back_to_plans_btn"):
        st.session_state.selected_plan = None
        st.rerun()

      st.markdown(
          f"<h1>{title} <span style='color: #34d399;'>| Target: ₹"
          f" {target_amt:,.0f}</span></h1>",
          unsafe_allow_html=True,
      )
      st.write(plan["desc"])

      freqs = [
          ("Daily", target_amt / 90, 0.08),
          ("Weekly", (target_amt / 90) * 7, 0.10),
          ("Monthly", target_amt / 3, 0.18),
      ]

      st.subheader("Configure AutoPay E-Mandate Frequency:")
      f_cols = st.columns(3)
      for i, (f_name, f_amt, f_roi) in enumerate(freqs):
        (
            maturity,
            fee,
            gst,
            net_payout,
            net_profit,
            bonus,
            total_installments,
        ) = calculate_payout(target_amt, f_name)
        with f_cols[i]:
          bonus_text = (
              f" (+{bonus*100:.1f}% AI Streak Bonus)" if bonus > 0 else ""
          )
          st.markdown(
              f"""
                    <div class="detail-card">
                        <h3 style='margin-bottom:0;'>{f_name} SIP</h3>
                        <p style='color: #cbd5e1;'>Deduction: <b>₹ {f_amt:,.2f}</b></p>
                        <hr style='border-color: #047857;'>
                        <p style='text-align: left; font-size: 13px; color: #f1f5f9;'>
                            <b>Target Yield Est.:</b> {f_roi*100:.0f}%{bonus_text}<br>
                            <b>Gross Maturity:</b> ₹ {maturity:,.2f}<br>
                            <span style='color: #fbbf24;'><b>Tenure:</b> 3 Months</span><br>
                            <span style='color: #fbbf24;'><b>Lock-in Period:</b> 1 Month</span><br>
                            <b>Platform Fee + GST:</b> -₹ {fee+gst:,.2f}<br><br>
                            <span style='color: #34d399; font-size: 15px;'><b>Est. Net Payout: ₹ {net_payout:,.2f}</b></span><br>
                            <span style='color: #38bdf8; font-size: 14px;'><b>Total EMIs to Deduct: {total_installments} Installments</b></span>
                        </p>
                    </div>
                    """,
              unsafe_allow_html=True,
          )
          if st.button(
              f"💳 Proceed to Payment for {f_name}",
              key=f"pay_btn_{f_name}_{plan_key}",
              type="primary",
              use_container_width=True,
          ):
            st.session_state.pending_checkout = {
                "title": title,
                "target": target_amt,
                "freq": f"{f_name} SIP",
                "inst_amt": float(f_amt),
            }
            st.rerun()

  elif menu == "📊 My Portfolio":
    st.subheader("Active Portfolios & Maturity / Withdrawal Portal")

    if not df_sub.empty:
      GamificationPlugin.render_widget(df_tx)

      for _, row in df_sub.iterrows():
        p_name = row["plan_name"]
        p_target = row["target_amount"]
        p_freq = row["frequency"]

        plan_contrib = (
            df_tx[
                (df_tx["plan_ref"] == p_name)
                & (df_tx["category"] == "Investment")
                & (df_tx["status"] == "Success")
            ]["amount"].sum()
            if not df_tx.empty
            else 0
        )

        st.markdown(f"### 🌿 Plan: {p_name}")
        st.progress(min(plan_contrib / p_target, 1.0))
        st.write(
            f"Accumulated: **₹ {plan_contrib:,.2f}** out of Target ₹"
            f" {p_target:,.0f} ({p_freq})"
        )

        start_date = pd.to_datetime(row["date"])
        completion_date = start_date + pd.Timedelta(days=90)
        withdrawal_date = completion_date + pd.Timedelta(days=30)
        current_time = pd.Timestamp.now()

        is_target_completed = plan_contrib >= p_target
        is_kyc_verified = "Verified" in kyc_status
        is_lockin_passed = current_time >= withdrawal_date

        if not is_target_completed:
          st.markdown(
              "<p style='color: #fbbf24; font-size: 13px;'>🔒 <b>Maturity &"
              " Withdrawal Locked:</b> E-Mandate SIP installments are ongoing"
              " until target principal is 100% achieved.</p>",
              unsafe_allow_html=True,
          )
        else:
          st.success(
              f"✅ Target 100% Achieved for {p_name}! Maturity Option Unlocked."
          )
          maturity, fee, gst, net_payout, net_profit, _, _ = calculate_payout(
              p_target, p_freq
          )

          st.write(
              f"📅 **Target Completion Date:**"
              f" {completion_date.strftime('%d %B %Y')}"
          )
          st.write(
              f"🔓 **Redemption Unlock Date:**"
              f" {withdrawal_date.strftime('%d %B %Y')}"
          )
          st.metric("Achieved Net Payout Value", f"₹ {net_payout:,.2f}")

          if st.button(
              f"Initiate Withdrawal Request ({p_name})",
              key=f"w_btn_{p_name}",
              type="primary",
          ):
            if not is_kyc_verified:
              w_status = "Pending"
            elif not is_lockin_passed:
              w_status = "In Process"
            else:
              w_status = "Completed"

            log_withdrawal_request(username, p_name, net_payout, w_status)

            if not is_kyc_verified:
              st.error(
                  "🚨 Withdrawal Request Submitted. Status is **Pending** because"
                  " your KYC/Bank details verification is pending."
              )
            elif not is_lockin_passed:
              st.warning(
                  "⏳ Withdrawal Request Submitted. Status is **In Process**"
                  " because the 1-month holding lock-in period is active."
              )
            else:
              st.success(
                  "🎉 Withdrawal Request Approved! Status is **Completed** and"
                  " funds have been transferred to your verified bank account."
              )
            time.sleep(2)
            st.rerun()

        st.markdown("---")

      st.subheader("📄 Download Certified Statement of Account")
      report_text = generate_text_summary(
          username, investor_id, kyc_status, df_sub, df_tx
      )
      st.download_button(
          label="📥 Download Certified Statement of Account (TXT)",
          data=report_text,
          file_name=f"GullakCoin_Statement_of_Account_{investor_id}.txt",
          mime="text/plain",
          type="primary",
      )

    else:
      st.warning(
          "No active capital allocations found. Go to 'Product offerings' to"
          " select and authorize plans."
      )

  elif menu == "📝 Transaction History":
    st.subheader("Certified Statement of Account & E-Mandate Ledger")
    st.markdown(
        "<p style='color: #cbd5e1;'>Itemized ledger showing every E-Mandate hit,"
        " plan reference, and withdrawal status (Pending / In Process /"
        " Completed).</p>",
        unsafe_allow_html=True,
    )

    if not df_sub.empty:
      with st.expander("🛠️ Developer Sandbox: Simulate E-Mandate Failure"):
        if st.button(
            "Simulate Insufficient Balance (Fail Next Installment)",
            key="sim_fail_btn",
            type="secondary",
        ):
          sample_plan = df_sub.iloc[0]["plan_name"]
          sample_inst = df_sub.iloc[0]["installment_amt"]
          log_failed_transaction(username, sample_plan, sample_inst)
          st.warning(
              f"⚠️ Simulated E-Mandate failure recorded for {sample_plan}!"
          )
          time.sleep(1)
          st.rerun()

    if not df_tx.empty:
      st.dataframe(
          df_tx[
              [
                  "date",
                  "plan_ref",
                  "trans_type",
                  "category",
                  "amount",
                  "status",
              ]
          ].sort_values(by="date", ascending=False),
          use_container_width=True,
          hide_index=True,
      )
    else:
      st.info("No ledger entries found.")

  elif menu == "🤖 AI Wealth Advisor":
    st.subheader("🤖 Smart Wealth Advisor & Voice Copilot")
    st.write(
        "Ask anything about your investment strategy, multi-plan startup"
        " allocation, or portfolio targets!"
    )

    st.markdown("---")
    st.markdown("#### 🎙️ Voice-Controlled AI Financial Copilot")
    audio_input_file = st.audio_input(
        "Record your financial query (e.g., 'What is my portfolio status?')"
    )
    if audio_input_file is not None:
      st.success("🎤 Audio recorded successfully! Processing voice command...")
      simulated_voice_query = "What is my portfolio status?"
      st.info(f"🗣️ **Recognized Voice Query:** *{simulated_voice_query}*")
      st.write(
          f"📊 **Copilot Response:** Your total active portfolio value is"
          f" **₹ {portfolio_value:,.2f}** across active plans (Total Target:"
          f" ₹ {total_target_value:,.0f})."
      )
    st.markdown("---")

    if "ai_messages" not in st.session_state:
      st.session_state.ai_messages = []

    for message in st.session_state.ai_messages:
      with st.chat_message(message["role"]):
        st.markdown(message["content"])

    if user_prompt := st.chat_input(
        "Type your financial query here (e.g., How to optimize my SIP?)"
    ):
      st.session_state.ai_messages.append(
          {"role": "user", "content": user_prompt}
      )
      with st.chat_message("user"):
        st.markdown(user_prompt)

      with st.chat_message("assistant"):
        with st.spinner("Smart AI Advisor is analyzing..."):
          q = user_prompt.lower()

          def dispatch_agent_plugin(query):
            risk_response = RiskAgentPlugin.evaluate_query(query)
            if risk_response:
              return risk_response

            if any(
                k in query for k in ["what is e-mandate", "e-nach", "enach"]
            ):
              return (
                  "🔄 **What is an E-Mandate? (Protocol Agent)**: An E-Mandate"
                  " (AutoPay / E-NACH) is an automated authorization given to"
                  " your bank to deduct your chosen SIP amount across your"
                  " running plans on schedule."
              )
            elif any(k in query for k in ["product", "offering", "tiers"]):
              return (
                  "📦 **Product Offerings (Allocation Agent)**: GullakCoin Pro"
                  " offers 4 structured startup allocation tiers that you can"
                  " invest in simultaneously!"
              )
            else:
              return (
                  f"💡 **DeepSeek Harness Advisor Insight**: Regarding your"
                  f" query about *'{user_prompt}'*, GullakCoin Pro's multi-plan"
                  " milestone model delivers superior net returns compared to"
                  " standard bank FDs."
              )

          ai_response = dispatch_agent_plugin(q)
          st.markdown(ai_response)
          st.session_state.ai_messages.append(
              {"role": "assistant", "content": ai_response}
          )

  elif menu == "👤 Profile & KYC":
    st.subheader("User Profile & KYC Verification")
    st.markdown(
        f"""
        * **Registered Account / Mobile:** `{username}`
        * **Permanent Investor ID:** `👤 {investor_id}`
        * **Current KYC & Bank Status:** **{kyc_status}**
        """
    )
    st.markdown("---")

    st.subheader("Update PAN, Aadhaar & Bank Details")
    st.markdown(
        "<p style='font-size: 13px; color: #cbd5e1;'><b>Rule:</b> Bank Account"
        " verification requires your bank registered mobile number to match"
        " your login mobile number (<b>"
        + username
        + "</b>) for automatic approval. Otherwise KYC remains Pending.</p>",
        unsafe_allow_html=True,
    )

    with st.form("kyc_form"):
      new_pan = st.text_input(
          "PAN Card Number", value=pan_num, placeholder="ABCDE1234F"
      )
      new_aadhar = st.text_input(
          "Aadhaar Card Number",
          value=aadhar_num,
          placeholder="12 Digit Aadhaar Number",
      )
      new_bank = st.text_input(
          "Bank Account Number",
          value=bank_acc,
          placeholder="Enter Bank Account Number",
      )
      new_ifsc = st.text_input(
          "IFSC Code", value=ifsc_code, placeholder="SBIN000XXXX"
      )
      new_branch = st.text_input(
          "Branch Name", value=branch_name, placeholder="Main Branch City"
      )
      new_bmobile = st.text_input(
          "Bank Registered Mobile Number",
          value=bank_mobile,
          placeholder="Must match login mobile",
      )

      submit_kyc = st.form_submit_button(
          "Submit KYC & Bank Details for Verification", type="primary"
      )

      if submit_kyc:
        if (
            new_pan
            and new_aadhar
            and new_bank
            and new_ifsc
            and new_branch
            and new_bmobile
        ):
          res_status = update_kyc(
              username,
              new_pan,
              new_aadhar,
              new_bank,
              new_ifsc,
              new_branch,
              new_bmobile,
          )
          if "Verified" in res_status:
            st.success(
                "✅ Bank details & KYC verified successfully! Account Approved."
            )
          else:
            st.warning(
                "⚠️ KYC updated as Pending. Bank registered mobile number must"
                " match your login mobile number for approval."
            )
          time.sleep(2)
          st.rerun()
        else:
          st.warning("Please fill in all KYC and banking fields completely.")

  elif menu == "💬 Support & Help":
    st.subheader("Customer Support & Assistance")
    st.write(
        "We are here to help you 24/7 with your investments and E-Mandates."
    )
    st.write("")

    wa_msg = urllib.parse.quote(
        "Hello GullakCoin Pro Support, I need assistance with my investment."
    )
    wa_url = f"https://wa.me/{MY_WHATSAPP_NUMBER}?text={wa_msg}"
    telegram_url = f"https://t.me/{MY_TELEGRAM_USERNAME}"

    s_col1, s_col2, s_col3 = st.columns(3)
    with s_col1:
      st.markdown(
          f"""
            <div class="support-card">
                <h3>💬 WhatsApp Support</h3>
                <p style="color: #cbd5e1; font-size: 13px;">Instant chat assistance with our executive.</p>
                <a href="{wa_url}" target="_blank"><button style="background-color: #25D366; color: white; border: none; padding: 10px 20px; border-radius: 8px; font-weight: bold; cursor: pointer;">Chat on WhatsApp</button></a>
            </div>
            """,
          unsafe_allow_html=True,
      )

    with s_col2:
      st.markdown(
          f"""
            <div class="support-card">
                <h3>🤖 Telegram Bot</h3>
                <p style="color: #cbd5e1; font-size: 13px;">Get automated updates via our Telegram Bot.</p>
                <a href="{telegram_url}" target="_blank"><button style="background-color: #0088cc; color: white; border: none; padding: 10px 20px; border-radius: 8px; font-weight: bold; cursor: pointer;">Join Telegram Bot</button></a>
            </div>
            """,
          unsafe_allow_html=True,
      )

    with s_col3:
      st.markdown(
          f"""
            <div class="support-card">
                <h3>📧 Email Support</h3>
                <p style="color: #cbd5e1; font-size: 13px;">Write to us at {MY_EMAIL}</p>
                <a href="mailto:{MY_EMAIL}"><button style="background-color: #34d399; color: black; border: none; padding: 10px 20px; border-radius: 8px; font-weight: bold; cursor: pointer;">Send Email</button></a>
                </div>
            """,
          unsafe_allow_html=True,
      )

  elif menu == "❓ FAQs":
    st.subheader("❓ Frequently Asked Questions")
    with st.expander("Q: How does withdrawal status work?"):
      st.write(
          "A: When you initiate a withdrawal after your target is completed,"
          " the status is recorded as **Pending** (if KYC is unverified), **In"
          " Process** (if KYC is verified but the 1-month lock-in period is"
          " active), or **Completed** (once all conditions are fully"
          " satisfied)."
      )
    with st.expander("Q: Can I run multiple investment plans simultaneously?"):
      st.write(
          "A: Yes! You can subscribe to and run multiple startup allocation"
          " plans simultaneously."
      )
