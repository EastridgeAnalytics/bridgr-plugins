# A trial on this computer

The address is `http://localhost:8080`. Only this computer can reach Bridgr. Nothing is lost when it gets a web
address later.

## Start it

Start Bridgr alone, without the HTTPS service, instead of step 5 in [install.md](../install.md):

```sh
mkdir -p files/uploads && docker compose up -d bridgr
```

Then give the person the one-time link from `docker compose run --rm bridgr signin` ([install.md](../install.md),
"Then give the person one link"). It opens `http://localhost:8080` signed in. No email is needed on a trial. On a server reached over SSH, the person first runs this on their
own computer: `ssh -L 8080:localhost:8080 <server>`.

The logs say `address: local trial at http://localhost:8080`, and the owner sees a reminder on the screen. Claude
Code and Codex on this computer can connect. Claude's and ChatGPT's apps, and the rest of the team, need a web
address.

Go back to [install.md](../install.md), "Then follow Bridgr".

## Later: give it a web address

When the team should reach it, read [web-address.md](web-address.md).
