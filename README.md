# Bridgr plugins

Bridgr answers questions from your company's own systems. It only reads. Your company runs it on its own server.

This repo holds the pages an AI assistant follows to install Bridgr or connect to it, and the Claude plugin.

## Which one are you?

**You're installing Bridgr for your company.** You have the licence email, or you're about to buy. Paste this into
Claude Code on the server, or any assistant that can run commands there:

    Install Bridgr for my company. Fetch and follow https://raw.githubusercontent.com/EastridgeAnalytics/bridgr-plugins/main/install.md

**Your company already runs Bridgr and you want it in your assistant.** Paste this into Claude Code, Claude Desktop,
Codex, ChatGPT, Cursor or any assistant that takes an MCP server. Add "at https://…" if you know your Bridgr's address.

    Connect me to Bridgr. Fetch and follow https://raw.githubusercontent.com/EastridgeAnalytics/bridgr-plugins/main/setup.md

That's it. The pages do the rest.

## What's here

| | |
|---|---|
| `install.md` and `install/` | the install path; one extra page only when a step needs it |
| `setup.md` and `setup/` | the connect path; one extra page for assistants other than Claude |
| `plugins/bridgr/` | the plugin for Claude Code and Codex, and the source of the Claude Desktop zip |
| `tools/build_zip.py` | builds the zip. Your own Bridgr builds one with its address already in it, under Settings, Connected assistants |

## Safety

- No password, key or token goes through the assistant. You sign in on your Bridgr's own page and click Approve yourself.
- Bridgr lets you in only if you're on your company's list, and checks again on every call.
- Bridgr only reads. It never changes your company's systems.

Questions: https://www.bridgr-platform.com/contact
