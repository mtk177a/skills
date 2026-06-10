# record-session-handoff evals

## Iter 0 — Static check

- description and body are internally consistent on "cross-session handoff operation"
- Session Log and Handoff (latest) roles are distinguished
- confirmed decisions and open questions are separated
- behavior when save destination is unspecified is clearly defined: stop and ask
- at least one `[critical]` assertion is identified per scenario

## Scenarios

### Scenario A: Long task handoff to the next session

Decisions and pending items are mixed in the current session state. The skill must produce a handoff that allows the next session to resume immediately.

Requirements checklist:
1. [critical] Decisions and Open Questions are not conflated
2. First Step Next Session is stated concretely
3. Session Log and Handoff roles are kept distinct
4. Only confirmed decisions are promoted to the decisions destination

### Scenario B: Save destination unspecified

A handoff is requested but neither the session log nor the latest handoff save destination has been specified. The skill must not begin the handoff workflow without a destination.

Requirements checklist:
1. [critical] Missing save destination is treated as an Ask-first stop condition
2. The conversation history alone is not used as the sole record
3. Required input fields are made clear
4. Open Questions are not confirmed as decisions

### Scenario C: Open questions must not be promoted to decisions (boundary)

Two approaches were discussed but no decision was reached. The completed work is clearly done. The skill must keep the undecided approach in Open Questions, not in Decisions.

Requirements checklist:
1. [critical] Undecided approach is not written as a decision
2. Open Questions section is present and contains the undecided item

## Failure Pattern Ledger

- `decisions and open questions conflated`
- `handoff written without destination`
- `session log and latest handoff blurred`
- `open questions promoted to durable decisions`
