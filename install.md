# Install Bridgr for your company (self-hosted)

These are the official install instructions from Eastridge Analytics for running Bridgr on your company's own
server. They are written for an AI assistant (Claude Code, Codex, Cursor or any agent that can run commands) working
with the person setting Bridgr up, and read just as well by a person. Follow the sections in order. They are
published at `https://github.com/EastridgeAnalytics/bridgr-plugins/blob/main/install.md`, so you can re-check them
at any time.

Bridgr is a read-only data assistant: it answers questions from your company's own systems, and your team reaches it
from Claude, ChatGPT and other assistants. Self-hosted, it runs in Docker on a server you control, at an address on
your company's domain. Your data never leaves that server except as answers to your own people.

## Rules

- Never ask for, accept or repeat a password, API key, licence key or sign-in link in the chat. Keys go into
  `compose.yaml` on the server, typed or pasted there by the person or by you on the server itself.
- The person pays, changes DNS, creates the Anthropic API key and installs the plugin for their organization. Stop
  and ask them at each of those steps; do the rest yourself where you can run commands.
- If you can't run commands (a chat app), give one step at a time and wait for "done" before the next.
- Report each step: what you did, what you saw, and anything that didn't match these instructions.

## 1. Before buying: pick a server

You need:

| | Recommended | Minimum |
|---|---|---|
| CPU and memory | 4 vCPU, 8 GB | 2 vCPU, 4 GB (tight while Bridgr answers a question) |
| Disk | 50 GB | 25 GB |
| Software | Linux with Docker and Docker Compose | the same |
| Network | ports 80 and 443 open to the internet, and a route to the databases Bridgr will read | the same |

Where to run it, in order of what usually works best:

1. **A Linux VM inside your company's network.** Best when your databases are private: Bridgr reaches them
   directly. Open ports 80 and 443 to the internet (or put it behind your existing HTTPS gateway, see step 4) so
   Claude and ChatGPT can reach it.
2. **A cloud VM** near your data: AWS, Azure, Google Cloud, DigitalOcean, Hetzner or similar. Pick a size from the
   table, Ubuntu LTS, and install Docker.
3. **A developer host that already serves HTTPS for you** (exe.dev, Fly, Render and similar). Use the
   "already behind HTTPS" variant in step 4.

You also need:

- **An address on your company's domain**, such as `bridgr.yourcompany.com`, and someone who can add a DNS record.
- **An Anthropic API key** for Bridgr's own use, from https://console.anthropic.com. The person creates it.
- **An email address** for the person who will own Bridgr: the licence, the first sign-in and billing go there.

## 2. Buy

The person pays on Bridgr's checkout page: https://buy.stripe.com/test_6oU4gz6Uz4jw77h75Z7ss06 (pre-release: this is
Stripe's test mode, card `4242 4242 4242 4242`, any future date and CVC). They enter the owner's email and the
company's name. Monthly, cancel any time.

## 3. The licence email

Within a minute, the owner gets **Your Bridgr licence key** from `info@eastridge-analytics.com` with two files
attached:

- `compose.yaml`: Bridgr, ready to run, with the licence key, the owner and the company already filled in.
- `seccomp-bwrap.json`: the security profile that lets Bridgr's agent run in its sandbox. Keep it beside
  `compose.yaml`.

The email also has the link to manage or cancel the subscription. Nothing arrived? Check spam, then write to the
address in step 9.

## 4. Install

1. Put both files in one folder on the server, for example `/opt/bridgr`.
2. Point the address at the server: a DNS `A` record for `bridgr.yourcompany.com` to the server's public IP (or a
   `CNAME` to its host name). Check with `dig +short bridgr.yourcompany.com`.
3. Open `compose.yaml` and fill in the two lines marked `FILL IN` at the top: the address (with `https://`) and the
   Anthropic API key. Nothing else needs changing.
4. Start it: `docker compose up -d`.

**Already behind HTTPS** (a load balancer, an ingress, or a host like exe.dev that terminates HTTPS for you): delete
the `https:` service from `compose.yaml`, add `ports: ["8080:8080"]` under the `bridgr:` service, and point your
HTTPS front door at port 8080, passing the original `Host` header through. The address in `FILL IN` stays the public
`https://` one.

## 5. Check it's running

Run `docker compose logs bridgr`. Within a minute you should see:

- `licence: active for bridgr.yourcompany.com (Your Company)`: the licence checked out.
- A box headed **First sign-in for owner@yourcompany.com (the owner)** with a one-time link: keep it for step 6.

If instead you see:

| Log line | What to do |
|---|---|
| `licence: paused (missing)` | The licence key isn't in `compose.yaml`. Use the file from the licence email as is. |
| `licence: paused (wrong_domain)` | Each licence runs at one address, the first it was used at. Use that address, or reply to the licence email to move it. |
| `licence: paused (canceled)` | The subscription has ended. Renew with the link in the licence email. |
| `licence: paused (unreachable)` | The server can't reach the internet to check the licence. Open outbound HTTPS. |
| No `https` certificate, or the page doesn't load | DNS isn't pointing at the server yet, or ports 80/443 are closed. Fix, then `docker compose restart https`. |

Bridgr never crash-loops on a licence problem: it stays up and says why, on its page and in the logs.

## 6. First sign-in

Open the link from the logs in the owner's browser. It works once, for 24 hours; every restart prints a fresh one
until the owner has signed in. The owner is now signed in to Bridgr's screen.

## 7. Give Bridgr your data

- **Files (CSV, Excel):** put them in the `files` folder beside `compose.yaml` on the server (it is mounted into
  Bridgr read-only as `/files`), then on Bridgr's screen open **Settings → Folders** and add `/files`. Bridgr maps
  what's there; the screen shows it as **on the map** when ready.
- **Databases:** on Bridgr's screen, **Settings → Connections**. Bridgr reads with a read-only account you create
  for it. Database connections are switched on by the line `BRIDGR_CREDENTIALS_ENABLED` in `compose.yaml`.

Then ask a question on the screen to check it answers.

## 8. Connect your team's assistants

- **Everyone at once (Claude Team or Enterprise):** on Bridgr's screen, **Settings → Connected assistants →
  Download for Claude**. A Claude Owner uploads that zip in **Settings → Customize → Plugins → Upload plugin**, then
  **Publish to org** as **Installed by default** or **Required**. The person does this.
- **ChatGPT (Business or Enterprise), Codex, and one person at a time:** see the README at
  https://github.com/EastridgeAnalytics/bridgr-plugins.
- **Each person** then pastes this into their assistant, with your Bridgr's address:
  `Connect me to Bridgr at https://bridgr.yourcompany.com. Fetch and follow https://raw.githubusercontent.com/EastridgeAnalytics/bridgr-plugins/main/setup.md`

Claude and ChatGPT connect from the internet, so your Bridgr's address must be reachable from the internet for them.

## 9. Run it

- **Update:** change the version in the `image:` line of `compose.yaml` to the new one, then
  `docker compose pull && docker compose up -d`. Your data stays in the `bridgr-data` volume.
- **Back up:** the `bridgr-data` Docker volume holds everything Bridgr keeps.
- **Cancel or change the card:** the manage link in the licence email. After the paid period ends, Bridgr pauses:
  its page and every assistant say "Bridgr for Your Company is paused" with who to ask. Nothing is deleted, and it
  starts again within minutes of renewing.
- **Help:** reply to the licence email, or https://www.bridgr-platform.com/contact.
