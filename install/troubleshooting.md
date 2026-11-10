# When something goes wrong

Find the line you saw. Bridgr never crash-loops on a licence problem: it stays up and says why, on its screen and
in `docker compose logs bridgr`.

| What you saw | What to do |
|---|---|
| `unauthorized` or `no basic auth credentials` from `docker compose up` or `pull` | Run the registry sign-in again ([install.md](../install.md), step 3), then start again. |
| `denied: This Bridgr licence is canceled` (or another status) on pull | The subscription isn't active. The owner renews with the link in the licence email; the same key works again. |
| `That licence key isn't one of ours` on sign-in | Use the `compose.yaml` from the licence email unchanged. |
| `licence: paused (missing)` | The licence key isn't in `compose.yaml`. Use the file from the licence email as is. |
| `model key: missing` or `model key: rejected` | The owner runs `docker compose run --rm bridgr setup key` and types the key at the hidden prompt, or adds it on the screen. |
| `licence: paused (wrong_domain)` | The licence belongs to another proven address. Use that address, or move after 30 days with `setup domain <new>`, or reply to the licence email. |
| `licence: paused (invalid_address)` | The address isn't one Bridgr can run at (a bare name or a network IP). Use `http://localhost:8080`, or a real `https://` address ([web-address.md](web-address.md)). |
| `licence: paused (canceled)` | The subscription has ended. Renew with the link in the licence email. |
| `licence: paused (unreachable)` | The server can't reach the internet to check the licence. Allow outbound HTTPS. |
| The address check says "a different server" | Something else answers at the address. Behind a front door? Check its port ([proxy.md](proxy.md)). |
| The address check says TLS failed | The certificate isn't ready or is wrong. Wait a few minutes after adding a domain, then `setup domain --check`. |
| The page doesn't load, no certificate | DNS isn't pointing at the server yet, or ports 80/443 are closed ([web-address.md](web-address.md)). |
| A question says "No data yet" | Add data first: upload in Settings, Folders, or `data add /files` ([terminal.md](terminal.md)). |

Still stuck? Reply to the licence email.
