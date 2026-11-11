# No licence email yet

Come back to [install.md](../install.md) when it arrives.

## 1. Where Bridgr runs

Ask the owner. In order of what usually works best:

1. A Linux VM inside the company's network. Best when the databases are private: Bridgr reaches them directly.
2. A cloud VM near the data (AWS, Azure, Google Cloud, DigitalOcean, Hetzner), Ubuntu LTS.
3. A host that already serves HTTPS for its servers.
4. Just trying it: any computer with Docker, a laptop included. No domain, no open ports.

| | Recommended | Minimum |
|---|---|---|
| CPU and memory | 4 vCPU, 8 GB | 2 vCPU, 4 GB |
| Disk | 50 GB | 25 GB |
| Software | Linux with Docker and Docker Compose | the same |
| Network | ports 80 and 443 open, and a route to the databases Bridgr will read | the same |

## 2. Have ready

- An address on the company's domain, like `bridgr.yourcompany.com`, and someone who can add a DNS record. Not
  needed for a trial on one computer.
- Claude Code signed in on the computer Bridgr will run on: Bridgr answers with that. Without it, an Anthropic API
  key from https://console.anthropic.com.
- The owner's email. The licence, first sign-in and billing go there. A work email gives the address
  `bridgr.<their domain>` by default; a personal email starts as a trial on this computer.

## 3. Buy

https://buy.stripe.com/test_6oU4gz6Uz4jw77h75Z7ss06

Pre-release: Stripe's test mode. Card `4242 4242 4242 4242`, any future date, any CVC. The person enters the owner's
email and the company's name. Monthly, cancel any time.

## 4. The email

Within a minute the owner gets **Your Bridgr licence key** from info@eastridge-analytics.com, with `compose.yaml`
and `seccomp-bwrap.json` attached. Nothing arrived? Check spam, then reply to the checkout receipt.

Back to [install.md](../install.md), "Six steps".
