# Everything from the terminal

Every setting on Bridgr's screen has a terminal command. Run them on the server, in the folder with `compose.yaml`:

    docker compose run --rm bridgr <command>

`docker compose run --rm bridgr --help` lists them. Secrets (the AI key, a database password, a mailbox app
password) are typed by the person at a hidden prompt, or read from a file with `--password-file` or
`--secret-file`. They are never part of the command.

| On the screen | In the terminal |
|---|---|
| The checklist | `status`, or `status --json` for an assistant |
| Signing in | `signin` prints the owner's one-time sign-in link; `signin EMAIL` one for a person on the list |
| Licence terms | `terms show` to read them; the owner accepts with `setup terms --by <their email> --yes` |
| Settings, AI key | `setup key` |
| Settings, Address | `setup domain`, `setup domain bridgr.yourcompany.com`, `setup domain --check` |
| Settings, Folders | `data list`, `data add /files`, `data look NAME`, `data remove NAME` |
| Settings, Connections | `database list`, `database add NAME --kind postgres --host H --database D --account A`, `database password NAME` |
| Settings, People | `people list`, `people add EMAIL --name "Their Name"`, `people remove EMAIL` |
| Settings, Mailbox (optional) | `mailbox status`, `mailbox add --provider gmail --address bridgr@yourcompany.com`, `mailbox skip`, `mailbox remove` |
| Ask a question | `ask "<question>"` |

- Files in `files/` beside `compose.yaml` are at `/files` inside Bridgr. Leave `files/uploads` in place.
- Databases need `BRIDGR_CREDENTIALS_ENABLED: "true"` in `compose.yaml` and a read-only account made for Bridgr.
- Without a mailbox, `people add` prints a one-time sign-in link for the owner to send that person privately. It
  lasts 24 hours.

## status --json, field by field

| Field | Meaning |
|---|---|
| `next` | The next step's id, or `done`. |
| `person` | `true` when the next step needs the owner. |
| `say_to_person` | What to say to the owner, word for word. Also set when `next` is `done`. |
| `open_url` | The owner's one-time sign-in link, while the licence terms are next. Open it in their browser. |
| `run` | The command to run: now when `person` is false, after the owner is done when it is true. |
| `wait_seconds` | Above 0 while Bridgr works by itself (mapping data). Wait, then check again. |
| `steps` | Every step with its state (`done`, `next`, `todo`, `optional`, `later`) and why. |

Exit codes: 0 done, 2 more to do, 1 an error.

## By hand, without an assistant

Do install.md's six steps yourself. Then `docker compose logs bridgr` shows `licence: active for` your address
and a box, `First sign-in for` the owner, with a one-time link. Open it: the licence terms come first, then your AI
key and your data, on the screen.
