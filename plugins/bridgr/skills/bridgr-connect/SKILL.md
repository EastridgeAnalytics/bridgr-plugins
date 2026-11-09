---
name: bridgr-connect
description: Use when the person asks to connect, install or set up Bridgr, or pastes a Bridgr setup prompt. Walks them through connecting this assistant to their own company's Bridgr, has them sign in and approve, and checks it works.
---

# Connect to Bridgr

Bridgr answers questions from a company's own systems, read-only. Every company has its own Bridgr at its own
address. You connect this assistant to **the person's company's Bridgr only**, then they sign in and approve.

## Rules

- Never ask for, accept or handle a password, key, token or sign-in code. Sign-in happens in the person's browser.
- The person clicks **Approve** themselves. Never click it for them or tell them it's safe to approve something they
  didn't start.
- Use only the address the person gives you from their own Bridgr email. It ends in `/mcp` once you add it, and it
  is a subdomain of `eastridge-analytics.com` (hosted by Eastridge) or on their company's own domain
  (self-hosted). If it's anything else, stop and ask them to check
  the welcome or Connect data email from Bridgr.
- Don't add a second Bridgr if one is already connected. Don't connect company systems: that's done on Bridgr's own
  screen, under Connections.

## No assistant yet?

If they don't have an assistant, help them choose and install one before connecting Bridgr. Follow the
**No assistant yet?** section in https://raw.githubusercontent.com/EastridgeAnalytics/bridgr-plugins/main/setup.md. It has the
current official download links for Claude Desktop and ChatGPT desktop, and install commands for Claude Code
and Codex CLI. Pick a chat app for no terminal commands, or a CLI to run commands locally, on Linux or on a server.
Run CLI install commands yourself if you can, on the person's chosen computer only. For desktop downloads and
sign-in, give one step at a time and wait for "done". Never handle passwords, tokens, codes or approval.

Claude Desktop is not a headless server app. Anthropic now offers a Linux desktop beta, so the old advice that
there is no Linux version is out of date. Use the official instructions linked in the public setup guide.
After installation and the person's own sign-in, use steps 1 and 2 of that guide, then step 3 to connect the
chosen assistant. In this skill's existing flow, continue at step 0 below instead. Installation alone is not a
successful Bridgr connection.

## 0. Already set up?

If you have the `bridgr_status` tool, call it. If it answers, Bridgr is connected: skip to step 4. If it says to sign
in or authenticate, the address is already set (your company's plugin carries it): skip to step 3 and have them
click **Connect** on the Bridgr connector (Claude Desktop: **Settings → Customize → Plugins → Bridgr → Connectors**;
Claude Code: `/mcp` → **bridgr** → **Authenticate**). Only if there's no `bridgr_status` tool at all, start at step 1.

## 1. Ask the one thing you can't know

Ask: "What's your company's Bridgr address? It's in your Bridgr welcome or Connect data email, for example
`https://yourcompany.eastridge-analytics.com`." Tidy it before you use it: keep `https://` and the host only, and
drop any trailing `/`, `/mcp` or anything after the host. That tidy form is the **company address**; the company
address plus `/mcp` is the **address**. (A trailing slash or a doubled `/mcp` makes the connection fail.)

If they have no Bridgr email, their company isn't set up yet: send them to https://www.bridgr-platform.com/contact and stop.

## 2. Pick the way in, for the assistant you are

Work out which assistant you're running in. Only ask the person if you can't tell, and offer just these choices:

**A. A chat app: Claude (claude.ai, Desktop, mobile) or ChatGPT.** Walk them through it one step at a time and wait
for each "done":
1. Claude: **Settings → Connectors → Add custom connector**. ChatGPT: **Settings → Apps & Connectors → Create**
   (developer mode may need to be on).
2. Name: `Bridgr`. URL: the address. No key, no client ID.
3. Click **Add**, then **Connect**.

**B. Claude Code.** If the Bridgr plugin is already installed (you can see this skill because of it), run
`/plugin configure bridgr@bridgr`, enter the company address (host only, no `/mcp`, no trailing `/`), then
`/reload-plugins`. Otherwise
offer two options and let them choose:
- *The Bridgr plugin* (adds a skill that knows Bridgr's tools):
  `/plugin marketplace add EastridgeAnalytics/bridgr-plugins`, then `/plugin install bridgr@bridgr`, and give it
  the company address (host only, no `/mcp`, no trailing `/`) when it asks.
- *Just the connector*: run `claude mcp add --transport http bridgr <address>`.

Then `/mcp` → **bridgr** → **Authenticate**.

**C. Codex.** Run `codex mcp add bridgr --url <address>`, then `codex mcp login bridgr`. (The Bridgr plugin for
Codex brings this skill and the tool guide; Codex plugins can't ask for an address yet, so the connector is always
this one command.)

**D. Anything else that takes a remote MCP server** (Cursor, Grok, others): add one with the address, sign-in
OAuth, no key.

(One-click install from Claude's and ChatGPT's directories isn't available yet. Don't offer it.)

## 3. Sign in (the person does this)

Their browser opens Bridgr: they enter their work email, open the emailed link ("Your link to <company>'s map",
good for 15 minutes), and see a page naming this assistant and their company. They check both, then click
**Approve**. Tell them what to expect before it opens.

## 4. Check it

Call `bridgr_status`. Tell them their company and which systems are connected, then call `bridgr_what_is_needed`
and say what's still missing and that it's added on Bridgr's screen, under Connections, never in this chat.
Finish with: "Bridgr is connected. Try: *How many deals were booked last week?*"

## If something goes wrong

| You see | Tell the person |
|---|---|
| No email arrives | They may not be on the list. Ask whoever runs Bridgr at their company to add them |
| "That request has run out" | It lasts 10 minutes. Start the connect step again |
| 401 or "needs authentication" later | Sign in again: Authenticate (Claude Code), `codex mcp login bridgr`, or Connect (chat apps) |
| They said No by mistake | Start again from the connect step |
| "Add custom connector" or **Connect** is greyed out, or "Ask an organization owner" | Their company's Claude or ChatGPT admin has to allow it. The admin downloads the company's Bridgr plugin from Bridgr (**Settings → Connected assistants → Download for Claude**), uploads it and publishes it to the organization. Then it's already installed for everyone |
| They want to stop | Disconnect here, or in Bridgr: **Settings → Connected assistants** |
