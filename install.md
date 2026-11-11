# Install Bridgr for your company

You are an AI assistant setting up Bridgr for this company. Bridgr answers questions from the company's own systems
and only reads. Read this page. It opens one more page from `install/` only when a step says so: replace
`install.md` in this page's address with `install/<page>.md`. The commands are for a Bash shell; Claude Code on
Windows runs them in Git Bash.

## Rules

- Never ask for, show or repeat a password, API key or licence key.
  Secrets are typed by the person at a hidden prompt. Or they go into Bridgr's own screen in their browser.
- You never see or type the licence key either. The one command that uses it, step 5, reads it from `compose.yaml`
  and pipes it straight into Docker. Run it yourself, like any other step.
- `compose.yaml` holds the licence key. Never print it whole: read or change one line at a time, with the commands
  below.
- The only sign-in link you may paste into the chat is the one Bridgr prints for the owner.
- Ask the questions below together, before the first step. After that, stop for the owner only when Docker needs
  them (step 1) or Bridgr says so (`person` is true below).
- Say only what the owner must do or wait for, in plain words. Don't report each step you did, and don't explain how
  a command works unless they ask.
  Don't use words like registry, image, compose, port, tag or CNAME unless they asked.

## Before you start

Ask these, one at a time. Skip any the person already answered.

1. "Do you have the Bridgr licence email? The subject is *Your Bridgr licence key*. Where are its two attachments
   saved?" No email: open [install/buy.md](install/buy.md) and stop until it arrives.
2. "Should I set Bridgr up on this computer to try it, or on a server your team can reach?"
   This computer is a trial: only this computer can open it, and nothing is lost when it moves to a server later.
   A server: confirm the address now, so the DNS can be on its way during the download (step 3 shows where it is):
   "Your team will open Bridgr at https://bridgr.yourcompany.com. Is that right?"
3. Say: "Bridgr will be able to see this computer's drive, read-only, and you choose on its screen what goes on the
   map. Say now if you'd rather it didn't." No answer, or fine: step 4's drive line. No: Bridgr sees only the `files`
   folder beside `compose.yaml`.

Don't ask about the AI key. Check for Claude Code's sign-in yourself: `ls ~/.claude/.credentials.json`. Found (Linux
and Windows): Bridgr uses it, through step 4's sign-in line. Not found, or a Mac (its sign-in is in the keychain):
ask "Bridgr needs an Anthropic API key to answer questions. Do you have one, or should I tell you how to get one?"
They type it on Bridgr's screen later, never here.

## Six steps

1. **Docker.** Run `docker info --format '{{.ServerVersion}}'`. A version number: go on. "Cannot connect": Docker is
   installed but not running; start it as below and wait. Not installed: install it.
   - Linux server: `curl -fsSL https://get.docker.com | sh`, then `sudo systemctl enable --now docker`.
   - Windows: say "Installing Docker, the free app Bridgr runs in. Windows will ask you to allow it." Then:

         curl -L -o "Docker Desktop Installer.exe" "https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe"
         powershell -c "Start-Process '.\Docker Desktop Installer.exe' -Wait -Verb RunAs -ArgumentList 'install','--accept-license','--quiet'"
         powershell -c "Start-Process 'C:\Program Files\Docker\Docker\Docker Desktop.exe'"

     If the installer says WSL is missing, the owner runs `wsl --install --no-distribution` in PowerShell as
     administrator and restarts the computer; then start again from step 1. A new terminal may be needed before
     `docker` is found.
   - Mac: say "Installing Docker, the free app Bridgr runs in. Your Mac will ask for your password." Use `arm64`
     below on Apple silicon (`uname -m` says `arm64`), `amd64` on Intel:

         curl -L -o Docker.dmg https://desktop.docker.com/mac/main/arm64/Docker.dmg
         sudo hdiutil attach Docker.dmg && sudo /Volumes/Docker/Docker.app/Contents/MacOS/install --accept-license --user=$USER && sudo hdiutil detach /Volumes/Docker
         open -a Docker

   - Then wait until `docker info --format '{{.ServerVersion}}'` prints a version, up to two minutes.
   - `--accept-license` accepts Docker's own terms for the owner: Docker Desktop is free for a company under 250
     people and $10M a year; a bigger one needs Docker's paid plan.
   - They can't install software here: stop. Eastridge can host Bridgr instead; they reply to the licence email.

   Then run `docker compose version`. It must print `Docker Compose version v2` or later. If it fails, or the
   only one there is the old `docker-compose`, install the Compose plugin: on a Linux server,
   `sudo apt-get install -y docker-compose-plugin` (or run the get.docker.com line above, which includes it). Docker
   Desktop already has it. An old Compose crashes Bridgr when it restarts.
2. **Files.** The two attachments, `compose.yaml` and `bridgr-security.json`, go together in one folder: the one the
   owner named, or a new one. Run the rest of the commands in that folder. (Emails before 11 November 2026 call the
   second file `seccomp-bwrap.json`: that file works as it is, because its compose.yaml uses that name.)
3. **Address.** See it with `grep -n 'address: &address' compose.yaml`. This computer: set it to
   `http://localhost:8080`, then read section C of [install/address.md](install/address.md):

       sed -i 's|address: &address "[^"]*"|address: \&address "http://localhost:8080"|' compose.yaml

   A server: edit the line if the owner gave another address. Something already serves HTTPS in front of this
   server: read [install/address.md](install/address.md), B.
4. **What Bridgr may read.** Add the lines that apply under `volumes:` in the `bridgr:` service, one `sed` each, then
   check with `grep -n ':ro' compose.yaml`: each line you added shows once, right under `bridgr-data:/data`. Missing
   or twice: fix it by hand before going on.
   - Claude Code's sign-in, when you found it:

         sed -i 's|^      - bridgr-data:/data.*|&\n      - ~/.claude/.credentials.json:/home/bridgr/.claude/.credentials.json:ro|' compose.yaml

   - The drive, unless the owner said no. Windows: `C:/:/host/c:ro`, and `D:/:/host/d:ro` for a second drive.
     Linux: `/:/host:ro`. Mac: `/Users:/host/Users:ro`. For example, on Windows:

         sed -i 's|^      - bridgr-data:/data.*|&\n      - C:/:/host/c:ro|' compose.yaml

5. **Sign in to Bridgr's download.** Run this yourself. It reads the licence key from the file and passes it
   straight to Docker, so nobody sees it:

       grep -o 'brg_[a-z]*_[0-9a-f]*' compose.yaml | docker login registry.bridgr-platform.com -u licence --password-stdin

   It prints `Login Succeeded`.
6. **Start Bridgr.** Say: "Bridgr is downloading, about 5 to 10 minutes." Then start it, in the background or with a
   15-minute timeout:
   - A server: `mkdir -p files/uploads && docker compose up -d`
   - This computer (a trial), Bridgr alone: `mkdir -p files/uploads && docker compose up -d bridgr`

## Then follow Bridgr

Run this and read the JSON. Check the rows in this order; the first that fits is the one.

    docker compose run --rm bridgr status --json

| If | Do |
|---|---|
| `next` is `terms`, `key`, `data` or `done` | Your part is over. Open `open_url` in the owner's browser if it is set (`open '<url>'` on a Mac, `xdg-open '<url>'` on Linux, `powershell -c "Start-Process '<url>'"` on Windows), else Bridgr's address. Say `say_to_person`, then the link on its own line. Stop. |
| `person` is true | The address on a server: say `say_to_person` word for word and wait for them to say it's done. Then run `run`, and run status again. |
| `wait_seconds` is above 0 | Bridgr is working by itself. Wait that long, then run status again. |
| `run` is set | Run exactly that command. Then run status again. |

Exit code 2 means more to do and is normal. Exit code 1 is an error:
[install/troubleshooting.md](install/troubleshooting.md). A trial's first answer looks like this (cut short):

    {"next": "terms", "person": true, "open_url": "http://localhost:8080/#signin=...", "run": "",
     "say_to_person": "Bridgr is ready. Open this link to accept the licence terms and give Bridgr your data. ...",
     "wait_seconds": 0, "steps": [...]}

## Bridgr stops for the owner

On a server the address comes first: you check it, and only if the check fails does the owner's IT add one DNS
record ([install/address.md](install/address.md), A). Then you hand over `open_url`, the owner's one-time sign-in
link: it works once, for 24 hours, and asking status again gives the same link until it's used. Everything after
that is on Bridgr's screen and the owner's to do: the licence terms, the AI key only without Claude Code's sign-in,
and the data. You don't wait for them: `next` is `done` once they finish, without you.

## After it's set up

- **People:** Settings, People, or `docker compose run --rm bridgr people add EMAIL --name "Their Name"`. It needs a
  web address first. Each person gets a one-time sign-in link the owner sends them privately. To add Bridgr to their
  own assistant, they paste the connect line from the [README](README.md).
- **More data later:** Settings, Folders, Add data. Or files in the `files` folder, then
  `docker compose run --rm bridgr data add` (no path: it reads that folder).
- **A web address later:** [install/address.md](install/address.md), D.
- **A mailbox** is optional: Settings, Mailbox, whenever the company wants Bridgr to send email.
- **Update:** change the version on the `image:` line, then `docker compose pull && docker compose up -d`. Data stays.
- **Start at boot:** `sudo systemctl enable docker`. Bridgr restarts by itself.
- **Back up:** the `bridgr-data` Docker volume.
- **Cancel or change the card:** the manage link in the licence email. Bridgr pauses when the paid period ends;
  nothing is deleted.
- **Help:** reply to the licence email, or https://www.bridgr-platform.com/contact.

Every setting has a terminal command, and the owner can install by hand: [install/terminal.md](install/terminal.md).
