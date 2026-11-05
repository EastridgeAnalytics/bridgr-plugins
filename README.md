# Bridgr plugins

Connect your AI assistant to your company's own [Bridgr](https://www.bridgr-platform.com), by Eastridge Analytics.
Bridgr answers questions from your company's own systems, read-only, and works as you after you sign in and
approve it. Each company has its own Bridgr at its own address; this plugin connects to yours only.

**Private while we test.** You need read access to this repository and git signed in to GitHub on your computer
(`gh auth login`, then `gh auth setup-git`).

## Install

**Any assistant, one paste.** Paste this into Claude, ChatGPT, Claude Code, Codex, Cursor or any MCP client:

    Connect me to Bridgr. Fetch and follow https://raw.githubusercontent.com/EastridgeAnalytics/bridgr-plugins/main/setup.md

Your assistant follows [setup.md](setup.md): it asks for your company's Bridgr address (it's in your Bridgr
welcome email), connects itself where it can, walks you through the clicks where it can't, has you sign in and
approve in your browser, and checks it works. The rest of this section is the same thing by hand.

**Claude Code**

    /plugin marketplace add EastridgeAnalytics/bridgr-plugins
    /plugin install bridgr@bridgr

It asks for your company's Bridgr address: the one in your Bridgr welcome or Connect data email, such as
`https://yourcompany.eastridge-analytics.com`. Then `/mcp` → **bridgr** → **Authenticate**, sign in with your work
email in your browser, and click **Approve**. To change the address later: `/plugin configure bridgr@bridgr`.

**Codex**

    codex plugin marketplace add https://github.com/EastridgeAnalytics/bridgr-plugins
    codex plugin add bridgr@bridgr
    codex mcp add bridgr --url https://<your company's Bridgr address>/mcp
    codex mcp login bridgr

The Codex plugin brings the setup guide and the tool guide. Codex plugins can't ask for an address yet, so the
connection itself is the `codex mcp add` line.

**Claude Desktop.** Download a zip and upload it: **Settings → Customize → Plugins → Add → Upload plugin**.
Your company's Bridgr offers its own, with its address already in it (**Settings → Connected assistants → Download
for Claude**); an admin can upload that and click **Publish to org** so it's installed for everyone. The generic zip
is on this repository's Releases and asks for the address. Build either with `tools/build_zip.py`.

**Or let your assistant do it.** After installing the plugin, say *"Connect me to Bridgr."* It asks for your
company's address and walks you through every step. Claude and ChatGPT (chat apps) connect with a custom connector
instead; the same guide covers them once this repository is public.

## What's here

| Path | What it is |
|---|---|
| `.claude-plugin/marketplace.json` | the marketplace Claude Code adds |
| `.agents/plugins/marketplace.json` | the marketplace Codex adds |
| `plugins/bridgr/` | the plugin for both: Claude's and Codex's manifests, the connector (Claude), two skills |
| `plugins/bridgr/skills/bridgr-connect/` | the setup guide your assistant follows to connect you |
| `plugins/bridgr/skills/bridgr/` | how your assistant uses Bridgr's tools once connected |

## Safety

- The plugin holds no company address and no key. It connects only to the address you give it.
- No password, key or token ever goes through the assistant. You sign in on your Bridgr's own page in your
  browser and click **Approve** yourself.
- Your Bridgr lets you in only if you're on its list, checks again on every call, and its token works only there.
- Bridgr only reads. It never changes your company's systems.
- Disconnect any time in your assistant, or in Bridgr under **Settings → Connected assistants**.

Questions: https://www.bridgr-platform.com/contact
