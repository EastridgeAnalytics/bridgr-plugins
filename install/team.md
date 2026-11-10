# Bring in the team

Bridgr needs a web address the team can reach first ([web-address.md](web-address.md)). A mailbox lets Bridgr email
invites and sign-in links. Without one, the owner sends each person their link.

## 1. Add people

On the screen, **Settings, People**. Or in the terminal ([terminal.md](terminal.md)):

```sh
docker compose run --rm bridgr people add colleague@yourcompany.com --name "Their Name"
```

## 2. Their assistants

- **Everyone at once (Claude Team or Enterprise):** on the screen, **Settings, Connected assistants, Download for
  Claude**. A Claude Owner uploads that zip in **Settings, Customize, Plugins, Upload plugin**, then **Publish to
  org** as **Installed by default** or **Required**. The person does this.
- **ChatGPT (Business or Enterprise), Codex, or one person at a time:** see the
  [README](../README.md).
- **Each person** can also paste this into their own assistant, with the company's address:

  ```
  Connect me to Bridgr at https://bridgr.yourcompany.com. Fetch and follow https://raw.githubusercontent.com/EastridgeAnalytics/bridgr-plugins/main/setup.md
  ```

Claude's and ChatGPT's apps connect from the internet, so the address must be reachable from the internet for them.
Claude Code and Codex on the company network or VPN can reach a private address.
