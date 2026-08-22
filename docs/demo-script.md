# ResolveAI Demo Script (5 minutes)

## 0:00 – 0:40 – Business Problem
"Operations teams receive hundreds of transaction exceptions daily. Manual investigation is slow and costly. AI can help, but financial decisions must never be made autonomously. We need a human‑in‑the‑loop system that *assists* but does not *decide*."

## 0:40 – 1:20 – Architecture
"ResolveAI separates:
- **Rule Engine** (deterministic) – flags transactions.
- **Confidence Engine** – computes a Decision Confidence Score.
- **Safety Controller** – decides if auto‑resolution is permitted based on confidence, severity, conflicts, and amount limits.
- **LLM** – only generates explanations and suggestions, never controls execution."

## 1:20 – 2:10 – Normal Exception (EX-1001)
- Open dashboard → see queue.
- Select EX-1001 (Amount mismatch).
- Click **Explain** → shows grounded reason.
- Click **Suggest Resolution** → shows recommended action.
- Safety Card shows **Auto‑Resolve Permitted** (confidence 91%, no high‑risk rules).

## 2:10 – 3:10 – High‑Risk Case (EX-1003)
- Select EX-1003 (₹125,000, many triggers).
- Safety Card shows **Auto‑Resolve Blocked**.
- Reasons: Confidence below threshold, High‑severity rule triggered, amount exceeds limit.
- Human buttons (Approve/Reject/Escalate) are active.

## 3:10 – 4:00 – Threshold Change Demonstration
- Go to **Rules** panel.
- Change Confidence Threshold from 85% to 90%.
- Return to EX-1001 (confidence 87%) → now **Blocked**.
- Change back to 85% → becomes **Permitted** again.
- Shows that the threshold directly controls autonomy.

## 4:00 – 5:00 – Auto‑Resolve a Safe Case & Audit
- Select EX-1007 (clean, confidence 94%).
- Click **Auto‑Resolve**.
- Queue updates – EX-1007 disappears from Open.
- Dashboard metrics refresh.
- Audit Trail shows the event with timestamp, actor, action, confidence, and rule results.
- Summarise: "The system enforces safety, provides full transparency, and keeps humans in command."

## Closing
"ResolveAI is a working prototype that demonstrates how to build reliable, safe, and auditable AI‑assisted exception resolution."