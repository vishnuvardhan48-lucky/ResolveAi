# Assumptions

- All transactions are synthetic and do not represent real customer data.
- "Resolution" is a simulated action – no external financial execution occurs.
- Confidence is a **decision‑support score**, not a statistical probability.
- High‑risk cases (e.g., amount > ₹50,000) always require human approval.
- Thresholds are configurable per session; persisted in database settings.
- The prototype is single‑tenant and does not implement user authentication.