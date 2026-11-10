# Bridgr plugins

Connect your AI assistant to your company's own [Bridgr](https://www.bridgr-platform.com), by Eastridge Analytics.
Bridgr answers questions from your company's own systems, read-only, and works as you after you sign in and
approve it.

## Start here: which one are you?

**Setting up Bridgr for your company** (you bought it, or want to). Paste this into Claude Code, Codex or any AI
assistant that can run commands on your server:

    Install Bridgr for my company. Fetch and follow https://raw.githubusercontent.com/EastridgeAnalytics/bridgr-plugins/main/install.md

**Your company already has Bridgr, and you want it in your assistant.** Paste this into Claude, ChatGPT, Claude
Code, Codex, Cursor or any MCP client:

    Connect me to Bridgr. Fetch and follow https://raw.githubusercontent.com/EastridgeAnalytics/bridgr-plugins/main/setup.md

Everything below is detail for admins and for doing it by hand.

## Run Bridgr on your own server (self-hosted)

[install.md](install.md) is a short page an assistant follows. It opens one more page from [install/](install/)
only when it needs it: [buying](install/buy.md), [a server behind HTTPS](install/proxy.md),
[a trial on one computer](install/local-trial.md), [a web address](install/web-address.md),
[every terminal command](install/terminal.md), [the team](install/team.md), [updates and cancelling](install/run-it.md),
[fixing problems](install/troubleshooting.md), and [installing by hand](install/by-hand.md).

## For your company's admin: install it once for everyone

If your company runs Bridgr on its own domain (self-hosted), or you want everyone to have Bridgr without each
person setting it up, install **your company's own Bridgr plugin** once for your organization. It has your Bridgr's
address built in, so people never type it: the first time they use Bridgr, they sign in with their work email and
click **Approve**, and that's all.

1. **Get your company's plugin.** In your Bridgr, open **Settings → Connected assistants → Download for Claude**
   (or **Download for Codex**). Or build it from this repository:
   `python3 tools/build_zip.py --company "Your Company" --url https://bridgr.yourcompany.com`
2. **Claude (Team or Enterprise):** an Owner uploads it in **Settings → Customize → Plugins → Add → Upload
   plugin**, then **Publish to org** and choose **Installed by default** (or **Required**). Everyone gets it.
3. **ChatGPT (Business or Enterprise):** an admin turns on developer mode / custom MCP apps for the workspace,
   creates an app with your Bridgr's address plus `/mcp` (**Workspace settings → Apps → Create**), publishes it and
   marks it **Installed**. After a Bridgr update adds a tool, the admin refreshes the app so members see it.
4. **Codex:** each person adds it on their own computer, with the steps under Install below.

Each person still signs in once, as themselves. Bridgr checks its own list of people on every call, so removing
someone from your Bridgr's list cuts off only them. If your Bridgr is only reachable inside your company's network,
Claude and ChatGPT's apps can't reach it (they connect from the internet); Claude Code and Codex on a computer on
the network or VPN can.

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
for Claude**); an admin can upload that and click **Publish to org** so it's installed for everyone (see above).
To build a zip yourself, use `tools/build_zip.py`.

**Or let your assistant do it.** After installing the plugin, say *"Connect me to Bridgr."* It asks for your
company's address and walks you through every step. Claude and ChatGPT (chat apps) connect with a custom connector
instead, and the same guide covers them.

## What's here

| Path | What it is |
|---|---|
| `setup.md` | the guide an assistant follows to connect a person to their company's Bridgr |
| `install.md` | the guide an assistant follows to install a self-hosted Bridgr for a company |
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
