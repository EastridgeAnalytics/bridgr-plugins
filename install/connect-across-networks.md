# Bridge across networks: connect Bridgr to data in another network

Read this when Bridgr runs on one server and a company system it should read is somewhere it can't reach: a database
in another cloud or VPC, a server in the office, anything without a public address. The sign is a connection that
says "nothing answered at that host and port". Then go back to [install.md](../install.md) or
[cloud.md](cloud.md).

Bridgr only reads. It needs one outbound connection from its server to the system's port (Postgres 5432, MySQL 3306,
SQL Server 1433, and so on). Nothing has to reach Bridgr's server in return. Choose one way below, with the person
and their cloud or network team. Never open a database to the whole internet to make it work.

| The system is | Use |
|---|---|
| In a private network: a VPC with no public address, an office server, a laptop | A. Tailscale |
| A cloud database that already has a public address the company keeps | B. Allow only Bridgr's address |
| Behind something the company already runs, such as a VPN or Cloudflare | Ask their network team to give Bridgr's server the same access a staff laptop has, then test it as in C |

## A. Tailscale (recommended for private networks)

Tailscale joins Bridgr's server and the system's network into one private network, the company's tailnet. Nothing is
opened to the internet. The person or their network team does the parts marked *person*.

1. *Person:* in the Tailscale admin console, Settings, Keys, generate a **one-off, pre-approved** auth key for
   Bridgr's server, with a tag such as `tag:bridgr` if the tailnet uses tags (a tagged server's key never expires).
   They run step 2 themselves with the key, in their own terminal, never in the chat.
2. On Bridgr's server, install Tailscale and join, accepting the routes the next step adds:

   ```bash
   curl -fsSL https://tailscale.com/install.sh | sh
   sudo tailscale up --accept-routes --auth-key='<the key>'   # the person runs this line, so the key stays with them
   tailscale ip -4                                            # a 100.x address: the server is on the tailnet
   ```

3. Next to the system, one machine shares its network with the tailnet, a *subnet router*. *Person or their network
   team:* on a small Linux machine in the same network as the system (a spare VM in that VPC is fine):

   ```bash
   curl -fsSL https://tailscale.com/install.sh | sh
   echo 'net.ipv4.ip_forward = 1' | sudo tee /etc/sysctl.d/99-tailscale.conf
   sudo sysctl -p /etc/sysctl.d/99-tailscale.conf      # only this file, never sysctl --system
   sudo tailscale up --advertise-routes=<the network, such as 10.0.0.0/16>
   ```

   Then approve the route in the admin console (Machines, the router, Subnets), and allow Bridgr's server to reach it
   in the access controls. If the system can run Tailscale itself, install it there instead and skip the router.

4. In Bridgr, connect the system with its **private IP address** (such as `10.0.3.12`), not a Tailscale name: Bridgr
   runs in a container that may not resolve tailnet names. Test as in C.

If the server's key wasn't tagged, turn off its key expiry (admin console, Machines, the server, Disable key expiry),
or Bridgr loses the system when the key expires. To remove: `sudo tailscale logout` on the server, and remove the
route.

## B. Allow only Bridgr's address

For a cloud database the company already keeps reachable on a public address. Bridgr's server always connects from
its public IP. Read it on the server:

```bash
curl -fsS https://ifconfig.me; echo
```

*Person or their cloud team:* allow that one address, with `/32`, on the database's port, in the database's firewall
or security group, and keep TLS on. Nothing else changes. If the server is ever deleted and rebuilt, its address
changes: allow the new one and remove the old one.

| Where the database is | Where the rule goes |
|---|---|
| AWS RDS | The database's security group: inbound, the port, source `<IP>/32` |
| Azure Database | The server's Networking page: a firewall rule for that one IP |
| Google Cloud SQL | Connections, Networking: an authorized network `<IP>/32` |
| Anything else | Its firewall: allow that one IP on that one port |

## C. Test it

On Bridgr's server itself (over SSH), before adding the system in Bridgr. From the laptop the test can fail even
when Bridgr's path is open, because the rule in B allows only the server's address:

```bash
nc -vz -w 5 <the system's IP or host> <port>       # "succeeded" or "open": the network path works
```

"Timed out" or "refused": the path isn't open yet. Recheck the route or rule, not the password. Then add the system
on Bridgr's screen (Settings, Connections) or let the person's assistant start it, and Bridgr checks it for real.

| What Bridgr or `nc` says | What it means |
|---|---|
| nothing answered at that host and port | The network path isn't open: the route, the rule or the system's own firewall |
| no host by that name | Use the IP address instead of a name |
| the password was rejected | The path works. Now it's the account or the password |
