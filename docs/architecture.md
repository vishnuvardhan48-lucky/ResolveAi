# System Architecture

## Data Flow
1. Synthetic transactions are seeded in SQLite.
2. When a transaction is viewed, the **Rule Engine** evaluates all enabled rules against its data.
3. Rule results feed into the **Confidence Engine** to compute a Decision Confidence Score (0–100).
4. The **Safety Controller** checks the score, severity, conflicts, and limits.
5. The **UI** shows the Safety Card and enables/disables the Auto‑Resolve button.
6. When Auto‑Resolve is clicked, the **Resolution Service** updates the transaction status and logs the event via the **Audit Service**.

## Decision Separation
- **LLM**: Generates only explanatory text (Explain, Suggest, Chat).
- **Rules & Confidence**: Deterministic and auditable.
- **Safety Controller**: Sole authority for execution permission.

...