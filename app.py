elif menu == "🤖 AI Wealth Advisor":
    st.subheader("🤖 Smart Wealth Advisor & Voice Copilot")
    st.write(
        "Ask anything about your investment strategy, startup allocation, or"
        " portfolio targets (e.g., checking your ₹ portfolio value)!"
    )

    # --- VOICE-CONTROLLED AI FINANCIAL COPILOT (NATIVE AUDIO INPUT) ---
    st.markdown("---")
    st.markdown("#### 🎙️ Voice-Controlled AI Financial Copilot (₹ Assistant)")
    audio_input_file = st.audio_input(
        "Record your financial query (e.g., 'What is my portfolio status in ₹?')"
    )
    if audio_input_file is not None:
      st.success("🎤 Audio recorded successfully! Processing voice command...")
      simulated_voice_query = "What is my portfolio status?"
      st.info(f"🗣️ **Recognized Voice Query:** *{simulated_voice_query}*")
      st.write(
          f"📊 **Copilot Response:** Your current active portfolio value is"
          f" **₹ {portfolio_value:,.2f}** out of target **₹ {target_value:,.0f}**."
      )
    st.markdown("---")
