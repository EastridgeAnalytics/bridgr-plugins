# Install by hand, without an assistant

The same steps as [install.md](../install.md), written for a person.

1. **Buy,** if you haven't: [buy.md](buy.md). You get an email with `compose.yaml` and `seccomp-bwrap.json`.
2. **Put both files in one folder** on the server, for example `/opt/bridgr`.
3. **Check the address** on the `address: &address` line in `compose.yaml`. It is filled in from your email's domain,
   or `http://localhost:8080` for a personal email. Edit it now if it is wrong: the licence locks to an address only
   once Bridgr proves it works there.
   - Server behind a load balancer or a host that serves HTTPS: [proxy.md](proxy.md).
   - Trying it on this computer: [local-trial.md](local-trial.md).
   - A server with ports 80 and 443 open: point DNS at it ([web-address.md](web-address.md)).
4. **Sign in to Bridgr's registry** in that folder. It reads the key from the file, so you never type or see it:

   ```sh
   grep -o 'brg_[a-z]*_[0-9a-f]*' compose.yaml | docker login registry.bridgr-platform.com -u licence --password-stdin
   ```

5. **Start it:** `mkdir -p files/uploads && docker compose up -d`
6. **Check it:** `docker compose logs bridgr`. Within a minute you see `licence: active for ...` and a box headed
   **First sign-in for you@yourcompany.com (the owner)** with a one-time link. Problems: [troubleshooting.md](troubleshooting.md).
7. **Sign in** with that link in your browser. It works once, for 24 hours; each restart prints a fresh one until you
   have signed in. Read and accept the licence terms.
8. **Your AI key:** on the screen, **Settings, AI key**. Or `docker compose run --rm bridgr setup key`.
9. **Your data:** on the screen, **Settings, Folders**, choose **Upload a data file** (CSV, Excel or Parquet, up to
   25 MB). Or put files in `files/` beside `compose.yaml` and run `docker compose run --rm bridgr data add /files`.
   Databases: **Settings, Connections** ([terminal.md](terminal.md) has the commands).
10. **Ask a question** on the screen to check it answers.
11. **Your team:** [team.md](team.md). Later: [run-it.md](run-it.md).

The checklist on Bridgr's screen, or `docker compose run --rm bridgr status`, always shows what is left.
