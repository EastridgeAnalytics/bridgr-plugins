# The server already has HTTPS in front of it

For a load balancer, an ingress, a reverse proxy, or a host that serves HTTPS for its servers. Do this before the
first `docker compose up -d`, then go back to [install.md](../install.md), step 3.

## 1. Ask the person two things

1. **Which port on this server does the HTTPS front door forward to?** For example 8080, or 8000.
2. **Can anyone on the internet open the address without signing in to the host first?** Some hosts keep new
   addresses private until you make them public. Bridgr signs people in itself, so the front door must let
   everyone through. If it is private, the person makes it public in the host's settings.

## 2. Change compose.yaml

1. Delete the `https:` service and its volumes. The front door already serves HTTPS.
2. Under `bridgr:`, change the ports line from `127.0.0.1:8080:8080` to `<port>:8080`, using the port from question 1.
   For example `8000:8080`.
3. Keep the `address:` line as the public `https://` address, such as `https://bridgr.yourcompany.com`.

## 3. DNS

Keep the DNS the front door needs. A CNAME to the host's name is fine. Do not replace it with an A record to this
server's IP: the front door is what the internet should reach.

## 4. Firewall and headers

- Allow that port only from the front door, if the firewall lets you.
- The front door must pass the original `Host` header through.

## How you know it worked

After `docker compose up -d`, `status --json` marks the web address as done by itself within a few minutes. Bridgr
fetches a one-time code from itself through the public address, so it proves the whole path works. If it says the
address answers but is "a different server", the front door is pointing somewhere else: check its port.
