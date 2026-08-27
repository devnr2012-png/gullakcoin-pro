elif menu == "❓ FAQs":
    st.subheader("❓ Frequently Asked Questions & Portfolio Guide")
    st.markdown(
        "<p style='color: #cbd5e1;'>Complete guidance on GullakCoin Pro's"
        " automated wealth model, portfolio tiers, and E-Mandate"
        " workflows.</p>",
        unsafe_allow_html=True,
    )

    with st.expander("Q1: What is GullakCoin Pro and how does it work?"):
      st.write(
          "A: GullakCoin Pro is a next-generation structured milestone wealth"
          " platform. It allows you to micro-invest in high-growth startup"
          " allocations through automated E-Mandate (AutoPay) cycles spanning 4"
          " months (3 months accumulation + 1 month hold period)."
      )

    with st.expander(
        "Q2: What are the Portfolio Tiers and their detailed allocations?"
    ):
      st.markdown("""
            A: GullakCoin Pro offers 4 structured startup allocation tiers designed for different risk-reward profiles:
            * **1. GullakCoin Seed Plan (Target: ₹ 5,000)**
              * *Best for:* Early-stage startup exposure with low micro-tickets.
              * *Daily SIP:* ~₹ 55.56 | *Weekly SIP:* ~₹ 384.62 | *Monthly SIP:* ₹ 1,666.67
              * *Target Net Yield:* 8% to 9% p.a. equivalent base + AI streak bonus.
            * **2. GullakCoin Growth Plan (Target: ₹ 25,000)**
              * *Best for:* Dynamically scaling an emerging startup portfolio.
              * *Daily SIP:* ~₹ 277.78 | *Weekly SIP:* ~₹ 1,923.08 | *Monthly SIP:* ₹ 8,333.33
              * *Target Net Yield:* 10% base + streak bonuses.
            * **3. GullakCoin Plus Plan (Target: ₹ 50,000)**
              * *Best for:* Advanced access into mid-stage venture rounds.
              * *Daily SIP:* ~₹ 555.56 | *Weekly SIP:* ~₹ 3,846.15 | *Monthly SIP:* ₹ 16,666.67
              * *Target Net Yield:* 12% base allocation performance.
            * **4. GullakCoin Superplus Plan (Target: ₹ 1,000,000 / ₹ 1 Lakh)**
              * *Best for:* Exclusive curated high-net-worth venture allocations.
              * *Daily SIP:* ~₹ 1,111.11 | *Weekly SIP:* ~₹ 7,692.30 | *Monthly SIP:* ₹ 33,333.33
              * *Target Net Yield:* 18% base + VIP venture growth returns.
            """)

    with st.expander(
        "Q3: What is the 120-Day Lock-in & Maturity Rule in Portfolios?"
    ):
      st.write(
          "A: Every active portfolio follows a strict 120-day lifecycle: **90"
          " days of continuous SIP installments** (accumulation phase) followed"
          " by a **30-day holding lock-in** to optimize startup venture"
          " returns. Withdrawals remain strictly locked until the Target"
          " Principal is 100% achieved and the hold period is cleared."
      )

    with st.expander(
        "Q4: What happens if my E-Mandate / AutoPay installment fails?"
    ):
      st.write(
          "A: If an installment fails due to an insufficient bank balance, a"
          " **5-day grace period** is triggered. Our AI Master Autopilot agent"
          " or manual payment option allows you to clear the missed"
          " installment via UPI/Card to prevent timeline extension."
      )

    with st.expander("Q5: How does the AI Master Autopilot work?"):
      st.write(
          "A: The AI Master Autopilot continuously monitors your compliance,"
          " auto-heals failed transactions using liquidity reserves, optimizes"
          " your streak rewards, and tracks your progress across generations."
      )

    with st.expander(
        "Q6: How do I withdraw my funds after maturity is completed?"
    ):
      st.write(
          "A: Once your target principal is 100% reached, your KYC is verified"
          " (bank mobile matching login ID), and the 30-day holding period"
          " lapses, you can click **'Initiate Withdrawal Request'** under the"
          " **'My Portfolio'** tab for direct net bank credit."
      )

    with st.expander("Q7: What is the Family Wealth Tree feature?"):
      st.write(
          "A: It allows you to add secondary seedlings or beneficiaries (such"
          " as children or spouse) with dedicated milestone goals like Higher"
          " Education or Wedding Funds to build generational wealth."
      )
