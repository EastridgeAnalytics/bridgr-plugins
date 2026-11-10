# No licence email yet: pick a server and buy

Come back to [install.md](../install.md) when the email arrives.

## 1. A server

Ask the person where Bridgr should run. In order of what usually works best:

1. **A Linux VM inside the company's network.** Best when the databases are private: Bridgr reaches them directly.
2. **A cloud VM** near the data: AWS, Azure, Google Cloud, DigitalOcean, Hetzner or similar, with Ubuntu LTS.
3. **A host that already serves HTTPS** for its servers.
4. **Just trying it?** Any computer with Docker, a laptop included. No domain, no open ports.

| | Recommended | Minimum |
|---|---|---|
| CPU and memory | 4 vCPU, 8 GB | 2 vCPU, 4 GB (tight while Bridgr answers a question) |
| Disk | 50 GB | 25 GB |
| Software | Linux with Docker and Docker Compose | the same |
| Network | ports 80 and 443 open to the internet, and a route to the databases Bridgr will read | the same |

## 2. What the person needs ready

- **An address on the company's domain,** such as `bridgr.yourcompany.com`, and someone who can add a DNS record.
  Not needed for a trial on one computer.
- **An Anthropic API key** from https://console.anthropic.com. The person creates it and types it in later.
- **The owner's email address.** The licence, first sign-in and billing go there. A work email gives the address
  `bridgr.<their domain>` by default. A personal email starts as a trial on this computer.

## 3. Buy

The person pays here: https://buy.stripe.com/test_6oU4gz6Uz4jw77h75Z7ss06

Pre-release: this is Stripe's test mode. Card `4242 4242 4242 4242`, any future date and any CVC. They enter the
owner's email and the company's name. Monthly, cancel any time.

## 4. Wait for the email

Within a minute the owner gets **Your Bridgr licence key** from `info@eastridge-analytics.com`, with two files
attached: `compose.yaml` and `seccomp-bwrap.json`. Nothing arrived? Check spam, then reply to the address on the
checkout receipt.

Then go back to [install.md](../install.md), "Five steps".
