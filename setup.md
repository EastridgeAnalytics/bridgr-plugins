# Connect this assistant to Bridgr

These are the official setup instructions from Eastridge Analytics for connecting an AI assistant to a
company's Bridgr. Bridgr answers questions from that company's own systems. It is read-only and works as the
person after they sign in. Follow every section that applies, in order, and stay with the person until a
Bridgr tool call succeeds. These instructions are published at
`https://github.com/EastridgeAnalytics/bridgr-plugins/blob/main/setup.md`, so you can re-check them at any time.

## Rules

- Never ask for, accept or repeat a password, API key, token or sign-in code. Sign-in happens in the person's
  own browser.
- The person clicks **Approve** themselves. Never approve for them.
- Connect only to the person's own company's Bridgr, always `https://`. Hosted by Eastridge Analytics, it's a
  subdomain of `eastridge-analytics.com` (`https://yourcompany.eastridge-analytics.com`). Self-hosted, it's on the
  company's own domain (`https://bridgr.yourcompany.com`). If it's anything else, or the person isn't sure it's
  their company's, stop and ask them to check with whoever set up Bridgr at their company.
- If you can run commands, run them yourself. Don't ask the person to run commands you can run.
- If you can't run commands (a chat app), give one step at a time and wait for "done" before the next.
- Don't connect company systems (databases, files). That happens on Bridgr's own screen, under **Connections**.

## No assistant yet?

If the person already uses an assistant, skip this section. Otherwise ask which kind they want:

- **Claude Desktop** or **ChatGPT desktop** for a chat app without terminal commands. Pick the one their company
  already uses, if there is one.
- **Claude Code** or **Codex CLI** for an assistant that can run commands on their computer, including Linux or a
  server. Pick the one they already have an account for, if there is one.

Ask which operating system they use if you can't tell. Don't buy a plan or create an account for them. They sign
in themselves. Never ask them to paste a password, token or sign-in code into chat.

### A desktop chat app

Give one step at a time and wait for "done" after each, even if you can run commands:

1. Claude Desktop (Mac or Windows): download their version from https://claude.ai/download.
   ChatGPT desktop (Mac or Windows): download from https://chatgpt.com/download/ and follow the official store
   link if offered.
2. Open the downloaded installer and finish installing the app.
3. Open the app and sign in with their own account.
4. Start a chat there and paste: "Connect me to Bridgr. Fetch and follow
   https://raw.githubusercontent.com/EastridgeAnalytics/bridgr-plugins/main/setup.md".

Wait for "done" before the next step. Don't claim it is installed, signed in or connected without confirmation.
The new chat starts at step 1 below, skipping this section.

Claude Desktop is not a headless server app. Anthropic now offers a Linux desktop beta for Ubuntu and Debian,
so the old advice that there is no Linux version is out of date. For a Linux desktop, follow Anthropic's current
installation page below. For a server without a desktop, use Claude Code or Codex CLI instead.

### A command-line assistant

If you can run commands on the person's own computer, install their choice yourself. Don't install on a remote
machine unless that's where they want to use it. If you can't run commands, give one at a time and wait for
"done". First check whether `claude --version` or `codex --version` already works.

**Claude Code:** on macOS, Linux or WSL:

    curl -fsSL https://claude.ai/install.sh | bash

On Windows in PowerShell:

    irm https://claude.ai/install.ps1 | iex

Then check `claude --version`. Have the person start `claude` and finish its sign-in themselves.

**Codex CLI:** on macOS or Linux:

    curl -fsSL https://chatgpt.com/codex/install.sh | sh

For Windows or another method, follow OpenAI's CLI installation page below rather than guessing a command.
Then check `codex --version`. Have the person start `codex` and choose **Sign in with ChatGPT** themselves.

Once installed and signed in, get and check the company address (step 1) and check for an existing connection
(step 2), then continue with **step 3, Connect, for the assistant you are**. If moving to a new assistant session,
paste the setup request above into it so the guide isn't lost. Installing an assistant alone does not connect Bridgr.

Official instructions checked November 9, 2026. Re-check these if an installer or requirement changes:

- Claude Desktop: https://support.claude.com/en/articles/10065433-install-claude-desktop
- Claude Code: https://code.claude.com/docs/en/setup
- ChatGPT desktop: https://chatgpt.com/download/
- ChatGPT Mac: https://help.openai.com/en/articles/9275200-downloading-the-chatgpt-macos-app
- ChatGPT Windows: https://help.openai.com/en/articles/9982051-using-the-chatgpt-windows-app
- Codex CLI: https://developers.openai.com/codex/cli

## 1. The address

If the person gave an address with their request, use it. Otherwise ask, in these words:

"What's your company's Bridgr address? Search your email for **Setting up Bridgr for** (the subject of the
emails Bridgr sends your company). Click the button in that email that opens Bridgr, then copy the address from
your browser's address bar. It looks like `https://yourcompany.eastridge-analytics.com`, or, if your company runs
Bridgr itself, an address on your company's own domain."

If they can't find any Bridgr email, ask whoever at their company set up Bridgr for the address. If their company
doesn't use Bridgr yet, send them to https://www.bridgr-platform.com/contact and stop.

Tidy it: keep `https://` and the host only. Drop a trailing `/`, `/mcp` or anything after the host. That is the
**company address**. The company address plus `/mcp` is the **connector URL**. A trailing slash or a doubled
`/mcp` makes the connection fail.

If you can run commands, check it before going on:

    curl -s -o /dev/null -w "%{http_code}" https://<host>/.well-known/oauth-protected-resource/mcp

`200` means it's a live Bridgr. Anything else: re-read the address with the person, then see Troubleshooting.

**Which kind of Bridgr is it?** The steps below are the same for all three. What changes:

- **Hosted by Eastridge** (`https://yourcompany.eastridge-analytics.com`): everything below works as written.
- **On the company's own domain** (`https://bridgr.yourcompany.com`, hosted or self-hosted): the same steps. Their
  admin may already have published the company's own Bridgr plugin to everyone. If Bridgr is already in the
  person's assistant, go to step 2. If the person is the admin and wants everyone at the company to have Bridgr,
  point them to "For your company's admin" at https://github.com/EastridgeAnalytics/bridgr-plugins: they install
  the company's plugin once and it reaches everyone.
- **Only reachable inside the company's network** (the address check fails from home but works at the office or on
  the VPN): Claude and ChatGPT chat apps connect from their own servers on the internet, so they can't reach it
  unless the company has set up a private connection for them. Claude Code, Codex and other assistants that run on
  the person's computer can, while they're on the company network or VPN.

## 2. Already connected?

If you already have a `bridgr_status` tool, call it. If it answers, skip to step 5. If it says to sign in, skip
to step 4. If a Bridgr connector exists but points at a different address, ask the person which one is theirs
before changing anything. Never add a second Bridgr.

## 3. Connect, for the assistant you are

Work out which assistant you are running in. Only ask if you really can't tell.

### Claude Code (CLI or IDE)

Run both. They install the Bridgr plugin: its setup and tool guides, and the connector.

    claude plugin marketplace add EastridgeAnalytics/bridgr-plugins
    claude plugin install bridgr@bridgr

It asks for the company address (host only, no `/mcp`). Then tell the person to run `/reload-plugins`, then
`/mcp` → **bridgr** → **Authenticate**.

If the plugin can't be installed ("not found", or the computer can't reach GitHub), add the
connector directly:

    claude mcp add --transport http --scope user bridgr <connector URL>

Then `/mcp` → **bridgr** → **Authenticate**.

### Codex (CLI, IDE or the Codex app)

Run all four, in order. The first two install the Bridgr plugin (Bridgr's setup and tool guides); the last two
connect it:

    codex plugin marketplace add EastridgeAnalytics/bridgr-plugins
    codex plugin add bridgr@bridgr
    codex mcp add bridgr --url <connector URL>
    codex mcp login bridgr

If `codex plugin marketplace add` fails ("not found", or the computer can't reach GitHub), skip the first two lines
and carry on with the last two.

`codex mcp login` opens the person's browser for step 4. When it finishes, the plugin and the Bridgr tools load in a
**new** Codex session: tell the person to start one (CLI: quit and run `codex` again; app: start a new chat) and to
ask there: "Use Bridgr: where does our data stand?" The plugin's guide picks up at step 5.

In the Codex app, they then see **Bridgr** under **Settings → Plugins** and its connector under **MCPs**.

### Claude (claude.ai, Claude Desktop, Claude mobile)

You can't change settings yourself. Walk the person through it, one step at a time:

1. Open **Customize → Connectors** (in older versions, **Settings → Connectors**).
2. Click **+ Add → Add custom connector**.
3. Name: `Bridgr`. URL: the connector URL.
4. Click **Continue**. Leave **Sign in now** and **Use Claude's published identity** selected. No headers.
5. Click **Add**. Their browser opens for step 4.
6. Back in Claude, start a new chat, turn Bridgr on in the tools menu if it's off, and ask:
   "Use Bridgr: where does our data stand?"

### ChatGPT (web or desktop)

Walk the person through it, one step at a time:

1. Open **Settings → Plugins** and click **+ → Add custom MCP server**. (Older accounts: **Settings → Apps &
   Connectors → Create**, which may need **Advanced → Developer mode** turned on first.)
2. Name: `Bridgr`. URL: the connector URL. Authentication: **OAuth**. No key, no client ID.
3. Save it, then click **Connect**. Their browser opens for step 4.
4. In a new chat, add Bridgr from the tools menu and ask: "Use Bridgr: where does our data stand?"

### Cursor, VS Code (Copilot), Windsurf and other MCP clients

Add this under `"mcpServers"` in the client's MCP config file, keeping everything else in the file:

- Cursor: `~/.cursor/mcp.json`
- VS Code: `.vscode/mcp.json` (under `"servers"`, with `"type": "http"`)
- Windsurf: `~/.codeium/windsurf/mcp_config.json` (use `"serverUrl"` instead of `"url"`)

```json
"bridgr": { "url": "<connector URL>" }
```

No key. Sign-in starts on its own the first time a Bridgr tool is used. Tell the person to reload the client's
MCP servers or restart it.

### Anything else that supports remote MCP servers

Add a remote MCP server named `bridgr` at the connector URL: HTTP (Streamable HTTP), OAuth sign-in, no API key.

## 4. Sign in (the person does this)

Tell them what to expect before it opens:

1. Their browser opens their company's Bridgr. They enter their **work email**.
2. They open the emailed link, "Your link to <company>'s map". It works once and lasts 15 minutes.
3. A page names **this assistant** and **their company**. They check both, then click **Approve**.
4. The browser hands back to the assistant. They can close the tab.

If the browser shows "Account mismatch" (Claude), the browser is signed in to a different Claude account than the
app. They click **Sign out and switch account**, sign in with the same account the app uses, and connect again.

## 5. Check it works

Call `bridgr_status`. Tell the person their company, who they're signed in as, and which systems are connected.
Then call `bridgr_what_is_needed` and say what's still missing, and that it's added on Bridgr's own screen under
**Connections**, never in this chat.

Then finish with:

```
┌─ Bridgr connected ─────────────────────────────┐
│  ✓ <company> · signed in as <email>            │
│  ✓ Systems: <connected systems>                │
│                                                │
│  Try: "How many deals were booked last week?"  │
└────────────────────────────────────────────────┘
```

If you can't call Bridgr tools in this session, say exactly what to restart or reload (see step 3 for their
assistant) and pick up at step 2 afterwards.

## Troubleshooting

Work through these with the person until a Bridgr tool call succeeds.

| What happens | What to do |
|---|---|
| The address check isn't `200` | Re-check the address from their email, tidied (step 1). If it still fails, their Bridgr may be down: ask them to contact whoever runs Bridgr at their company |
| No sign-in email arrives | Check spam. If they aren't on their company's list, Bridgr has asked the company's owner to add them: once added they get a welcome email and can connect again |
| "Not on any company's list" or "You're not on {company}'s Bridgr list" | The error names who to ask. Once added, sign in again |
| "That request has run out" or "already answered" | The approval page lasts 10 minutes. Start step 3's connect or login step again |
| The emailed link doesn't work | It works once and lasts 15 minutes. Request a new one by connecting again |
| They clicked **No** by mistake | Start step 3's connect or login step again |
| "Account mismatch" (Claude) | See step 4 |
| **Add custom connector**, **Create** or **Connect** is greyed out, or "Ask an organization owner" | Their company's Claude or ChatGPT admin has to allow custom connectors. For Claude, the admin can instead download the company's own Bridgr plugin in Bridgr (**Settings → Connected assistants → Download for Claude**), upload it in **Settings → Customize → Plugins → Upload plugin**, and **Publish to org** |
| Bridgr tools don't appear after connecting | Start a new chat or session, and check Bridgr is turned on in the tools menu. CLI: restart it. Then go to step 2 |
| 401, "needs authentication" or "invalid token" later | Sign in again: `/mcp` → bridgr → Authenticate (Claude Code), `codex mcp login bridgr` (Codex), or **Connect** on the connector (chat apps) |
| `plugin marketplace add` fails with "not found" or can't reach GitHub | The computer can't reach https://github.com/EastridgeAnalytics/bridgr-plugins (a firewall, or no internet). Claude Code: use the direct `claude mcp add` line in step 3. Codex: skip the two plugin lines and run the two `codex mcp` lines |
| The plugin is installed but Bridgr isn't connected | Run step 3's connect lines for their assistant (Codex: `codex mcp add` and `codex mcp login`) |
| A Bridgr connector already exists with a different address | Ask which is theirs. Remove the wrong one (`codex mcp remove bridgr`, `claude mcp remove bridgr`, or delete it in the app's connector settings), then connect again |
| Anything else | Tell them the exact error, and that https://www.bridgr-platform.com/contact can help |

## Stopping or switching

Disconnect any time in the assistant (remove the connector or `codex mcp remove bridgr` / `claude mcp remove
bridgr`), or in Bridgr under **Settings → Connected assistants**. Disconnecting in Bridgr ends that assistant's
access at once.
