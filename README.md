# Bridgr plugins

Bridgr answers questions from your company's own systems. It only reads. Your company runs it on its own server.

This repo holds the pages an AI assistant follows to install Bridgr or connect to it, and the Claude plugin.

## Which one are you?

**You're installing Bridgr for your company.** You have the licence email, or you're about to buy. Paste this into
Claude Code on the server, or on this computer to try it first, or any assistant that can run commands there:

    Install Bridgr for my company. Fetch and follow https://raw.githubusercontent.com/EastridgeAnalytics/bridgr-plugins/main/install.md

**Your company already runs Bridgr and you want it in your assistant.** Paste this into Claude Code, Claude Desktop,
Codex, ChatGPT, Cursor or any assistant that takes an MCP server. Add "at https://…" if you know your Bridgr's address.

    Connect me to Bridgr. Fetch and follow https://raw.githubusercontent.com/EastridgeAnalytics/bridgr-plugins/main/setup.md

That's it. The pages do the rest.

## Buy

https://buy.stripe.com/dRm5kD92H9DQ4Z9dun7ss05

$999 a month, cancel any time. The owner pays there themselves, by card, and enters the company's name. Have a
promotion code? Enter it on that page. Within a minute the licence email, **Your Bridgr licence key**, arrives with
the two files the install needs. What to have ready, and where Bridgr runs best: [install/buy.md](install/buy.md).

## Try it somewhere separate first

Bridgr runs in Docker and only reads. If your security team wants to look before it goes near a work machine, start
with a sandbox: a fresh VM (any cloud, Ubuntu LTS) or a spare computer with Docker. Tell your assistant so: "Install
Bridgr for my company on this test VM." Nothing is lost when it moves to a real server later: the same licence and
files work there. What the container can reach, and what it keeps: [Safety](#safety).

## What's here

| | |
|---|---|
| `install.md` and `install/` | the install path; one extra page only when a step needs it |
| `setup.md` and `setup/` | the connect path; one extra page for assistants other than Claude |
| `plugins/bridgr/` | the plugin for Claude Code and Codex, and the source of the Claude Desktop zip |
| `tools/build_zip.py` | builds the zip. Your own Bridgr builds one with its address already in it, under Settings, Connected assistants |

## Safety

- The assistant never sees a password, key or token. You sign in on your Bridgr's own page and click Approve yourself.
- Bridgr lets you in only if you're on your company's list, and checks again on every call.
- Bridgr only reads. It never changes your company's systems.
- Bridgr runs as one Docker container with its own sandbox for the AI's work (`bridgr-security.json`). It can see the machine's drive read-only, or
  only the `files` folder beside `compose.yaml` if you say so at install, and you choose on its screen what goes on
  the map. It keeps its own data in a Docker volume on that machine.

Questions: https://www.bridgr-platform.com/contact
