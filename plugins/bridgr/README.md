# Bridgr plugin (Claude Code and Codex)

One folder for both. Claude Code reads `.claude-plugin/plugin.json` and `.mcp.json`; Codex reads
`.codex-plugin/plugin.json`. Both load the two skills in `skills/`: `bridgr-connect` (setup) and `bridgr` (the
tools).

- **Claude Code** asks for your company's Bridgr address when you install (`userConfig.bridgr_url`) and connects to
  `<address>/mcp` only. Until you give it one, it connects to nothing.
- **Codex** has no way yet for a plugin to ask for an address, so the plugin carries no connector. Add it with
  `codex mcp add bridgr --url <address>/mcp`, then `codex mcp login bridgr`. The `bridgr-connect` skill walks you
  through it.

Sign-in is your Bridgr's own, in your browser, and the assistant then works as you, with the same list and limits.
It never sees a password.
