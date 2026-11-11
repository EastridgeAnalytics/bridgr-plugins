# Other assistants

The MCP URL is the Bridgr address plus `/mcp` (setup.md, step 1). Sign-in is OAuth in the browser: no key, no
client ID, no headers. When Bridgr is added, go back to setup.md, step 4.

**Codex** (CLI, IDE or app). Run all four, in order. The first two bring the guide to Bridgr's tools; the last two
connect:

    codex plugin marketplace add EastridgeAnalytics/bridgr-plugins
    codex plugin add bridgr@bridgr
    codex mcp add bridgr --url <MCP URL>
    codex mcp login bridgr

If the first line fails (not found, or no route to GitHub), skip the first two. Bridgr's tools load in a **new**
Codex session: quit and run `codex` again, or start a new chat in the app.

**Claude** (claude.ai, Claude Desktop without the plugin, mobile). One step at a time: **Customize → Connectors →
+ Add → Add custom connector**. Name `Bridgr`, URL the MCP URL. **Continue**, leave **Sign in now** selected, **Add**.
Then a new chat, with Bridgr on in the tools menu.

**ChatGPT** (web or desktop). One step at a time: **Settings → Plugins → + → Add custom MCP server**. Name
`Bridgr`, URL the MCP URL, authentication **OAuth**. Save, then **Connect**. Then a new chat, with Bridgr added from
the tools menu. A Business or Enterprise admin may have to allow custom MCP servers first.

**Cursor, VS Code (Copilot), Windsurf.** Add this under `"mcpServers"` in the client's MCP config, keeping the rest
of the file:

    "bridgr": { "url": "<MCP URL>" }

Cursor: `~/.cursor/mcp.json`. VS Code: `.vscode/mcp.json`, under `"servers"`, with `"type": "http"`. Windsurf:
`~/.codeium/windsurf/mcp_config.json`, with `"serverUrl"` in place of `"url"`. Reload the client's MCP servers or
restart it. Sign-in starts the first time a Bridgr tool is used.

**Anything else** that takes a remote MCP server: add one named `bridgr` at the MCP URL, Streamable HTTP, OAuth.
