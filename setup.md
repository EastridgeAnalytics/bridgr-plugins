# Connect this assistant to Bridgr

You are an AI assistant connecting yourself to the Bridgr of the company the person works for. Bridgr answers
questions from the company's own systems, only reads, and works as the person once they sign in. These instructions
are published at https://github.com/EastridgeAnalytics/bridgr-plugins/blob/main/setup.md. Stay with the person until
a Bridgr tool call succeeds.

## Rules

- Never ask for, accept or repeat a password, API key, token or sign-in link. Sign-in happens in the person's browser.
- The person clicks **Approve** themselves.
- Connect only to the person's own company's Bridgr, always `https://`: a subdomain of `eastridge-analytics.com`, or
  an address on the company's own domain. The one exception is a trial on this same computer,
  `http://localhost:8080`. Anything else: stop, and have them check with whoever set up Bridgr.
- Run commands yourself when you can. When you can't (a chat app), give one step at a time and wait for "done".
- Don't connect company systems. That happens on Bridgr's own screen, under Connections.

## 1. The address

If the person gave an address, use it. Otherwise ask: "What's your company's Bridgr address? It's what you open
Bridgr at in your browser, like `https://yourcompany.eastridge-analytics.com`. Whoever set up Bridgr at your company
has it." No Bridgr at their company yet: https://www.bridgr-platform.com/contact, and stop.

Keep `https://` and the host, nothing after it. That is the **Bridgr address**. The Bridgr address plus `/mcp` is
the **MCP URL**. A trailing slash or a doubled `/mcp` fails.

If you can run commands, check it:

    curl -s -o /dev/null -w "%{http_code}" https://<host>/.well-known/oauth-protected-resource/mcp

`200` means a live Bridgr. Anything else: re-read the address with the person, then Troubleshooting.

A Bridgr reachable only inside the company's network works from Claude Code, Codex and other assistants on the
person's computer while they're on the network or VPN. Claude's and ChatGPT's apps connect from the internet and
can't reach it.

## 2. Already connected?

If you have a `bridgr_status` tool, call it. It answers: go to step 5. It says to sign in: go to step 4. A Bridgr
connector exists with a different address: ask the person which is theirs before changing anything. Never add a
second Bridgr.

## 3. Add Bridgr to the assistant you are

**Claude Code** (CLI or IDE). Run both. They install the Bridgr plugin: the connector and the guide to its tools.

    claude plugin marketplace add EastridgeAnalytics/bridgr-plugins
    claude plugin install bridgr@bridgr

It asks for the Bridgr address (host only). Then the person runs `/reload-plugins`, then `/mcp` → **bridgr** →
**Authenticate**. If the plugin can't be installed (not found, or no route to GitHub), add the connector directly:

    claude mcp add --transport http --scope user bridgr <MCP URL>

**Claude Desktop.** The person uploads a zip: **Settings → Customize → Plugins → Add → Upload plugin**. Their
company's Bridgr hands out one with the address already in it, at **Settings → Connected assistants → Download for
Claude**; the generic one is on this repo's Releases page and asks for the address. Then **Bridgr → Connect**.
A Claude Team or Enterprise admin uploads it once, clicks **Publish to org** and picks **Installed by default**:
everyone has it.

**Anything else** (Codex, claude.ai, ChatGPT, Cursor, VS Code, Windsurf, any MCP client):
[setup/other-assistants.md](setup/other-assistants.md), then come back here.

## 4. Sign in and approve (the person does this)

Tell them what to expect first. Their browser opens their company's Bridgr. A page names **this assistant** and
**their company**. They check both and click **Approve**. The browser hands back to the assistant.

If the page asks them to sign in first: where it has an email box, they ask for a link there. Otherwise they open
the one-time sign-in link their Bridgr owner sent them, then connect again. No link: the owner makes one at
Settings, People.

"Account mismatch" (Claude): the browser is signed in to a different Claude account than the app. **Sign out and
switch account**, then connect again.

## 5. Check it works

Call `bridgr_status`. Tell the person their company, who they're signed in as, and which systems are connected.
Call `bridgr_what_is_needed` and say what's still missing, and that it's added on Bridgr's screen under
Connections, never in this chat. Finish: "Bridgr is connected. Try: *How many deals were booked last week?*"

No Bridgr tools in this session: say exactly what to restart or reload (step 3), then pick up at step 2.

## Troubleshooting

| What happens | What to do |
|---|---|
| The address check isn't `200` | Re-check the address (step 1). Still failing: their Bridgr may be down; ask whoever runs it |
| "You're not on {company}'s Bridgr list" | The error names who to ask. Once added, sign in again |
| "That request has run out" or "already answered" | The approval page lasts 10 minutes. Start step 3's connect step again |
| They clicked **No** by mistake | Start step 3's connect step again |
| **Upload plugin**, **Add custom connector** or **Connect** is greyed out, or "Ask an organization owner" | Their company's Claude or ChatGPT admin has to allow it, or (Claude) publish the company's Bridgr plugin to the org |
| Bridgr tools don't appear after connecting | Start a new chat or session; CLI: restart it. Check Bridgr is on in the tools menu. Then step 2 |
| 401, "needs authentication" or "invalid token" later | Sign in again: `/mcp` → bridgr → Authenticate (Claude Code), **Connect** on the plugin or connector (apps), `codex mcp login bridgr` (Codex) |
| `plugin marketplace add` fails | No route to GitHub. Claude Code: the direct `claude mcp add` line in step 3. Codex: skip the plugin lines |
| A Bridgr connector exists with a different address | Ask which is theirs. Remove the wrong one, then connect again |
| Anything else | Tell them the exact error, and that https://www.bridgr-platform.com/contact can help |

## Disconnect

Remove the plugin or connector in the assistant (`claude mcp remove bridgr`, `codex mcp remove bridgr`, or the
app's settings), or in Bridgr under **Settings → Connected assistants**, which ends that assistant's access at once.
