# Give Bridgr a web address

Read this when moving from a trial on one computer to an address the team can reach, or when Bridgr's status says
the address needs a DNS record. Behind a load balancer or a host that serves HTTPS? Read [proxy.md](proxy.md)
instead.

## 1. Pick the way that fits

| The server | Do this |
|---|---|
| Has ports 80 and 443 open to the internet | Point an `A` record for the address at the server's public IP. On a cloud VM, also allow 80 and 443 in its firewall or security group. Bridgr's built-in HTTPS gets the certificate. |
| Has HTTPS in front of it already | Follow [proxy.md](proxy.md). |
| Can't be reached from outside (a laptop, a private server) | A Cloudflare Tunnel, free, on the company's own Cloudflare account: `cloudflared tunnel create bridgr`, route the address to `http://localhost:8080`, run it as a service, and delete the `https:` service from `compose.yaml` (the tunnel serves HTTPS). Any tunnel the company already uses works the same way. |

## 2. The DNS record

Run this. It prints the exact record for the address:

```sh
docker compose run --rm bridgr setup domain
```

For a server with a public IP it looks like this:

```text
Type:  A
Name:  bridgr
Value: this server's public IP
TTL:   300
```

Find who hosts the company's DNS, then:

| DNS provider | What the assistant runs, or what the person does |
|---|---|
| Cloudflare | The Cloudflare API, with a token scoped to Zone DNS Edit on that one zone. |
| AWS Route 53 | `aws route53 change-resource-record-sets` with the hosted zone ID and the record. |
| Google Cloud DNS | `gcloud dns record-sets create` with the zone, name, type A, IP and TTL 300. |
| DigitalOcean | `doctl compute domain records create` with the domain, type A, name, IP and TTL 300. |
| GoDaddy, Namecheap and other registrars | The person opens the domain's DNS page, adds the record and saves it. |

Ask the person before creating any DNS token, and only for that one zone. They set it through the provider's own
sign-in or a hidden prompt, never in chat.

## 3. Switch Bridgr to the address

1. `docker compose run --rm bridgr setup domain bridgr.yourcompany.com` (this changes the address in `compose.yaml`).
2. `docker compose up -d`. Data, people and settings stay.
3. `docker compose run --rm bridgr setup domain --check`. Bridgr proves HTTPS works there before the licence
   belongs to that address. Bridgr also checks by itself every 5 minutes.
4. Everyone signs in once more at the new address. Then bring in the team: [team.md](team.md).

A licence can move to another address once every 30 days. Sooner? Reply to the licence email.
