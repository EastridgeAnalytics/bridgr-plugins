---
name: bridgr
description: Use when the person asks to connect, install or set up Bridgr, or asks about their company's data through Bridgr - how a number came out, what Bridgr found, which systems are connected or still waiting, or a question Bridgr should answer from the company's own systems. Covers bridgr_status, bridgr_what_is_needed, bridgr_findings, bridgr_ask and bridgr_answer.
---

# Bridgr

Bridgr maps what a company's data means and answers questions from its own read-only access to the company's
systems. You reach it through the `bridgr` MCP server, signed in as the person using you.

## Connecting, or not working?

Check this first, in one call at most:

| You see | Do |
|---|---|
| No `bridgr_*` tools, or "unknown tool" | Bridgr isn't connected in this session. Just connected: start a new chat or session. Otherwise fetch and follow https://raw.githubusercontent.com/EastridgeAnalytics/bridgr-plugins/main/setup.md from step 2 |
| The server asks to sign in, 401, "needs authentication" | Sign in again: `/mcp` → bridgr → Authenticate (Claude Code), **Connect** on the plugin or connector (apps), `codex mcp login bridgr` (Codex). The person signs in and clicks Approve in their browser; never ask for a password, key or code |
| "You're not on {company}'s Bridgr list" | Pass on the error's own words: it names who to ask. Once added, they sign in again |

Tell the person what you found and the one step to fix it. Never guess at tool names or work around a missing
connection.

## Which tool

| The person wants | Call |
|---|---|
| Where the company stands, which systems are connected | `bridgr_status` |
| What Bridgr still needs before it can read a system | `bridgr_what_is_needed` |
| What Bridgr noticed and emailed them about | `bridgr_findings` |
| A number, a list or an explanation from the company's data | `bridgr_ask`, then `bridgr_answer` with the ask id |

## Asking

- `bridgr_ask` returns at once with an ask id. Bridgr answers in a minute or two. Call `bridgr_answer` with the id;
  if it says still being answered, wait about a minute and call again. Never ask the same question twice.
- One question at a time per person, 20 a day, shared with Bridgr's screen. A follow-up passes the earlier answer's
  id as `follows`.
- Give the answer in Bridgr's words, with its `answer_page` link. Don't recompute or round Bridgr's numbers.

## Never

- A password, key or token in a tool call or a question. Bridgr strips them and refuses a question that is only a
  password. Passwords go in on Bridgr's screen, under Connections; `bridgr_what_is_needed` says where.
- A promise that Bridgr can change data. It only reads.
