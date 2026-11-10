# Everything from the terminal

Every setting on Bridgr's screen has a terminal command. Run them on the server, in the folder with `compose.yaml`:

```sh
docker compose run --rm bridgr <command>
```

`docker compose run --rm bridgr --help` lists them too.

Secrets (the AI key, a database password, a mailbox app password) are typed by the person at a hidden prompt, or
read from a file with `--password-file` or `--secret-file`. They are never part of the command, and an assistant
lets the person type them.

| On the screen | In the terminal |
|---|---|
| The checklist | `status`, or `status --json` for an assistant |
| Licence terms | `terms show` to read them. The owner then runs `setup terms --by <their email> --yes` |
| Settings, AI key | `setup key` |
| Settings, Address | `setup domain`, `setup domain bridgr.yourcompany.com`, `setup domain --check` |
| Settings, Folders | `data list`, `data add /files`, `data look NAME`, `data remove NAME` |
| Settings, Connections | `database list`, `database add NAME --kind postgres --host H --database D --account A`, `database password NAME` |
| Settings, Mailbox | `mailbox status`, `mailbox add --provider gmail --address bridgr@yourcompany.com`, `mailbox skip`, `mailbox remove` |
| Settings, People | `people list`, `people add colleague@yourcompany.com --name "Their Name"`, `people remove EMAIL` |
| Ask a question | `ask "<question>"` |

Notes:

- Files you put in `files/` beside `compose.yaml` are at `/files` inside Bridgr. Leave `files/uploads` in place.
- Databases need `BRIDGR_CREDENTIALS_ENABLED: "true"` in `compose.yaml`, and a read-only account made for Bridgr.
- Without a mailbox, `people add` prints a one-time sign-in link for the owner to send that person privately.

## status --json, field by field

| Field | Meaning |
|---|---|
| `next` | The next step's id, or `"done"`. |
| `person` | `true` when the next step needs the human. |
| `say_to_person` | One plain sentence to say to the owner when `person` is true. |
| `run` | The exact command to run next when `person` is false. |
| `wait_seconds` | Above 0 while Bridgr works by itself (for example mapping data). Wait, then check again. |
| `steps` | Every step, with its state (`done`, `next`, `todo`, `locked`) and why. |

Exit codes: 0 all done, 2 more to do, 1 an error.
