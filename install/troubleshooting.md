# When something goes wrong

Find the line you saw. Bridgr never crash-loops on a licence problem: it stays up and says why, on its screen and
in `docker compose logs bridgr`.

| What you saw | What to do |
|---|---|
| `docker: command not found`, or `docker compose` isn't a command | Docker isn't installed: [install.md](../install.md), step 1. On Mac or Windows the person installs Docker Desktop and opens it once. |
| Docker Desktop is installed but `docker info` says it can't connect | It is still starting. Wait a minute and try again. Still not: open Docker Desktop from the Start menu or Applications, and wait for it to say it's running. |
| The download takes more than 10 minutes | Bridgr is about 600 MB. Let it finish. If it stopped, run the same start command again; it carries on. |
| `unauthorized` or `no basic auth credentials` from `docker compose up` or `pull` | Run the registry sign-in again ([install.md](../install.md), step 5), then start again. |
| `denied: This Bridgr licence is canceled` (or another status) on pull | The subscription isn't active. The owner renews with the link in the licence email; the same key works again. |
| `That licence key isn't one of ours` | Use the `compose.yaml` from the licence email unchanged. |
| `licence: paused (missing)` | The licence key isn't in `compose.yaml`. Use the file from the email as is. |
| `model key: missing` or `model key: rejected` | The owner types the key on the screen, or runs `docker compose run --rm bridgr setup key` and types it at the hidden prompt. |
| `licence: paused (wrong_domain)` | The licence belongs to another proven address. Use that address, move after 30 days with `setup domain <new>`, or reply to the licence email. |
| `licence: paused (invalid_address)` | A bare name or a network IP. Use `http://localhost:8080` or a real `https://` address ([address.md](address.md)). |
| `licence: paused (canceled)` | Renew with the link in the licence email. |
| `licence: paused (unreachable)` | Its words say which: this computer can't reach the internet (allow outbound HTTPS), or Eastridge's licence service failed (Bridgr keeps trying every 5 minutes). |
| The address check says "a different server" | Something else answers at the address. Behind a front door? Check its port ([address.md](address.md), B). |
| The address check says TLS failed | Wait a few minutes after adding the domain, then `setup domain --check`. |
| The page doesn't load, no certificate | DNS isn't pointing at the server yet, or ports 80 and 443 are closed ([address.md](address.md), A). |
| The sign-in page says "Ask them for your sign-in link", or a link says it's used or out of date | `docker compose run --rm bridgr signin` prints a fresh one for the owner; `signin EMAIL` for a person on the list. |
| The AI key step stays on Claude Code | The `volumes:` line points at a file that isn't there, so Docker made a folder in its place. Delete that folder, check the path, start again. Or use the AI key. |
| Bridgr says its Claude Code sign-in has run out | Sign in to Claude Code again on that computer. Or `claude setup-token` in the owner's own terminal prints a token that lasts a year: paste it at Settings, AI key. No Claude subscription: an Anthropic API key goes in the same box. |
| `model key: rejected: the Claude Code token has expired` | Run `claude setup-token` again and paste the new token at Settings, AI key. |
| `data add /files` says "not a full path: start it at the drive" | Windows' Git Bash changed `/files` into a Windows path. Run `data add` with no path; it means `/files`. |
| The data window says "This Bridgr can't see any folders on the computer" | The drive line isn't in `compose.yaml` (install.md, step 4). Add it and start again with the same command as step 6, or upload a file instead. |
| A question says "No data yet" | Add data first: Settings, Folders, or `data add /files` ([terminal.md](terminal.md)). |
| Connecting a system says "nothing answered at that host and port" | Bridgr's server can't reach it over the network: it's private, in another cloud, or a firewall blocks it. Read [connect-across-networks.md](connect-across-networks.md). Don't change the password. |

Still stuck? Reply to the licence email.
