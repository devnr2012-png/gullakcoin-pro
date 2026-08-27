def get_risk_plugin_response(query):
  q = query.lower()
  if any(k in q for k in ["fail", "payment fail", "insufficient"]):
    return (
        "⚠️ **Failed E-Mandate Resolution (Risk Plugin Agent)**: If an"
        " installment fails due to insufficient bank balance, a **5-day grace"
        " period** becomes active. Clear missed installments manually using"
        " UPI/Card."
    )
  return None
