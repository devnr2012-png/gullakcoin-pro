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

# --- CASHFREE & TELEGRAM CONFIGURATION ---
CASHFREE_APP_ID = "YOUR_CASHFREE_APP_ID"
CASHFREE_SECRET_KEY = "YOUR_CASHFREE_SECRET_KEY"
CASHFREE_ENV = "TEST"
TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
TELEGRAM_CHAT_ID = "YOUR_TELEGRAM_CHAT_ID"

# --- TWILIO SMS API CONFIGURATION ---
TWILIO_ACCOUNT_SID = "AC6ee8959f0b00dd9d5b8648baeddda119"
TWILIO_API_KEY_SID = "SK051e4ca445f1469c93174d5f794a0089"
TWILIO_API_SECRET = "LTMfWNFvjS60bethokwAvmAdleQvgS0I"
TWILIO_PHONE_NUMBER = "YOUR_TWILIO_PHONE_NUMBER"  # Apna Twilio phone number yahan dalein

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
    
    .stTabs [data-baseweb="tab-list"] { gap: 10px; justify-content: center; }
    .stTabs [data-baseweb="tab"] {
        background-color: #000000 !important;
        border-radius: 8px !important;
        border: 1px solid #059669 !important;
        padding: 10px 18px !important;
    }
    .stTabs [data-baseweb="tab"] p {
        color: #34d399 !important;
        font-weight: 800 !important;
        font-size: 15px !important;
        font-style: italic;
    }
    .stTabs [aria-selected="true"] {
        background-color: #0b2920 !important;
        border-color: #34d399 !important;
        box-shadow: 0 0 15px rgba(52, 211, 153, 0.3);
    }
    .stTabs [aria-selected="true"] p {
        color: #ffffff !important;
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
        padding: 40px; border-radius: 20px; border: 1px solid #10b981;
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.7); max-width: 520px; margin: 0 auto;
    }
    
    .nurturing-banner {
        background: linear-gradient(rgba(4, 47, 34, 0.65), rgba(4, 47, 34, 0.65)), 
                    url('https://images.unsplash.com/photo-1542601906990-b4d3fb778b09?auto=format&fit=crop&w=1200&q=80');
        background-size: cover;
        background-position: center;
        border: 2px solid #34d399;
        padding: 28px 20px;
        border-radius: 16px;
        text-align: center;
        max-width: 520px;
        margin: 0 auto 20px auto;
        box-shadow: 0 10px 30px rgba(52, 211, 153, 0.35);
    }
    .banner-title {
        font-size: 13px; text-transform: uppercase; letter-spacing: 2px; color: #34d399; font-weight: 900; margin-bottom: 6px;
    }
    .banner-text {
        font-size: 17px; font-weight: 700; color: #ffffff;
    }
    .ad-badge {
        display: inline-block; background: #fbbf24; color: #061a14; font-size: 11px; font-weight: 900; padding: 2px 8px; border-radius: 4px; margin-top: 8px;
    }

    .logo-container { text-align: center; margin-bottom: 20px; }
    .logo-badge {
        display: inline-block; background: linear-gradient(135deg, #34d399, #059669); color: #061a14;
        font-weight: 900; font-size: 28px; padding: 12px 22px; border-radius: 16px;
        box-shadow: 0 10px 25px rgba(52, 211, 153, 0.4); letter-spacing: 1.5px;
    }
    .brand-title { font-size: 30px; font-weight: 900; color: #ffffff; margin-top: 15px; }
    .brand-tagline { font-size: 13px; color: #34d399; margin-top: 6px; font-style: italic; font-weight: 700; }
    
    .plan-card {
        background-color: #0b2920; padding: 25px; border-radius: 16px; border: 1px solid #047857;
        height: 230px; display: flex; flex-direction: column; justify-content: flex-start; margin-bottom: 12px;
    }
    .detail-card {
        background-color: #0b2920; padding: 22px; border-radius: 12px; border: 1px solid #34d399;
        text-align: center; margin-top: 15px; margin-bottom: 15px;
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
</style>
""",
    unsafe_allow_html=True,
)


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
                 id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, trans_type TEXT, category TEXT, amount REAL, status TEXT, date TEXT)"""
  )
  c.execute(
      """CREATE TABLE IF NOT EXISTS subscriptions (
                 id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, plan_name TEXT, target_amount INTEGER, frequency TEXT, installment_amt REAL, date TEXT)"""
  )
  conn.commit()
  conn.close()


def send_twilio_sms(to_number, message_body):
  if (
      TWILIO_PHONE_NUMBER == "YOUR_TWILIO_PHONE_NUMBER"
      or not TWILIO_PHONE_NUMBER
  ):
    return False
  url = f"https://api.twilio.com/2010-04-01/Accounts/{TWILIO_ACCOUNT_SID}/Messages.json"
  payload = {
      "To": to_number,
      "From": TWILIO_PHONE_NUMBER,
      "Body": message_body,
  }
  try:
    response = requests.post(
        url,
        data=payload,
        auth=(TWILIO_API_KEY_SID, TWILIO_API_SECRET),
        timeout=5,
    )
    return response.status_code == 201
  except Exception:
    return False


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
      f"SELECT * FROM subscriptions WHERE username='{username}' ORDER BY id"
      " DESC LIMIT 1",
      conn,
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
      " status, date) VALUES (?, ?, ?, ?, ?, ?)",
      (username, "Income", "Investment", installment_amt, "Success", dt),
  )
  conn.commit()
  conn.close()
  send_telegram_alert(
      f"🚀 New E-Mandate Alert: {username} subscribed to {plan_name} via"
      f" {frequency_text} SIP (Amt: ₹{installment_amt:,.2f})"
  )


def log_failed_transaction(username, installment_amt):
  conn = sqlite3.connect("gullakcoin_advanced.db")
  c = conn.cursor()
  dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  c.execute(
      "INSERT INTO transactions (username, trans_type, category, amount,"
      " status, date) VALUES (?, ?, ?, ?, ?, ?)",
      (
          username,
          "Expense",
          "Failed SIP",
          installment_amt,
          "Failed (Insufficient Balance)",
          dt,
      ),
  )
  conn.commit()
  conn.close()
  send_telegram_alert(
      f"⚠️ AutoPay Failure Alert: {username} installment of ₹{installment_amt:,.2f}"
      " failed due to insufficient balance!"
  )


init_db()

# --- SESSION STATE ---
if "logged_in" not in st.session_state:
  st.session_state.logged_in = False
if "current_user" not in st.session_state:
  st.session_state.current_user = ""
if "otp_generated" not in st.session_state:
  st.session_state.otp_generated = ""
if "auth_stage" not in st.session_state:
  st.session_state.auth_stage = "none"
if "selected_plan" not in st.session_state:
  st.session_state.selected_plan = None
if "forgot_user" not in st.session_state:
  st.session_state.forgot_user = ""
if "whatsapp_otp_sent" not in st.session_state:
  st.session_state.whatsapp_otp_sent = False

# --- AUTHENTICATION SCREEN ---
if not st.session_state.logged_in:
  st.write("")
  ads_list = [
      (
          "🌱 GullakCoin Seed (Target: ₹ 5,000) - Nurturing small savings into"
          " fruitful returns together!"
      ),
      (
          "🌿 GullakCoin Growth (Target: ₹ 25,000) - Watch your family's future"
          " grow with dynamic venture allocations."
      ),
      (
          "🌳 GullakCoin Plus (Target: ₹ 50,000) - Advanced mid-stage capital"
          " branching out securely for generations."
      ),
      (
          "🌲 GullakCoin Superplus (Target: ₹ 100,000) - Maximum institutional"
          " tree growth & robust financial yield."
      ),
  ]
  active_ad = ads_list[int(time.time()) % len(ads_list)]

  st.markdown(
      f"""
        <div class="nurturing-banner">
            <div class="banner-title">👨‍👦 Nurturing Wealth Together (Guiding the Next Generation)</div>
            <div class="banner-text">{active_ad}</div>
            <div class="ad-badge">✨ Featured Company Wealth Plan</div>
        </div>
    """,
      unsafe_allow_html=True,
  )

  st.markdown("<div class='auth-container'>", unsafe_allow_html=True)
  st.markdown(
      """
        <div class="logo-container">
            <div class="logo-badge">GC</div>
            <div class="brand-title">GullakCoin Pro</div>
            <div class="brand-tagline">“Nurturing Your Wealth, From a Seedling to a Grand Tree.”</div>
        </div>
    """,
      unsafe_allow_html=True,
  )

  tab1, tab2, tab3 = st.tabs(
      ["Secure Login", "Create Account", "🔑 Forgot Password"]
  )

  with tab1:
    st.write("")
    l_user = st.text_input("Registered Email or Mobile Number", key="l_user")
    l_pass = st.text_input("Secure Password", type="password", key="l_pass")

    # Biometric / Passkey Quick Login Simulator Toggle
    use_biometric = st.checkbox(
        "🔑 Quick Login via Device Passkey / Biometric Simulator"
    )
    st.write("")

    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
      req_wa = st.button(
          "Request WhatsApp OTP", use_container_width=True, type="primary"
      )
    with col_btn2:
      req_sms = st.button(
          "Request Text (SMS) OTP", use_container_width=True, type="secondary"
      )

    if req_wa or req_sms:
      conn = sqlite3.connect("gullakcoin_advanced.db")
      c = conn.cursor()
      c.execute(
          "SELECT * FROM users WHERE username=? AND password=?", (l_user, l_pass)
      )
      user_exists = c.fetchone()
      conn.close()

      if use_biometric and l_user:
        st.session_state.logged_in = True
        st.session_state.current_user = l_user
        st.success("🔓 Biometric Passkey Verified Successfully!")
        time.sleep(1)
        st.rerun()
      elif user_exists or l_user:
        otp = str(random.randint(100000, 999999))
        st.session_state.otp_generated = otp
        st.session_state.auth_stage = "login_otp"
        st.session_state.whatsapp_otp_sent = req_wa

        if req_sms and l_user and l_user.isdigit():
          # Send Real SMS via Twilio API
          sms_body = (
              f"Your GullakCoin Pro verification code is: {otp}. Valid for 5"
              " minutes."
          )
          target_mobile = (
              f"+{l_user.strip()}"
              if not l_user.startswith("+")
              else l_user.strip()
          )
          sms_sent = send_twilio_sms(target_mobile, sms_body)
          if sms_sent:
            st.success("✅ Real SMS OTP sent successfully via Twilio!")
          else:
            st.info(
                f"ℹ️ SMS Gateway notice. Simulated Code: **{otp}** (Configure"
                " Twilio Phone Number)"
            )
        elif req_wa:
          st.success("✅ WhatsApp OTP Generated Successfully!")
      else:
        st.error("Please enter your registered mobile number or email.")

    if st.session_state.auth_stage == "login_otp":
      target_phone = (
          l_user.strip()
          if l_user
          and l_user.isdigit()
          and len(l_user) >= 10
          else MY_WHATSAPP_NUMBER
      )

      if st.session_state.whatsapp_otp_sent:
        wa_msg = (
            "Hello, please send my GullakCoin Pro Login OTP. Verification Code:"
            f" {st.session_state.otp_generated}"
        )
        wa_link = (
            f"https://wa.me/{target_phone}?text={urllib.parse.quote(wa_msg)}"
        )

        st.markdown(
            f"""
                <div style="background-color: rgba(37, 211, 102, 0.15); border: 1px solid #25D366; padding: 15px; border-radius: 10px; text-align: center; margin-bottom: 15px;">
                    <p style="color: #ffffff; font-weight: 700; margin-bottom: 8px;">📲 Click below to receive your OTP instantly on WhatsApp:</p>
                    <a href="{wa_link}" target="_blank" style="background-color: #25D366; color: white; padding: 10px 20px; border-radius: 8px; text-decoration: none; font-weight: bold; display: inline-block;">💬 Send OTP via WhatsApp</a>
                </div>
                """,
            unsafe_allow_html=True,
        )
      else:
        st.info(
            "📩 Enter the Text OTP received on your mobile number (Simulated"
            f" code for testing: **{st.session_state.otp_generated}**)"
        )

      l_otp_input = st.text_input(
          "Enter 6-Digit Verification Code", key="l_otp"
      )
      if st.button(
          "Verify & Access Dashboard", type="primary", use_container_width=True
      ):
        if l_otp_input == st.session_state.otp_generated:
          st.session_state.logged_in = True
          st.session_state.current_user = l_user
          st.session_state.auth_stage = "none"
          st.session_state.whatsapp_otp_sent = False
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
        conn = sqlite3.connect("gullakcoin_advanced.db")
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=?", (s_user,))
        if c.fetchone():
          st.error("Account already exists.")
        else:
          otp = str(random.randint(100000, 999999))
          st.session_state.otp_generated = otp
          st.session_state.auth_stage = "signup_otp"
          st.success(f"🔐 Registration OTP: **{otp}** (Simulated)")
        conn.close()
      else:
        st.warning("Please fill in all fields.")

    if st.session_state.auth_stage == "signup_otp":
      s_otp_input = st.text_input(
          "Enter 6-Digit Verification Code", key="s_otp"
      )
      if st.button(
          "Verify & Complete Registration", type="primary", use_container_width=True
      ):
        if s_otp_input == st.session_state.otp_generated:
          investor_id = f"GC-PRO-{random.randint(100000, 999900)}"
          conn = sqlite3.connect("gullakcoin_advanced.db")
          c = conn.cursor()
          c.execute(
              "INSERT INTO users (username, password, investor_id, kyc_status,"
              " pan, aadhar, bank_acc, ifsc, branch, bank_mobile) VALUES (?, ?,"
              " ?, ?, ?, ?, ?, ?, ?, ?)",
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
              f" {investor_id}. Please login."
          )
          st.session_state.auth_stage = "none"
          time.sleep(3)
          st.rerun()
        else:
          st.error("Invalid verification code.")

  with tab3:
    st.write("")
    f_user = st.text_input(
        "Enter Your Registered Email or Mobile Number", key="f_user"
    )
    st.write("")

    if st.button("Send Password Reset OTP", use_container_width=True):
      if f_user:
        conn = sqlite3.connect("gullakcoin_advanced.db")
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=?", (f_user,))
        user_record = c.fetchone()
        conn.close()

        if user_record:
          otp = str(random.randint(100000, 999999))
          st.session_state.otp_generated = otp
          st.session_state.forgot_user = f_user
          st.session_state.auth_stage = "forgot_otp"
          st.success(f"🔐 Reset OTP: **{otp}** (Simulated)")
        else:
          st.error("Account not found with this mobile number/email.")
      else:
        st.warning("Please enter your registered number or email.")

    if st.session_state.auth_stage == "forgot_otp":
      f_otp_input = st.text_input("Enter 6-Digit Reset OTP", key="f_otp")
      new_pass_1 = st.text_input("New Password", type="password", key="n_pass1")
      new_pass_2 = st.text_input(
          "Confirm New Password", type="password", key="n_pass2"
      )

      if st.button(
          "Reset Password & Save", type="primary", use_container_width=True
      ):
        if f_otp_input == st.session_state.otp_generated:
          if new_pass_1 and new_pass_1 == new_pass_2:
            update_password(st.session_state.forgot_user, new_pass_1)
            st.success(
                "🎉 Password updated successfully! Please go to Secure Login."
            )
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
  target_value = 0
  active_plan = None
  balance_target = 0
  estimated_maturity = 0


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


  if not df_sub.empty:
    active_plan = df_sub.iloc[0]
    target_value = active_plan["target_amount"]
    balance_target = max(target_value - portfolio_value, 0)
    estimated_maturity, _, _, _, _, _ = calculate_payout(
        target_value, active_plan["frequency"]
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
    st.rerun()

  # HEADER METRICS
  col1, col2, col3, col4 = st.columns(4)
  with col1:
    st.metric("Portfolio Value", f"₹ {portfolio_value:,.2f}")
  with col2:
    st.metric("Target Value", f"₹ {target_value:,.0f}")
  with col3:
    st.metric(
        "Balance Target",
        f"🔒 ₹ {balance_target:,.2f}"
        if balance_target > 0
        else "✅ Completed",
    )

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
      st.markdown(
          "<p style='color: #cbd5e1; font-size: 16px; margin-bottom: 5px;'>Select"
          " a structured allocation plan below to view projections and E-Mandate"
          " frequencies.</p>",
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

      cols = st.columns(4)
      for i, (title, target_amt, desc, key_id) in enumerate(plans):
        with cols[i]:
          st.markdown(
              f"""
                    <div class="plan-card">
                        <div class="plan-title">{title}</div>
                        <div class="plan-desc">{desc}</div>
                        <div class="plan-target">🎯 Target: ₹ {target_amt:,.0f}</div>
                    </div>
                    """,
              unsafe_allow_html=True,
          )
          if st.button(
              f"Explore {title.split()[-1]}",
              key=f"expl_{key_id}",
              use_container_width=True,
          ):
            st.session_state.selected_plan = {
                "title": title,
                "target": target_amt,
                "desc": desc,
            }
            st.rerun()
    else:
      plan = st.session_state.selected_plan
      target_amt = plan["target"]
      title = plan["title"]

      if st.button("⬅️ Back to All Plans"):
        st.session_state.selected_plan = None
        st.rerun()

      st.markdown(
          f"<h1>{title} <span style='color: #34d399;'>| Target: ₹"
          f" {target_amt:,.0f}</span></h1>",
          unsafe_allow_html=True,
      )
      st.write(plan["desc"])

      st.markdown(
          """
            <div class="strict-rule-box">
                <b>⚠️ Important Lock-in & E-Mandate Rule:</b><br>
                Once you authorize AutoPay, installments deduct automatically. <b>You cannot withdraw</b> your funds until the full Target Principal and maturity cycle are 100% completed. In case of insufficient bank balance, a 5-day grace period applies before cycle timeline extension.
            </div>
            """,
          unsafe_allow_html=True,
      )

      st.subheader("Configure AutoPay E-Mandate Frequency:")

      freqs = [
          ("Daily", target_amt / 90, 0.08),
          ("Weekly", (target_amt / 90) * 7, 0.10),
          ("Monthly", target_amt / 3, 0.18),
      ]

      f_cols = st.columns(3)
      for i, (f_name, f_amt, f_roi) in enumerate(freqs):
        maturity, fee, gst, net_payout, net_profit, bonus = calculate_payout(
            target_amt, f_name
        )
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
                            <span style='color: #34d399; font-size: 16px;'><b>Est. Net Payout: ₹ {net_payout:,.2f}</b></span>
                        </p>
                    </div>
                    """,
              unsafe_allow_html=True,
          )
          if st.button(
              f"Authorize {f_name} AutoPay",
              key=f"sub_{f_name}",
              type="primary",
              use_container_width=True,
          ):
            try:
              # Cashfree Order Registration
              add_subscription(username, title, target_amt, f_name, f_amt)
              st.success(
                  f"✅ E-Mandate registered successfully for {title} via"
                  f" {f_name} SIP!"
              )
              st.session_state.selected_plan = None
              time.sleep(2)
              st.rerun()
            except Exception as e:
              st.error(f"Error: {e}")

  elif menu == "📊 My Portfolio":
    st.subheader("Active Asset Allocation & Projections")
    if active_plan is not None:
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
                <h4 style="color: #fbbf24; margin-top:0;">🤖 AI Yield Predictor & Gamification</h4>
                <p style="margin-bottom: 5px;"><b>Active Streak:</b> {streak_days} Days Consistent AutoPay</p>
                <p style="margin-bottom: 5px;"><b>Investor Status Badge:</b> {badge_level}</p>
                <p style="font-size: 12px; color: #cbd5e1; margin-bottom:0;">Maintain consistent deductions to qualify for AI-modeled yield bonuses and VIP fee waivers.</p>
            </div>
            """,
          unsafe_allow_html=True,
      )

      failed_txs = df_tx[df_tx["status"] == "Failed (Insufficient Balance)"]

      if not failed_txs.empty:
        st.markdown(
            f"""
                <div class="alert-failed">
                    <b>⚠️ AutoPay E-Mandate Failure Detected!</b><br>
                    Your recent installment of <b>₹ {active_plan['installment_amt']:,.2f}</b> failed due to insufficient bank balance. A 5-day grace period is active. Please clear your missed payment to prevent timeline extension.
                </div>
                """,
            unsafe_allow_html=True,
        )

        if st.button(
            "💳 Pay Missed Installment Now (Manual UPI/Card)", type="primary"
        ):
          conn = sqlite3.connect("gullakcoin_advanced.db")
          c = conn.cursor()
          dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
          c.execute(
              "INSERT INTO transactions (username, trans_type, category,"
              " amount, status, date) VALUES (?, ?, ?, ?, ?, ?)",
              (
                  username,
                  "Income",
                  "Investment",
                  active_plan["installment_amt"],
                  "Success",
                  dt,
              ),
          )
          conn.commit()
          conn.close()
          st.success(
              "✅ Missed installment cleared successfully! Your cycle is back on"
              " track."
          )
          time.sleep(2)
          st.rerun()

      p_col1, p_col2, p_col3 = st.columns(3)
      with p_col1:
        st.info(f"**Active Plan:** {active_plan['plan_name']}")
      with p_col2:
        st.info(f"**Target Principal:** ₹ {active_plan['target_amount']:,.0f}")
      with p_col3:
        st.info(f"**Frequency:** {active_plan['frequency']}")

      st.progress(min(portfolio_value / target_value, 1.0))
      st.write(
          f"Accumulated via AutoPay: **₹ {portfolio_value:,.2f}** out of ₹"
          f" {target_value:,.0f}"
      )
      st.markdown("---")

      start_date = pd.to_datetime(active_plan["date"])
      completion_date = start_date + pd.Timedelta(days=90)
      withdrawal_date = completion_date + pd.Timedelta(days=30)
      current_time = pd.Timestamp.now()

      is_target_completed = portfolio_value >= target_value
      is_lockin_passed = current_time >= withdrawal_date

      st.subheader("Maturity & Redemption Portal")

      if not is_target_completed:
        st.markdown(
            f"""
                <div class="locked-box">
                    <h3 style="color: #fbbf24; margin-bottom: 5px;">🔒 Maturity & Withdrawal Locked</h3>
                    <p style="color: #fef3c7; font-size: 14px;">Your SIP deductions are ongoing. Withdrawals remain strictly locked until your <b>Target Principal of ₹ {target_value:,.0f}</b> is fully accumulated.</p>
                </div>
                """,
            unsafe_allow_html=True,
        )
      else:
        if "Verified" not in kyc_status:
          st.error(
              "🚨 Withdrawal Blocked: Your Bank Details & KYC Verification is"
              " Pending/Mismatch. Please go to 'Profile & KYC' to complete"
              " verification with your registered mobile number."
          )
        else:
          w_col1, w_col2 = st.columns(2)
          with w_col1:
            st.success("✅ Target 100% Achieved & Bank Verified!")
            st.write(
                f"📅 **Target Completion Date:**"
                f" {completion_date.strftime('%d %B %Y')}"
            )
            st.write(
                f"🔓 **Redemption Unlock Date:**"
                f" {withdrawal_date.strftime('%d %B %Y')}"
            )

          with w_col2:
            maturity, fee, gst, net_payout, net_profit, _ = calculate_payout(
                target_value, active_plan["frequency"]
            )
            st.metric("Achieved Maturity Value", f"₹ {maturity:,.2f}")

            if not is_lockin_passed:
              unlock_str = withdrawal_date.strftime("%d %B %Y")
              st.warning(
                  f"⏳ Withdrawal unlocks on {unlock_str} (1-month hold period"
                  " active)."
              )
              st.button(
                  "Initiate Withdrawal Request",
                  disabled=True,
                  use_container_width=True,
              )
            else:
              if st.button(
                  "Initiate Withdrawal Request",
                  type="primary",
                  use_container_width=True,
              ):
                st.success(
                    "✅ Redemption request queued successfully for bank"
                    " transfer."
                )
                st.code(f"""
Gross Maturity Amount : ₹ {maturity:,.2f}
- Processing Fee (2%) : ₹ {fee:,.2f}
- GST on Fee (18%)    : ₹ {gst:,.2f}
-----------------------------------
Net Bank Credit       : ₹ {net_payout:,.2f}
Estimated Net Gain    : ₹ {net_profit:,.2f}
                                """)
    else:
      st.warning(
          "No active capital allocations found. Explore product offerings to"
          " initiate a plan."
      )

  elif menu == "📝 Transaction History":
    st.subheader("Automated E-Mandate Audit Logs")

    if not df_sub.empty:
      with st.expander("🛠️ Developer Sandbox: Simulate E-Mandate Failure"):
        if st.button(
            "Simulate Insufficient Balance (Fail Next Installment)",
            type="secondary",
        ):
          active_inst = df_sub.iloc[0]["installment_amt"]
          log_failed_transaction(username, active_inst)
          st.warning(
              "⚠️ Simulated E-Mandate failure recorded! Check 'My Portfolio'."
          )
          time.sleep(1)
          st.rerun()

    if not df_tx.empty:
      st.dataframe(
          df_tx[["date", "trans_type", "category", "amount", "status"]]
          .sort_values(by="date", ascending=False),
          use_container_width=True,
          hide_index=True,
      )
    else:
      st.info("No ledger entries found.")

  elif menu == "🤖 AI Wealth Advisor":
    st.subheader("🤖 Smart Wealth Advisor (AI Assistant)")
    st.write(
        "Ask anything about your investment strategy, startup allocation, or"
        " portfolio targets!"
    )

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
            if any(
                k in query
                for k in ["mandate fail", "payment fail", "insufficient"]
            ):
              return (
                  "⚠️ **Failed E-Mandate Resolution (Risk Agent)**: If an"
                  " installment fails due to insufficient bank balance, a"
                  " **5-day grace period** becomes active. You can immediately"
                  " clear the missed installment manually using **UPI / Debit"
                  " Card** from the **'My Portfolio'** tab to prevent tenure"
                  " extension."
              )
            elif any(
                k in query for k in ["what is e-mandate", "e-nach", "enach"]
            ):
              return (
                  "🔄 **What is an E-Mandate? (Protocol Agent)**: An E-Mandate"
                  " (AutoPay / E-NACH) is an automated authorization given to"
                  " your bank to deduct your chosen SIP amount (Daily,"
                  " Weekly, or Monthly) on schedule."
              )
            elif any(k in query for k in ["product", "offering", "tiers"]):
              return (
                  "📦 **Product Offerings (Allocation Agent)**: GullakCoin Pro"
                  " offers 4 structured startup allocation tiers:\n1."
                  " **GullakCoin Seed** (Target ₹ 5,000)\n2. **GullakCoin"
                  " Growth** (Target ₹ 25,000)\n3. **GullakCoin Plus** (Target"
                  " ₹ 50,000)\n4. **GullakCoin Superplus** (Target ₹"
                  " 100,000)"
              )
            elif any(k in query for k in ["120", "lock", "hold"]):
              return (
                  "⏳ **120 Days Lock-in Rule (Milestone Agent)**: Our model"
                  " consists of **90 days of SIP accumulation** followed by a"
                  " **30 days holding lock-in** to maximize startup growth"
                  " returns."
              )
            elif any(
                k in query for k in ["withdraw", "payout", "redeem", "redemption"]
            ):
              return (
                  "💸 **Withdrawal Process (Liquidity Agent)**: Once your"
                  " target is 100% achieved, KYC is verified, and the 30-day"
                  " lock-in passes, click **'Initiate Withdrawal Request'**"
                  " under **'My Portfolio'**."
              )
            elif any(k in query for k in ["plan", "choose", "select"]):
              return (
                  "🎯 **Plan Selection (Execution Agent)**: Go to the **'Product"
                  " offerings'** tab, pick your target tier, choose your"
                  " frequency, and authorize AutoPay."
              )
            elif any(
                k in query for k in ["emi", "deduct", "installment", "how many"]
            ):
              return (
                  f"💳 **EMI & Deductions for {username} (Ledger Agent)**:"
                  " Installments depend on frequency (Daily: 90, Weekly: 13,"
                  " Monthly: 3). Check audit logs under **'Transaction"
                  " History'**."
              )
            elif any(k in query for k in ["transaction", "history", "ledger"]):
              return (
                  "📝 **Transaction History (Audit Agent)**: Open the"
                  " **'Transaction History'** tab to audit past successful"
                  " investments and simulated failures."
              )
            elif any(k in query for k in ["portfolio", "balance", "value"]):
              return (
                  f"📊 **Portfolio Overview (Analytics Agent)**: Your active"
                  f" portfolio value is **₹ {portfolio_value:,.2f}** out of target"
                  f" **₹ {target_value:,.0f}**."
              )
            elif any(k in query for k in ["kyc", "pan", "bank"]):
              return (
                  f"🛡️ **KYC & Bank Status (Compliance Agent)**: Current"
                  f" status is **{kyc_status}**. Ensure your bank registered"
                  f" mobile number matches your login ID (`{username}`)."
              )
            elif any(
                k in query for k in ["detector", "streak", "bonus", "predictor"]
            ):
              return (
                  "🤖 **AI Yield Predictor (Gamification Agent)**: Maintaining"
                  " 3+ consecutive successful AutoPay installments awards you"
                  " the Gold Investor Badge and an extra **+1.0% AI Streak Yield"
                  " Bonus**!"
              )
            else:
              return (
                  f"💡 **DeepSeek Harness Advisor Insight**: Regarding your"
                  f" query about *'{user_prompt}'*, GullakCoin Pro's structured"
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
    st.subheader("Frequently Asked Questions")
    with st.expander("Q: What is the AI Yield Predictor & Streak Tracker?"):
      st.write(
          "A: Our AI system tracks your AutoPay discipline. Maintaining"
          " consistent successful installments increases your streak counter"
          " and qualifies your portfolio for AI-modeled yield bonuses and"
          " investor badges."
      )
    with st.expander("Q: What is my Investor ID and how is it generated?"):
      st.write(
          "A: Your Investor ID (e.g., GC-PRO-XXXXXX) is a unique permanent"
          " identifier generated automatically upon account registration."
      )
    with st.expander(
        "Why should I lock my funds for 4 months instead of a Bank FD?"
    ):
      st.write(
          "Unlike traditional bank FDs yielding 3-7% p.a., GullakCoin Pro's"
          " structured 120-day milestone model targets significantly higher net"
          " returns through startup allocations."
      )
    with st.expander(
        "What happens if my E-Mandate fails due to insufficient balance?"
    ):
      st.write(
          "You receive a 5-day grace period to clear your installment"
          " manually via UPI/Card in your 'My Portfolio' tab."
      )
