# Install Bridgr for your company

You are an AI assistant setting up Bridgr, a read-only data assistant, for this company. Read this page only. It
sends you to one more page when you need it.

Every page here sits next to this one: replace `install.md` in this page's address with `install/<page>.md`.

## Rules

- Never ask for, accept, show or repeat a password, API key, licence key, token or sign-in link in the chat.
  Secrets go into Bridgr's own page in the person's browser, or a hidden prompt.
- Stop for the owner only when Bridgr says so (`person` is true below). Do everything else yourself.
- Tell the person what you did and what you saw at each step, in plain words. The person may not be technical.
  Say what it means for them, not how it works: "Bridgr is downloading, about 5 to 10 minutes", not "pulling
  layers from the registry". Don't use words like registry, image, compose, port, tag or CNAME unless they
  asked. Keep each update to one or two short sentences, and say when they need to do something.

## Start: two questions

1. Ask: **"Do you have the Bridgr licence email (subject: Your Bridgr licence key)?"**
   - **No:** open [install/buy.md](install/buy.md) and stop here until it arrives.
2. Ask: **"Should I set up Bridgr on this computer to try it, or on a server your team can reach?"**
   - **This computer:** a trial. Only this computer can open it. Nothing is lost when it moves to a server later.
   - **A server:** the team will reach it at an address like `https://bridgr.yourcompany.com`.

## Five steps

1. **Docker.** Run `docker compose version`. If it works, go on. If not:
   - **Linux server:** install it yourself: `curl -fsSL https://get.docker.com | sh`, then
     `sudo systemctl enable --now docker`. Tell the person: "Installing Docker, the free tool Bridgr runs in."
   - **Mac or Windows:** tell the person: "Bridgr needs a free app called Docker Desktop. Please install it from
     https://www.docker.com/products/docker-desktop/, open it once, then tell me 'done'." Wait for them.
   - **They can't install software here:** stop and tell them Eastridge can host Bridgr for them instead; they reply
     to the licence email.
2. **Files.** From the email, save `compose.yaml` and `seccomp-bwrap.json` together in one folder.
3. **Address.** Read the line starting `address: &address` in `compose.yaml`.
   - **This computer:** set it to `http://localhost:8080` and read [install/local-trial.md](install/local-trial.md).
   - **A server:** confirm the address with the person in plain words ("Your team will open Bridgr at
     https://bridgr.yourcompany.com. Is that right?") and edit the line if not. If the server already has HTTPS in
     front of it (a load balancer, ingress, or a host that serves HTTPS), read [install/proxy.md](install/proxy.md).
4. **Sign in to Bridgr's download,** in that folder. This reads the licence key without printing it:

   ```sh
   grep -o 'brg_[a-z]*_[0-9a-f]*' compose.yaml | docker login registry.bridgr-platform.com -u licence --password-stdin
   ```

   It prints `Login Succeeded`.
5. **Start Bridgr.** The first start downloads Bridgr, about 5 to 10 minutes. Start it now and, while it downloads,
   tell the person: "Bridgr is downloading, about 5 to 10 minutes. Meanwhile, please get an Anthropic API key at
   https://console.anthropic.com (you'll paste it into Bridgr's page, not here)."

   ```sh
   mkdir -p files/uploads && docker compose up -d
   ```

   On this computer, use `docker compose up -d bridgr` instead ([install/local-trial.md](install/local-trial.md)).

## Then give the person one link

When Bridgr is running, run this and give the person the one-time link it prints, privately (not in a team chat):

```sh
docker compose run --rm bridgr signin
```

Say: "Open this link to finish setting up Bridgr. It works once." Opening it signs them in, on this computer or a
server alike. The link is a sign-in, so don't keep it or repeat it after they've opened it.

From there Bridgr walks them through three screens: accept the licence terms, paste their AI key, add their data.

## Then follow Bridgr

Run this, read the JSON, and do what it says. Repeat until `next` is `done`.

```sh
docker compose run --rm bridgr status --json
```

| If | Do |
|---|---|
| `person` is true | If `run` is not empty, run it first and give the owner what it prints privately (a one-time sign-in link). Then say `say_to_person` word for word, and wait for them to say "done". |
| `wait_seconds` is above 0 | Bridgr is working by itself. Wait that long, then run status again. |
| `run` is not empty (and `person` is false) | Run exactly that command. |
| `next` is `done` | Stop. Bridgr is set up. |

Exit code 2 means "more to do" and is normal. Exit code 1 is an error: read
[install/troubleshooting.md](install/troubleshooting.md).

Bridgr stops for the owner three times, in this order, each on its own page in their browser: the licence terms
(read them and click I accept), their AI key, and their data. After that it works. Two short choices finish the
list: a mailbox, which they can add or skip for now, and their team, which joins once Bridgr has a web address.
Then `next` is `done`.

## Only when you need it

- Owner prefers the terminal to the screen, or wants every command: [install/terminal.md](install/terminal.md)
- Giving Bridgr a web address later: [install/web-address.md](install/web-address.md)
- Bringing in the team and their assistants: [install/team.md](install/team.md)
- Updates, backups, cancelling, help: [install/run-it.md](install/run-it.md)
- A person installing by hand, without an assistant: [install/by-hand.md](install/by-hand.md)
