# Install Bridgr for your company

You are an AI assistant setting up Bridgr for this company. Bridgr answers questions from the company's own systems
and only reads. Read this page. It opens one more page from `install/` only when a step says so: replace
`install.md` in this page's address with `install/<page>.md`. The commands are for a Bash shell; Claude Code on
Windows has one.

## Rules

- Never ask for, show or repeat a password, API key or licence key.
  Secrets are typed by the person at a hidden prompt. Or they go into Bridgr's own screen in their browser.
- `compose.yaml` holds the licence key. Never print it whole: read or change one line at a time, with the commands
  below.
- The only links you may paste into the chat are the sign-in links Bridgr prints for the owner, and only when you
  can't open them for the owner yourself.
- Stop for the owner only when Bridgr says so (`person` is true below). Do everything else yourself.
- Tell the owner what you did in plain words, one or two sentences at a time. Say what it means for them, not how it
  works: "Bridgr is downloading, about 5 to 10 minutes."
  Don't use words like registry, image, compose, port, tag or CNAME unless they asked.

## Before you start

Ask these, one at a time. Skip any the person already answered.

1. "Do you have the Bridgr licence email? The subject is *Your Bridgr licence key*."
   No: open [install/buy.md](install/buy.md) and stop until it arrives.
2. "Should I set Bridgr up on this computer to try it, or on a server your team can reach?"
   This computer is a trial: only this computer can open it, and nothing is lost when it moves to a server later.
3. "Bridgr needs an Anthropic API key to answer questions. If Claude Code is signed in on this computer, Bridgr can
   use that instead. Which would you like?"

## Six steps

1. **Docker.** Run `docker info --format '{{.ServerVersion}}'`. A version number: go on. Otherwise:
   - "Cannot connect" on Mac or Windows: Docker Desktop is installed but not running. Ask them to open it.
   - Not installed, Linux server: `curl -fsSL https://get.docker.com | sh`, then `sudo systemctl enable --now docker`.
   - Not installed, Mac or Windows: "Bridgr needs a free app called Docker Desktop. Please install it from
     https://www.docker.com/products/docker-desktop/, open it once, then tell me." Wait for them.
   - They can't install software here: stop. Eastridge can host Bridgr instead; they reply to the licence email.
2. **Files.** Save the two attachments, `compose.yaml` and `seccomp-bwrap.json`, together in one folder. Run the
   rest of the commands in that folder.
3. **Address.** See it with `grep -n 'address: &address' compose.yaml`.
   - This computer: set it to `http://localhost:8080`, then read [install/address.md](install/address.md), C:

         sed -i 's|address: &address "[^"]*"|address: \&address "http://localhost:8080"|' compose.yaml

   - A server: confirm it in plain words: "Your team will open Bridgr at https://bridgr.yourcompany.com. Is that
     right?" Edit the line if not. Something already serves HTTPS in front of this server: read
     [install/address.md](install/address.md), B.
4. **Claude Code instead of a key** (only if they chose it). Check `ls ~/.claude/.credentials.json` finds the file;
   on a Mac it isn't a file (the sign-in is in the keychain), so they use an API key. Then give Bridgr read-only use
   of it:

       sed -i 's|^      - bridgr-data:/data.*|&\n      - ~/.claude/.credentials.json:/home/bridgr/.claude/.credentials.json:ro|' compose.yaml
       grep -n 'credentials.json' compose.yaml

5. **Sign in to Bridgr's download.** This reads the licence key without printing it:

       grep -o 'brg_[a-z]*_[0-9a-f]*' compose.yaml | docker login registry.bridgr-platform.com -u licence --password-stdin

   It prints `Login Succeeded`.
6. **Start Bridgr.** First say: "Bridgr is downloading, about 5 to 10 minutes." If they chose an API key, add:
   "Meanwhile, please get one at https://console.anthropic.com. You'll type it into Bridgr's screen, not here."
   Then start it. The first start downloads about 600 MB, so give it up to 15 minutes.
   - A server: `mkdir -p files/uploads && docker compose up -d`
   - This computer (a trial), Bridgr alone: `mkdir -p files/uploads && docker compose up -d bridgr`

## Then follow Bridgr

Run this, read the JSON, do what it says. Repeat until `next` is `done`.

    docker compose run --rm bridgr status --json

| If | Do |
|---|---|
| `person` is true | If `open_url` is set, open it in the owner's browser (`open '<url>'` on a Mac, `xdg-open '<url>'` on Linux, `powershell -c "Start-Process '<url>'"` on Windows). If you can't, paste it. Say `say_to_person` word for word and wait for them to say they're done. Then, if `run` is set, run it. At the data stop, see "The data" below. |
| `wait_seconds` is above 0 | Bridgr is working by itself. Wait that long, then run status again. |
| `run` is set and `person` is false | Run exactly that command. |
| `next` is `done` | Say `say_to_person`. Bridgr is set up. |

`next` is `address`, `terms`, `key`, `data` or `done`. Exit code 2 means more to do and is normal. Exit code 1 is an
error: [install/troubleshooting.md](install/troubleshooting.md). A trial's first answer looks like this (cut short):

    {"next": "terms", "person": true, "open_url": "http://localhost:8080/#signin=...", "run": "",
     "say_to_person": "Bridgr is ready for you. I've opened your sign-in link; ...", "wait_seconds": 0, "steps": [...]}

## Bridgr stops for the owner

On a server the address comes first: you check it, and only if the check fails does the owner's IT add one DNS
record ([install/address.md](install/address.md), A). Then three stops, in this order:

- **The licence terms.** Status gives you `open_url`, their one-time sign-in link. Open it. They land on the licence
  terms, tick the box and click **I accept**. The link works once, for 24 hours; asking status again gives the same
  link until it's used.
- **The AI key.** A box asks for it on the screen, or they run `docker compose run --rm bridgr setup key` in their
  own terminal and type it at the hidden prompt. With Claude Code (step 4) this stop is already done.
- **The data.** They upload a file at Settings, Folders, or connect a read-only database at Settings, Connections.
  Or files go in the `files` folder beside `compose.yaml`: if they give you a file's path, copy it there yourself,
  then run `docker compose run --rm bridgr data add` (no path: it reads that folder). It returns once the files are
  on the map, under a minute for a spreadsheet. A big folder takes longer; status then says how long to wait.

Then `next` is `done`. The team is optional and never blocks it; on a trial the address and the team say `later`.

## After it's set up

- **People:** Settings, People, or `docker compose run --rm bridgr people add EMAIL --name "Their Name"`. It needs a
  web address first. Each person gets a one-time sign-in link the owner sends them privately. To add Bridgr to their
  own assistant, they paste the connect line from the [README](README.md).
- **A web address later:** [install/address.md](install/address.md), D.
- **A mailbox** is optional: Settings, Mailbox, whenever the company wants Bridgr to send email.
- **Update:** change the version on the `image:` line, then `docker compose pull && docker compose up -d`. Data stays.
- **Start at boot:** `sudo systemctl enable docker`. Bridgr restarts by itself.
- **Back up:** the `bridgr-data` Docker volume.
- **Cancel or change the card:** the manage link in the licence email. Bridgr pauses when the paid period ends;
  nothing is deleted.
- **Help:** reply to the licence email, or https://www.bridgr-platform.com/contact.

Every setting has a terminal command, and the owner can install by hand: [install/terminal.md](install/terminal.md).
