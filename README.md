# ResolveAI – Real‑Time Human‑in‑the‑Loop Exception Resolution Workbench

## Problem
Operations teams face high volumes of transaction exceptions that require manual investigation. AI can assist, but must never autonomously act on financial decisions.

## Solution
ResolveAI provides a dashboard where reviewers:
- See a queue of flagged transactions
- Ask the AI for explanations and suggested resolutions
- View a **Decision Confidence Score** and **Safety Card**
- Auto‑resolve only when the safety controller permits it
- Maintain a full audit trail

## Architecture
- **Frontend**: Streamlit
- **Backend**: Python services (rule engine, confidence engine, safety controller)
- **Database**: SQLite
- **AI**: OpenAI‑compatible (fallback to deterministic rules)

## Human‑in‑Command
The LLM generates natural‑language explanations but **never** decides whether to act. The deterministic safety controller evaluates:
1. Confidence ≥ threshold
2. No HIGH severity rule triggered
3. No conflicting evidence
4. Amount within autonomous limit

## Getting Started
... (see above)