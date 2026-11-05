---
name: bridgr
description: Use when the user asks about their company's data through Bridgr - how a number came out, what Bridgr found, which systems are connected or still waiting, or a question Bridgr should answer from the company's own systems. Covers the bridgr_status, bridgr_what_is_needed, bridgr_findings, bridgr_ask and bridgr_answer tools.
---

# Bridgr

Bridgr maps what a company's data means and answers questions from its own read-only access to the company's
systems. You reach it through the `bridgr` MCP server, signed in as the person using you.

## Which tool

| The person wants | Call |
|---|---|
| Where the company stands, which systems are connected | `bridgr_status` |
| What Bridgr still needs before it can read a system | `bridgr_what_is_needed` |
| What Bridgr noticed and emailed them about | `bridgr_findings` |
| A number, a list or an explanation from the company's data | `bridgr_ask`, then `bridgr_answer` with the ask id |

## Asking

- `bridgr_ask` returns at once with an ask id. Bridgr's agent answers in a minute or two. Call `bridgr_answer`
  with the id; if it says still being answered, wait about a minute and call it again. Do not ask the same
  question twice.
- One question at a time per person, 20 a day (shared with Bridgr's screen); Bridgr answers a few people at
  once. A follow-up passes the earlier answer's id as `follows`.
- Give the answer in Bridgr's words, with its `answer_page` link for the full list and how it was worked out.
  Do not recompute or round Bridgr's numbers.

## Never

- Never put a password, key or token in any tool call or in a question. Bridgr takes such lines out and refuses a
  question that is only a password. Passwords go in on Bridgr's own screen, Connections (the `how` field of
  `bridgr_what_is_needed` says where).
- Bridgr never writes to the company's systems; do not promise that it can change data.

## If Bridgr isn't working

Check this before anything else, and don't spend more than one call working it out:

| You see | Do |
|---|---|
| No `bridgr_*` tools at all, or "unknown tool" | Bridgr isn't connected in this session. If it was just connected, start a new chat or session. Otherwise follow https://raw.githubusercontent.com/EastridgeAnalytics/bridgr-plugins/main/setup.md from step 2 |
| The server asks to sign in, or 401 / "needs authentication" | Sign in again: `/mcp` → bridgr → Authenticate (Claude Code), `codex mcp login bridgr` (Codex), or **Connect** on the connector (chat apps) |
| "Not on any company's list" / "You're not on {company}'s Bridgr list" | Pass on the error's own words: it names who to ask. Once added, they sign in again |

Tell the person what you found and the one step to fix it. Never guess at tool names or work around a missing
connection.
