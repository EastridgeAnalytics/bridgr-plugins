# Run it: updates, backups, cancelling, help

- **Update:** change the version in the `image:` line of `compose.yaml`, then
  `docker compose pull && docker compose up -d`. Data stays in the `bridgr-data` volume. Updates need an active
  subscription: the registry checks the licence key on every pull. On a new server, or after Docker is reset, run the
  registry sign-in again ([install.md](../install.md), step 4).
- **Start at boot:** the container restarts by itself (`restart: unless-stopped`). Make sure Docker starts at boot:
  `sudo systemctl enable docker`.
- **Back up:** the `bridgr-data` Docker volume holds everything Bridgr keeps.
- **Cancel or change the card:** the manage link in the licence email. After the paid period ends, Bridgr pauses: its
  screen and every assistant say "Bridgr for Your Company is paused" and who to ask. Nothing is deleted, and it starts
  again within minutes of renewing.
- **Help:** reply to the licence email, or https://www.bridgr-platform.com/contact.
