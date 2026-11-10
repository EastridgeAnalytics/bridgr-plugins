# Install Bridgr for your company

You are an AI assistant setting up Bridgr, a read-only data assistant, on a server this company controls. Read this
page only. It sends you to one more page when you need it.

Every page here sits next to this one: replace `install.md` in this page's address with `install/<page>.md`.

## Rules

- Never ask for, accept, show or repeat a password, API key, licence key, token or sign-in link in the chat.
  Secrets are typed by the person at a hidden prompt.
- Stop for the owner only when Bridgr says so (`person` is true below). Do everything else yourself.
- Tell the person what you did and what you saw at each step, in plain words. The person may not be technical.
  Say what it means for them, not how it works: "Bridgr is downloading, about 10 minutes", not "pulling
  layers from the registry". Don't use words like registry, image, compose, port, tag or CNAME unless they
  asked. Keep each update to one or two short sentences, and say when they need to do something.

## Start: one question

Ask the person: **"Do you have the Bridgr licence email (subject: Your Bridgr licence key)?"**

- **No:** open [install/buy.md](install/buy.md) and stop here until it arrives.
- **Yes:** carry on.

## Four steps

1. **Files.** From the email, save `compose.yaml` and `seccomp-bwrap.json` together in one folder on the server.
2. **Address.** This is the web address people will type to open Bridgr, like `https://bridgr.yourcompany.com`.
   Read the line starting `address: &address` in `compose.yaml` and ask the person in plain words, for example:
   "Bridgr will live at https://bridgr.yourcompany.com. Is that where your team should open it? If you just
   want to try it on this computer first, I can set it up so only this computer can open it." If they want
   something else, edit that line now. Then pick the one page that fits:
   - The server already has HTTPS in front of it (a load balancer, ingress, or a host that serves HTTPS):
     [install/proxy.md](install/proxy.md).
   - The address is `http://localhost:8080` (a trial on this computer): [install/local-trial.md](install/local-trial.md).
   - Otherwise (a server with ports 80 and 443 open): nothing to read now.
3. **Sign in to Bridgr's registry,** in that folder. This reads the licence key without printing it:

   ```sh
   grep -o 'brg_[a-z]*_[0-9a-f]*' compose.yaml | docker login registry.bridgr-platform.com -u licence --password-stdin
   ```

   It prints `Login Succeeded`.
4. **Start Bridgr:**

   ```sh
   mkdir -p files/uploads && docker compose up -d
   ```

## Then follow Bridgr

Run this, read the JSON, and do what it says. Repeat until `next` is `done`.

```sh
docker compose run --rm bridgr status --json
```

| If | Do |
|---|---|
| `person` is true | Say `say_to_person` to the owner, word for word. Wait for them. |
| `wait_seconds` is above 0 | Bridgr is working by itself. Wait that long, then run status again. |
| `run` is not empty | Run exactly that command. |
| `next` is `done` | Stop. Bridgr is set up. |

Exit code 2 means "more to do" and is normal. Exit code 1 is an error: read
[install/troubleshooting.md](install/troubleshooting.md).

Bridgr stops for the owner three times, in this order: the licence terms (they read and accept them, at their first
sign-in on the screen or with `terms show` and `setup terms` in the terminal), their AI key, and their data. After
that it works. Two short choices finish the list: a mailbox, which they can add or skip for now, and their team,
which they can add with or without a mailbox. Then `next` is `done`.

## Only when you need it

- Owner prefers the terminal to the screen, or wants every command: [install/terminal.md](install/terminal.md)
- Bringing in the team and their assistants: [install/team.md](install/team.md)
- Updates, backups, cancelling, help: [install/run-it.md](install/run-it.md)
- A person installing by hand, without an assistant: [install/by-hand.md](install/by-hand.md)
