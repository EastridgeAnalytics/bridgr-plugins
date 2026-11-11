# The address

Read the part that fits, then go back to [install.md](../install.md). Bridgr's address is where people open it,
like `https://bridgr.yourcompany.com`; the line `address: &address` in `compose.yaml` holds it.

## A. A server with ports 80 and 443 open

Nothing to change in `compose.yaml`. Point an `A` record for the address at the server's public IP; on a cloud VM,
allow 80 and 443 in its firewall too. Bridgr's own HTTPS gets the certificate. This prints the exact record:

    docker compose run --rm bridgr setup domain

| Who hosts the DNS | What you run, or what the person does |
|---|---|
| Cloudflare | The Cloudflare API, with a token scoped to Zone DNS Edit on that one zone. |
| AWS Route 53 | `aws route53 change-resource-record-sets` with the hosted zone ID and the record. |
| Google Cloud DNS | `gcloud dns record-sets create` with the zone, name, type A, IP and TTL 300. |
| DigitalOcean | `doctl compute domain records create` with the domain, type A, name, IP and TTL 300. |
| GoDaddy, Namecheap and other registrars | The person opens the domain's DNS page, adds the record and saves it. |

Ask before creating any DNS token, and only for that one zone. The person sets it through the provider's own sign-in
or a hidden prompt, never in the chat. Bridgr checks the address by itself every 5 minutes, or now:

    docker compose run --rm bridgr setup domain --check

## B. Something already serves HTTPS in front

A load balancer, an ingress, a reverse proxy, or a host that serves HTTPS for its servers. Before the first
`docker compose up -d`:

1. Ask two things: which port the front door forwards to on this server, and whether anyone on the internet can open
   the address without signing in to the host first. Bridgr signs people in itself, so the front door must let
   everyone through.
2. In `compose.yaml`, delete the `https:` service and its volumes. Under `bridgr:`, change `127.0.0.1:8080:8080` to
   `<that port>:8080`, for example `8000:8080`. Keep `address:` as the public `https://` address.
3. Keep the DNS the front door needs. A CNAME to the host's name is fine. Allow that port only from the front door if
   the firewall lets you. The front door must pass the `Host` header through.

Bridgr marks the address done by itself within a few minutes of starting: it fetches a one-time code from itself
through the public address. "A different server" means the front door points somewhere else: check its port.

## C. A trial on this computer

The address is `http://localhost:8080`. Start Bridgr alone, without the HTTPS service (install.md, step 6):

    mkdir -p files/uploads && docker compose up -d bridgr

Only this computer can open it. On a server reached over SSH, the person first runs
`ssh -L 8080:localhost:8080 <server>` on their own computer. The logs say `address: local trial at
http://localhost:8080`. Claude Code and Codex on this computer can connect. Claude's and ChatGPT's apps, and the
team, need a web address. In `status`, the address and the team say `later`: skip them.

## D. Moving to a web address later

1. `docker compose run --rm bridgr setup domain bridgr.yourcompany.com`. This edits `compose.yaml`.
2. Add the DNS record (A), or set up the front door (B). A computer nobody can reach from outside can use a
   Cloudflare Tunnel on the company's own Cloudflare account: `cloudflared tunnel create bridgr`, route the address to
   `http://localhost:8080`, and delete the `https:` service.
3. `docker compose up -d`, then `docker compose run --rm bridgr setup domain --check`. Data, people and settings stay.
4. Everyone signs in once more at the new address. The owner gets a new link with
   `docker compose run --rm bridgr signin`.

A licence moves to another address once every 30 days. Sooner? Reply to the licence email.
