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

- Never ask for, accept or repeat a password, API key, licence key or token in the chat. Share the first sign-in
  link only with the owner, never in a public or team chat. For the AI
  key, run `docker compose run --rm bridgr setup key`: the person types it at a hidden prompt; the agent never sees it.
- The person buys the licence before this path starts. During setup, stop for the owner only for the AI key,
  first sign-in and licence terms, and the data choice. Use existing server and DNS access for the rest. If access
  is missing, explain the blocker without asking for secrets in chat.
- If you can't run commands (a chat app), give one step at a time and wait for "done" before the next.
- Report each step: what you did, what you saw, and anything that didn't match these instructions.

## For an AI assistant: the quick version

1. Read the licence email. Save `compose.yaml` and `seccomp-bwrap.json` together on the server. Check the
   `address: &address` line before the first start: it defaults to `bridgr.<email domain>`, for example
   `https://bridgr.yourcompany.com` (personal email addresses use `http://localhost:8080`). If it is wrong, edit
   that line now. The licence locks to an address only after Bridgr proves it works there, so check it first.
   Set up DNS and HTTPS for that address using the choices below, or use the local trial.
2. In that folder, sign in without printing the licence key:

   ```sh
   grep -o 'brg_[a-z]*_[0-9a-f]*' compose.yaml | docker login registry.bridgr-platform.com -u licence --password-stdin
   ```

3. Start Bridgr:

   ```sh
   mkdir -p files/uploads && docker compose up -d
   ```

4. Run `docker compose run --rm bridgr status --json`. If `next` is `done`, stop. If `person` is true,
   relay `say_to_person` to the owner and wait. If `wait_seconds` is above 0, Bridgr is working by itself: wait
   that long and check again. Otherwise run the exact command in `run`. Repeat status after
   each step. Do not guess a command from a step's `action` or open a screen in place of `run`.
5. The three owner stops are:
   - **AI key:** the person types it on Bridgr's screen or at the hidden prompt from
     `docker compose run --rm bridgr setup key`. Never ask them to paste it to the agent.
   - **First sign-in and terms:** get the first sign-in link from `docker compose logs bridgr` and give it only
     to the owner to open in their browser. The owner reads and accepts the licence terms, not the agent.
   - **Data choice:** the owner chooses the files or read-only database connection Bridgr should use.

The JSON is `onboard.checklist(project)` plus these top-level fields:

| Field | Meaning |
|---|---|
| `next` | Step id or `"done"`. |
| `person` | `true` when the next step needs the human. |
| `say_to_person` | One plain sentence to relay when `person` is true, `""` otherwise. |
| `run` | The exact command to run next when `person` is false, `""` otherwise. |
| `wait_seconds` | Above 0 when Bridgr is working by itself (for example mapping uploaded data): wait that long, then check status again. Nothing to run and nothing to ask. |

Exit codes: **0** all done, **2** more to do, **1** error. Exit 2 is normal in the loop, not a failed install.
On an error, fix the reported problem before continuing. `docker compose run --rm bridgr status` shows the
checklist in plain words. People can use the manual path below at any time.

## Manual path

Follow sections 1 to 10 if you prefer to install by hand. The same registry sign-in, files folder and owner
choices apply. Never accept the terms or enter a key on someone else's behalf.

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
3. **A host that already serves HTTPS for you.** Use the
   "Already behind an HTTPS proxy" variant in step 4.

4. **Just trying it first? Any computer with Docker.** A laptop, or a server you reach over SSH, with no domain and no
   open ports. Use the "On this computer" variant in step 4. Only that computer can reach Bridgr until you give it a
   web address (step 10); nothing is lost when you do.

You also need:

- **An address on your company's domain**, such as `bridgr.yourcompany.com`, and someone who can add a DNS record.
  Not needed to try it on one computer (`http://localhost:8080`); needed for Claude's and ChatGPT's apps and your team.
- **An Anthropic API key** for Bridgr's own use, from https://console.anthropic.com. The person creates it.
- **An email address** for the person who will own Bridgr: the licence, the first sign-in and billing go there.

## 2. Buy

The person pays on Bridgr's checkout page: https://buy.stripe.com/test_6oU4gz6Uz4jw77h75Z7ss06 (pre-release: this is
Stripe's test mode, card `4242 4242 4242 4242`, any future date and CVC). They enter the owner's email and the
company's name. Monthly, cancel any time.

## 3. The licence email

Within a minute, the owner gets **Your Bridgr licence key** from `info@eastridge-analytics.com` with two files
attached:

- `compose.yaml`: Bridgr, ready to run, with the licence key, the owner and the company already filled in. The
  address is already `bridgr.<your email's domain>`, such as `https://bridgr.yourcompany.com`, or
  `http://localhost:8080` for a personal email address. Check and, if needed, edit the address line before first start.
- `seccomp-bwrap.json`: the security profile that lets Bridgr's agent run in its sandbox. Keep it beside
  `compose.yaml`.

The email also has the link to manage or cancel the subscription. Nothing arrived? Check spam, then write to the
address in step 9.

## 4. Install

1. Put both files in one folder on the server, for example `/opt/bridgr`.
2. For a public address, point DNS at the server and open ports 80 and 443 (step 10). For a local trial, use the
   "On this computer" variant below.
3. Before the first start, check the `address: &address` line in `compose.yaml`. It is already filled in from
   your email domain, or set to `http://localhost:8080` for a personal email address. If wrong, edit that line
   now. The licence locks to an address only after Bridgr proves it works there.
   Leave the AI key empty for now. After starting, the person types it on Bridgr's screen or at the hidden
   prompt from `docker compose run --rm bridgr setup key`, never in chat.
   Leave `BRIDGR_ACCEPT_TERMS` as `"no"`: the owner reads and accepts the Bridgr Licence Terms
   (https://github.com/EastridgeAnalytics/bridgr-plugins/blob/main/TERMS.md) on the screen at first sign-in.
   Never accept them on the person's behalf.
4. Sign in to Bridgr's registry. The Bridgr image is for licence holders, and your licence key is the password. In
   the folder with `compose.yaml`, run exactly this (it reads the key from the file, so nobody types, pastes or
   prints it; an AI assistant must not show the key either):

   ```
   grep -o 'brg_[a-z]*_[0-9a-f]*' compose.yaml | docker login registry.bridgr-platform.com -u licence --password-stdin
   ```

   It should print `Login Succeeded`. Docker keeps the sign-in on this server for later updates.
5. Prepare the files mountpoint and start it: `mkdir -p files/uploads && docker compose up -d`.

**On this computer** (trying it on a laptop, or a server you reach over SSH; no domain, no open ports): set the
address in `FILL IN` to `http://localhost:8080`, and start Bridgr alone, without the HTTPS service:
`mkdir -p files/uploads && docker compose up -d bridgr`. Open `http://localhost:8080` in a browser on that computer
(over SSH, first run `ssh -L 8080:localhost:8080 <server>` from your own computer). The logs say
`address: local trial at http://localhost:8080`, and the owner sees a reminder on the screen. Claude Code and Codex
on the same computer can connect; Claude's and ChatGPT's apps and the rest of your team need a web address (step 10).

**Already behind an HTTPS proxy** (a load balancer, an ingress, or a host that serves HTTPS): delete
 the `https:` service from `compose.yaml`. Under `bridgr:`, replace `127.0.0.1:8080:8080` with the host port
 your proxy forwards to, for example `8000:8080` when it forwards to port 8000. Restrict that port to the proxy
 in your firewall. Pass the original `Host` header through. The address stays the public `https://` one,
 such as `https://bridgr.yourcompany.com`. A DNS CNAME to the proxy host is fine. Do not replace it with an A
 record to this server's outbound IP.

## 5. Check it's running

Run `docker compose logs bridgr`. Within a minute you should see:

- `licence: active for bridgr.yourcompany.com (Your Company)`: the licence checked out.
- A box headed **First sign-in for owner@yourcompany.com (the owner)** with a one-time link: keep it for step 6.

If instead you see:

| Log line or message | What to do |
|---|---|
| `unauthorized` or `no basic auth credentials` from `docker compose up` or `pull` | Run the registry sign-in (step 4, item 4), then start again. |
| `denied: This Bridgr licence is canceled` (or another status) on pull | The subscription isn't active. Renew with the link in the licence email; the same key works again. |
| `That licence key isn't one of ours` on sign-in | Use the `compose.yaml` from your licence email unchanged; the key in it is the one to sign in with. |
| `licence: paused (missing)` | The licence key isn't in `compose.yaml`. Use the file from the licence email as is. |
| `model key: missing` or `model key: rejected` | The owner runs `docker compose run --rm bridgr setup key` and types the key at the hidden prompt, or adds it on Bridgr's screen. Never put it in chat. |
| `licence: paused (wrong_domain)` | The licence belongs to another proven address. Use that address, or move with `docker compose run --rm bridgr setup domain <new>` once 30 days have passed. Otherwise reply to the licence email. |
| `licence: paused (invalid_address)` | The address in `FILL IN` isn't one Bridgr can run at (a bare name or a network IP). Use `http://localhost:8080` on this computer, or your company's own `https://` address (step 10). |
| `licence: paused (canceled)` | The subscription has ended. Renew with the link in the licence email. |
| `licence: paused (unreachable)` | The server can't reach the internet to check the licence. Open outbound HTTPS. |
| No `https` certificate, or the page doesn't load | DNS isn't pointing at the server yet, or ports 80/443 are closed. Fix, then `docker compose restart https`. |

Bridgr never crash-loops on a licence problem: it stays up and says why, on its page and in the logs.

## 6. First sign-in

Open the link from the logs in the owner's browser. It works once, for 24 hours; every restart prints a fresh one
until the owner has signed in. The owner is now signed in to Bridgr's screen.

## 7. Give Bridgr your data

- **Upload files (CSV, Excel .xlsx, Parquet):** the owner can open **Settings → Folders** and choose **Upload a data file**.
  Each file can be up to 25 MB. Bridgr keeps a copy in its writable uploads volume and adds that project's uploads
  folder to the map. This works without a mailbox and without enabling database credential setup.
  Before the first `docker compose up -d`, run `mkdir -p files/uploads` to prepare the nested mountpoint.
- **Files already on the server:** put them in the `files` folder beside `compose.yaml` on the server (it is mounted into
  Bridgr read-only as `/files`), then on Bridgr's screen open **Settings → Folders** and add `/files`. Bridgr maps
  what's there; the screen shows it as **on the map** when ready. Leave `files/uploads` in place as the mountpoint
  for the separate writable uploads volume. The rest of `files` stays read-only.
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
  `docker compose pull && docker compose up -d`. Your data stays in the `bridgr-data` volume. Updates need an active
  subscription: the registry checks the licence key on every pull. Signed out (a new server, or Docker reset)? Run the
  sign-in from step 4 again.
- **Back up:** the `bridgr-data` Docker volume holds everything Bridgr keeps.
- **Cancel or change the card:** the manage link in the licence email. After the paid period ends, Bridgr pauses:
  its page and every assistant say "Bridgr for Your Company is paused" with who to ask. Nothing is deleted, and it
  starts again within minutes of renewing.
- **Help:** reply to the licence email, or https://www.bridgr-platform.com/contact.

## 10. Give it a web address

Started on one computer (`http://localhost:8080`)? Give Bridgr a web address when you want Claude's and ChatGPT's apps
and the rest of your team to reach it. First run:

```
docker compose run --rm bridgr setup domain
```

It prints the exact DNS record for your address. To choose another address, run
`docker compose run --rm bridgr setup domain bridgr.yourcompany.com`. After setting up DNS and HTTPS, check it with:

```
docker compose run --rm bridgr setup domain --check
```

For a server with a public IP, the record is:

```text
Type:  A
Name:  bridgr
Value: this server's public IP
TTL:   300
```

Use the server's public inbound IP only when DNS points straight at it. Behind an HTTPS proxy, keep the proxy's
DNS target, including a CNAME to its host. Do not use an outbound IP as a substitute. Pick the row for whoever
hosts your domain's DNS:

| DNS provider | What the assistant runs, or what the person does |
|---|---|
| Cloudflare | Use the Cloudflare API to create the record, with a token scoped to Zone DNS Edit on that one zone. |
| AWS Route 53 | `aws route53 change-resource-record-sets` with the hosted zone ID and the record above. |
| Google Cloud DNS | `gcloud dns record-sets create` with the managed zone, record name, type A, IP and TTL 300. |
| DigitalOcean | `doctl compute domain records create` with the domain, type A, name bridgr, IP and TTL 300. |
| GoDaddy, Namecheap and other registrars | The person opens the domain's DNS dashboard, chooses Add record, enters the record above and saves it. |

**Give an assistant a DNS token for that one zone only, and ask the person before creating it.** Never put a token
in chat. The person sets it through the provider's local sign-in or secret prompt.

Pick the way that fits, then do the last part.

| Your situation | Do this |
|---|---|
| A server with ports 80 and 443 open to the internet | Point a DNS `A` record for `bridgr.yourcompany.com` at the server's public IP. On a cloud VM, also allow 80 and 443 in its firewall or security group. Bridgr's built-in HTTPS gets the certificate. |
| You already have HTTPS in front (a load balancer, an ingress, a host that serves it) | Point it at the host port your proxy forwards to, passing the original `Host` header through. A CNAME to the proxy host is fine. Delete the `https:` service and map that host port to container port 8080, for example `8000:8080` (step 4, "Already behind an HTTPS proxy"). |
| Neither: a laptop, or a server nobody can reach from outside | A Cloudflare Tunnel, free, on your own Cloudflare account and a domain there: `cloudflared tunnel create bridgr`, route `bridgr.yourcompany.com` to `http://localhost:8080`, and run it as a service. Delete the `https:` service as above (the tunnel serves HTTPS). Any tunnel or reverse proxy you already use works the same way. |

Then, the last part, the same for every way:

1. Run `docker compose run --rm bridgr setup domain bridgr.yourcompany.com` to change the address in `compose.yaml`.
2. `docker compose up -d`. Bridgr comes back at the new address with everything it had: data, people and settings stay
   in the `bridgr-data` volume.
3. Run `docker compose run --rm bridgr setup domain --check`. Bridgr must prove HTTPS works at the address before the
   licence belongs to it. Check that `docker compose logs bridgr` says `licence: active for bridgr.yourcompany.com`
   and the reminder is gone from the screen. Moving later: `docker compose run --rm bridgr setup domain <new>`.
   A licence can move once every 30 days, or reply to the licence email.
4. Everyone signs in once more at the new address. Assistants connected on this computer (Claude Code, Codex)
   reconnect with the new address. Then connect the rest of your team's assistants (step 8).
