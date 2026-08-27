import streamlit as st


def render_gamification_widget(df_tx):
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
        <div style="background: linear-gradient(135deg, rgba(251, 191, 36, 0.12), rgba(5, 150, 105, 0.2));
        border: 1px solid #fbbf24; padding: 22px; border-radius: 16px; margin-bottom: 20px; color: #f8fafc;">
            <h4 style="color: #fbbf24; margin-top:0;">🤖 AI Yield Predictor & Gamification Plugin</h4>
            <p style="margin-bottom: 5px;"><b>Active Streak:</b> {streak_days} Days Consistent AutoPay</p>
            <p style="margin-bottom: 5px;"><b>Investor Status Badge:</b> {badge_level}</p>
            <p style="font-size: 12px; color: #cbd5e1; margin-bottom:0;">Modular plugin architecture active.</p>
        </div>
        """,
      unsafe_allow_html=True,
  )
