---
name: record-session-handoff
description: Record decisions as external notes during an AI agent conversation and hand off safely to the next session. (session memory, handoff, notes, context continuity)
license: MIT
---

# Record Session Handoff

## Purpose

- Record decisions, open questions, and next actions as external notes so that a new session can resume in the same context.

## When to use

- When the conversation context is getting long and you want to switch to a new session
- When you want to work across multiple phases in separate sessions
- When you want to reuse a decision that was made once in future sessions

## Input (optional)

- Target project name
- Current task name
- Storage location for the session log
- Storage location for the latest handoff
- Storage location for persisted decisions
- Decisions / open questions for this session
- First thing to do in the next session

## Steps

1. Identify the project to record notes for.
2. At the start of a session, check the latest handoff at the provided location and clarify continuations from the previous session.
3. During work, extract only the important decisions and separate confirmed from pending.
4. At the end of a session, create or update the session log at the provided location.
5. Update the latest handoff at the provided location with a summary for the next session.
6. Promote only confirmed decisions to the decisions storage location.

## Output format

```md
Session Log:
- Date: YYYY-MM-DD
- Topic: ...
- Decisions:
  - ...
- Open Questions:
  - ...
- Next Actions:
  - ...

Handoff (latest):
- Current Goal: ...
- Must-keep Context:
  - ...
- First Step Next Session:
  - ...
```

## Boundaries

### Always:

- Check the latest handoff at the start of each session
- Leave Decisions / Open Questions / Next Actions at the end of each session
- Record confirmed and unconfirmed items separately

### Ask first:

- When incorporating into existing operational rule documents (AGENTS.md / docs)
- When starting operations without a specified storage location

### Never:

- Treat the conversation history as the only record
- Record unconfirmed items as confirmed in `decisions`
- Write secrets in notes

## Notes (optional)

- Keep one log per session; summarize logs that grow too large before the next session starts.
- Do not over-fix the format; prioritize the required fields (Decisions / Open Questions / Next Actions).
- The output template is in English because session handoffs are referenced by both agents and humans across sessions.
