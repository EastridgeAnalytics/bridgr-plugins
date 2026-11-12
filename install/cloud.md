# A server in your cloud

You are on the person's laptop. Stay there. Create one server in their cloud, then run Bridgr's commands on it
through SSH. Open web pages on the laptop, not the server. Keep [install.md](../install.md)'s rules.

## Before you create anything

Ask: "Which cloud do you already use: AWS, Google Cloud, DigitalOcean or Hetzner? May I use its command-line app
to create one small server for Bridgr? Your team will open it at https://bridgr.yourcompany.com. Is that right?"
Confirm the account or project and the region too. Don't create another account for them.

The person signs the app in themselves, in their own terminal. Never ask for, read or repeat their cloud password
or token. If the app is missing, use that provider's official installation page. Then have the person run the line
that fits. An existing sign-in in the right account is fine.

```bash
aws sso login
# Google Cloud
gcloud auth login
# DigitalOcean
doctl auth init
# Hetzner
hcloud context create bridgr
```

For AWS, an SSO profile must already be set up. If not, the person runs `aws configure sso` first. Use their chosen
profile for every AWS command (`export AWS_PROFILE='<their profile name>'`). DigitalOcean and Hetzner ask the person
for a token in their terminal, never here.
Don't use a service account key as a replacement for the person's sign-in.

Use Ubuntu 24.04, 2 vCPU, 4 GB memory and at least 25 GB of disk. AWS and Google Cloud let you choose 25 GB.
DigitalOcean includes 80 GB and Hetzner includes 40 GB with these sizes. You cannot shrink those bundled disks to
25 GB. Google's e2-medium has two shared vCPUs, not two full-time cores.

**Read the current monthly price before creating the server.** Use the provider's price page or calculator for the
chosen region. Count the disk and public IPv4 too. AWS t3.medium in us-east-1 is about $30.37 a month for the server
alone at 730 hours. DigitalOcean's regular s-2vcpu-4gb is $24 a month with its disk. For Google Cloud, quote the
calculator's e2-medium, 25 GB standard disk and one public IPv4. For Hetzner, read the selected location's monthly
price below and add the primary IPv4 charge. Prices, tax and traffic charges can change. Don't call an estimate a
fixed bill. The Bridgr subscription and AI use are separate.

Say: "This server will cost about <amount and currency> a month, including its disk and public address, before tax
and extra traffic. Bridgr and AI use are separate. Shall I create it?" Wait for a yes. No yes: stop.

The price pages are [AWS](https://aws.amazon.com/ec2/pricing/on-demand/),
[Google Cloud](https://cloud.google.com/products/calculator),
[DigitalOcean](https://www.digitalocean.com/pricing/droplets) and
[Hetzner](https://www.hetzner.com/cloud/cost-optimized/).

Use the person's existing SSH key. Ask which public key file to use if it isn't the default. Never print or copy
the private key. No key yet: the person runs `ssh-keygen -t ed25519` in their terminal and keeps its passphrase
there. Run the rest from a private working folder on the laptop. Keep the non-secret resource IDs there for later.

```bash
KEY="$HOME/.ssh/id_ed25519"
test -f "$KEY.pub"
```

Read only the provider section that fits. Don't run a create command twice if it fails halfway through. Read back
the named resources first and carry on with those. An access, billing, quota or company policy error: stop and ask
the person to fix that in their cloud. Don't give yourself more rights or change company policy.

## AWS

These commands use us-east-1 and its default network. Use the agreed region instead if needed. No default public
subnet: ask the person's cloud team for a public subnet and its network ID. Don't invent a new network.

```bash
export AWS_REGION=us-east-1
export AWS_PAGER=""
aws sts get-caller-identity --query Account --output text
aws ec2 describe-subnets --filters Name=default-for-az,Values=true \
  --query 'Subnets[].{Subnet:SubnetId,Network:VpcId,Zone:AvailabilityZone}' --output table
```

Choose one listed subnet. Set `SUBNET` and `VPC` to its values. Find Canonical's current Ubuntu 24.04 image rather
than copying an old image ID. Then create a key entry and the firewall. Port 22 is for SSH, 80 and 443 for HTTPS.
Where the laptop has a fixed public IP, use that IP with `/32` instead of `0.0.0.0/0` for port 22 only.

```bash
SUBNET='<public subnet ID>'
VPC='<that subnet network ID>'
AMI=$(aws ec2 describe-images --owners 099720109477 \
  --filters 'Name=name,Values=ubuntu/images/hvm-ssd-gp3/ubuntu-noble-24.04-amd64-server-*' \
    Name=state,Values=available \
  --query 'sort_by(Images,&CreationDate)[-1].ImageId' --output text)
aws ec2 import-key-pair --key-name bridgr --public-key-material "fileb://$KEY.pub"
SG=$(aws ec2 create-security-group --group-name bridgr --description 'Bridgr SSH and HTTPS' \
  --vpc-id "$VPC" --query GroupId --output text)
aws ec2 authorize-security-group-ingress --group-id "$SG" --protocol tcp --port 22 --cidr 0.0.0.0/0
aws ec2 authorize-security-group-ingress --group-id "$SG" --protocol tcp --port 80 --cidr 0.0.0.0/0
aws ec2 authorize-security-group-ingress --group-id "$SG" --protocol tcp --port 443 --cidr 0.0.0.0/0
INSTANCE=$(aws ec2 run-instances --image-id "$AMI" --instance-type t3.medium --count 1 \
  --key-name bridgr --subnet-id "$SUBNET" --security-group-ids "$SG" --associate-public-ip-address \
  --credit-specification CpuCredits=standard \
  --block-device-mappings '[{"DeviceName":"/dev/sda1","Ebs":{"VolumeSize":25,"VolumeType":"gp3","DeleteOnTermination":true,"Encrypted":true}}]' \
  --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=bridgr}]' \
  --query 'Instances[0].InstanceId' --output text)
aws ec2 wait instance-running --instance-ids "$INSTANCE"
IP=$(aws ec2 describe-instances --instance-ids "$INSTANCE" \
  --query 'Reservations[0].Instances[0].PublicIpAddress' --output text)
printf '%s\n' "$IP"
SERVER="ubuntu@$IP"
```

## Google Cloud

Use the person's project ID. These commands use us-central1-a and the default network. No default network: ask the
cloud team for a network and subnet, then use those with `--network` and `--subnet`. Don't create another project.

```bash
PROJECT='<project ID>'
ZONE=us-central1-a
gcloud billing projects describe "$PROJECT" --format='value(billingEnabled)'
gcloud services enable compute.googleapis.com --project="$PROJECT"
```

Billing must be linked and the Compute API enabled before creating anything. If the first command says `True`
and the second succeeds, go on. If the cloud team has already confirmed both for this project, skip those two
commands. A denied check or a disabled Cloud Billing API does not mean billing is unlinked. Ask the cloud team to
confirm both, then carry on only after they do. Don't enable another API or add billing permissions just to read
this check. Actual billing isn't linked or Compute isn't enabled: stop until the cloud team fixes that.

Prepare the SSH public key with the server's username. This uses instance SSH keys, not OS Login. If company policy
requires OS Login, stop for the cloud team to arrange access. Don't turn that policy off.

```bash
printf 'bridgr:%s\n' "$(cat "$KEY.pub")" > bridgr-ssh.pub
gcloud compute firewall-rules create bridgr-web --project="$PROJECT" --network=default \
  --direction=INGRESS --allow=tcp:22,tcp:80,tcp:443 --source-ranges=0.0.0.0/0 --target-tags=bridgr
gcloud compute instances create bridgr --project="$PROJECT" --zone="$ZONE" \
  --machine-type=e2-medium --image-family=ubuntu-2404-lts-amd64 --image-project=ubuntu-os-cloud \
  --boot-disk-size=25GB --boot-disk-type=pd-standard --network=default --tags=bridgr \
  --metadata-from-file=ssh-keys=bridgr-ssh.pub --no-service-account --no-scopes
IP=$(gcloud compute instances describe bridgr --project="$PROJECT" --zone="$ZONE" \
  --format='get(networkInterfaces[0].accessConfigs[0].natIP)')
printf '%s\n' "$IP"
SERVER="bridgr@$IP"
```

The new server needs no cloud service account. To restrict SSH to the laptop's public IP, make a separate rule for
22 with that source and leave 80 and 443 open to everyone.

## DigitalOcean

These commands use nyc3. Check that the size is available in the agreed region and read its `PriceMonthly` before
the cost question above. Use the regular size, not a more expensive CPU option.

```bash
doctl compute size list --format Slug,Memory,VCPUs,Disk,PriceMonthly
doctl compute region list
SSH_ID=$(doctl compute ssh-key import bridgr --public-key-file "$KEY.pub" --format ID --no-header)
DROPLET=$(doctl compute droplet create bridgr --region nyc3 --image ubuntu-24-04-x64 \
  --size s-2vcpu-4gb --ssh-keys "$SSH_ID" --wait --format ID --no-header)
doctl compute firewall create --name bridgr --droplet-ids "$DROPLET" \
  --inbound-rules 'protocol:tcp,ports:22,address:0.0.0.0/0 protocol:tcp,ports:80,address:0.0.0.0/0 protocol:tcp,ports:443,address:0.0.0.0/0' \
  --outbound-rules 'protocol:tcp,ports:all,address:0.0.0.0/0 protocol:udp,ports:all,address:0.0.0.0/0 protocol:icmp,address:0.0.0.0/0'
IP=$(doctl compute droplet get "$DROPLET" --format PublicIPv4 --no-header)
printf '%s\n' "$IP"
SERVER="root@$IP"
```

Save the firewall ID printed by its create command as `FIREWALL`. For a fixed laptop IP, use it with `/32` as the
source for 22 only. The server has IPv4 only in this example.

## Hetzner

These commands use nbg1 and the x86 CX23. Read the `prices` for that location, including currency and tax, before
the cost question. Add the primary IPv4 price from Hetzner's price page. Don't switch to an Arm server if this size
is unavailable. Ask the person before changing the size, price or location.

```bash
hcloud server-type describe cx23 -o json
hcloud ssh-key create --name bridgr --public-key-from-file "$KEY.pub"
hcloud firewall create --name bridgr
hcloud firewall add-rule bridgr --direction in --protocol tcp --port 22 --source-ips 0.0.0.0/0
hcloud firewall add-rule bridgr --direction in --protocol tcp --port 80 --source-ips 0.0.0.0/0
hcloud firewall add-rule bridgr --direction in --protocol tcp --port 443 --source-ips 0.0.0.0/0
hcloud server create --name bridgr --type cx23 --image ubuntu-24.04 --location nbg1 \
  --ssh-key bridgr --firewall bridgr --without-ipv6
IP=$(hcloud server ip bridgr)
printf '%s\n' "$IP"
SERVER="root@$IP"
```

With no outbound rules, Hetzner allows outbound traffic. Use the laptop's fixed public IP with `/32` for 22 if
available. Keep 80 and 443 open to everyone.

## Install Bridgr on that server

`SERVER` is the user and public IP from the section above. All `ssh` and `scp` lines below run on the laptop.
Wait for SSH to be ready. On the first connection, check the host key against the cloud's console before trusting
it. Never turn host key checking off. A changed host key is a reason to stop, not delete the old entry blindly.

```bash
ssh -i "$KEY" "$SERVER" 'uname -m && . /etc/os-release && printf "%s\n" "$PRETTY_NAME"'
```

It must be x86_64 and Ubuntu 24.04. Now do [install.md](../install.md)'s six steps on the server, not the laptop:

1. **Docker.** Check it over SSH. If it isn't installed, install it and start it:

   ```bash
   ssh -i "$KEY" "$SERVER" "sudo docker info --format '{{.ServerVersion}}'"
   ssh -i "$KEY" "$SERVER" 'curl -fsSL https://get.docker.com | sudo sh && sudo systemctl enable --now docker'
   ssh -i "$KEY" "$SERVER" 'sudo docker compose version'
   ```

   Skip the install line if Docker already works. Compose must be v2 or later. Use `sudo docker` for this fresh
   Ubuntu user throughout, including status and any command Bridgr returns. Don't install Docker on the laptop.

   Then let Bridgr's sandbox run. Ubuntu 24.04 cloud images stop programs from making their own private sandbox,
   and without it Bridgr can map data but can't answer a question. This one setting allows it, now and after a
   restart:

   ```bash
   ssh -i "$KEY" "$SERVER" 'echo kernel.apparmor_restrict_unprivileged_userns=0 | sudo tee /etc/sysctl.d/60-bridgr-sandbox.conf >/dev/null && sudo sysctl -p /etc/sysctl.d/60-bridgr-sandbox.conf'
   ```

   Apply only that file. Don't run `sysctl --system`: it can switch off the network forwarding Docker turned on,
   and the address stops answering until Docker restarts.
2. **Files.** From the private folder holding the two licence email attachments:

   ```bash
   ssh -i "$KEY" "$SERVER" 'umask 077 && mkdir -p bridgr && chmod 700 bridgr'
   scp -i "$KEY" compose.yaml bridgr-security.json "$SERVER:bridgr/"
   ssh -i "$KEY" "$SERVER" 'chmod 600 bridgr/compose.yaml bridgr/bridgr-security.json'
   ```

   Never print the whole compose file or the licence key. Older email: copy `seccomp-bwrap.json` instead, as
   [install.md](../install.md), step 2 explains.
3. **Address.** Keep the public HTTPS subdomain, never localhost or the server's IP:

   ```bash
   ssh -i "$KEY" "$SERVER" "cd bridgr && grep -n 'address: &address' compose.yaml"
   ```

   If it differs, replace just that line with the agreed address. For example:

   ```bash
   ssh -i "$KEY" "$SERVER" 'cd bridgr && sed -i '\''s|address: &address "[^"]*"|address: \&address "https://bridgr.yourcompany.com"|'\'' compose.yaml'
   ```

   Follow [address.md](address.md), section A. Add an `A` record for `bridgr.<the company domain>` pointing at
   `IP`. If the person manages DNS, give them just that record and wait for it. If you are allowed to use their
   DNS app, follow section A's sign-in rules. On Cloudflare use DNS only, not the proxy. Don't change the domain's
   other records. Remove an old AAAA record for this same name only with permission if it points elsewhere.
4. **What Bridgr may read.** Add no extra mounts. Do not mount the server's drive or the laptop's Claude Code
   sign-in. Keep the attachment's `files/` mount and `bridgr-data` volume. The owner uploads files on Bridgr's
   screen. The owner types an Anthropic API key on that screen too, never in chat. The laptop's Claude Code
   sign-in doesn't sign Bridgr on a different server in.
5. **Sign in to Bridgr's download.** The pipe runs entirely on the server. The licence key never passes through
   the laptop's command output:

   ```bash
   ssh -i "$KEY" "$SERVER" "cd bridgr && grep -o 'brg_[a-z]*_[0-9a-f]*' compose.yaml | sudo docker login registry.bridgr-platform.com -u licence --password-stdin"
   ```

   It must say `Login Succeeded`.
6. **Start Bridgr.** Say: "Bridgr is downloading, about 5 to 10 minutes." Allow 15 minutes for this command:

   ```bash
   ssh -i "$KEY" "$SERVER" 'cd bridgr && mkdir -p files/uploads && sudo docker compose up -d'
   ```

Bridgr's `https` service uses Caddy to get and renew the certificate. Keep ports 80 and 443 open. Don't install a
second web server. Check the address from the server:

```bash
ssh -i "$KEY" "$SERVER" 'cd bridgr && sudo docker compose run --rm bridgr setup domain --check'
```

## Then follow Bridgr from the laptop

Use the same loop as [install.md](../install.md), **Then follow Bridgr**. Each command runs on the server in
`bridgr`. Only web pages open on the laptop.

```bash
ssh -i "$KEY" "$SERVER" 'cd bridgr && sudo docker compose run --rm bridgr status --json'
```

| If | Do |
|---|---|
| `next` is `terms`, `key`, `data` or `done` | Open `open_url` in the person's laptop browser if set, else the Bridgr address. Say `say_to_person`, then hand the owner their link privately. Stop for the owner. |
| `person` is true | Say `say_to_person` word for word and wait for them to say it is done. Run `run` if set, over SSH in `bridgr`, then status again. |
| `wait_seconds` is above 0 | Wait that long, then status again over SSH. |
| `run` is set | Run that command over SSH in `bridgr`, then status again. |

For `run`, keep the returned command unchanged apart from `sudo docker` instead of `docker` for this Ubuntu user.
Never run it on the laptop. Exit code 2 means more to do and is normal. Exit code 1 is an error: read
[troubleshooting.md](troubleshooting.md), running its checks over SSH too. Don't print status JSON containing an
owner link into a shared log. Open the link privately. Save status JSON only in a file only the person can read
(`umask 077`). Never paste cloud keys, licence keys or sign-in links into a report.

The owner link works once, in one browser. To sign the owner in on another browser or computer, run
`ssh -i "$KEY" "$SERVER" 'cd bridgr && sudo docker compose run --rm bridgr signin'` for a fresh link.

Open a page only in the person's permitted laptop browser. If you cannot open it privately, ask the person to open
it themselves. Do not try `xdg-open` on the server or forward a localhost trial instead of fixing the public address.
The owner accepts the terms, types their AI key and adds data on Bridgr's screen. Follow install.md's handoff, not
an unattended attempt to accept terms or supply a made-up key.

## Connect the assistant on this laptop

After the owner finishes, use the connect line from the [README](../README.md), with the agreed address:

```text
Connect me to Bridgr at https://bridgr.yourcompany.com. Fetch and follow https://raw.githubusercontent.com/EastridgeAnalytics/bridgr-plugins/main/setup.md
```

Follow it on the laptop, not over SSH. Claude Code's `/mcp` connects to the server's public
`https://bridgr.yourcompany.com/mcp`. The person signs in and clicks Approve in their laptop's browser. Keep going
until this laptop's `bridgr_status` tool succeeds. A successful status command over SSH is not this test.

## Keep it safe, or remove it later

- Back up the `bridgr-data` Docker volume. It holds Bridgr's state. Also keep `files/` for uploaded source files,
  and a private copy of the two attachments. A backup on this same server is not enough. Keep an encrypted copy
  elsewhere and check that it restores before deleting a server. Don't run `docker compose down -v`.
- The public IP on AWS or Google Cloud can change after stopping and starting. Read it again and update this
  name's A record before checking the address again. For a permanent server, ask the cloud team about reserving
  the address and its cost.
- Stopping a server is not the same as deleting it. Disk and address charges can remain. DigitalOcean and Hetzner
  also charge for powered-off servers. Check the provider's bill.
- To delete it, first get the owner's explicit yes and confirm the backup. Use only the IDs you saved for this
  installation. These commands permanently remove the server and may remove its disk:

  ```bash
  # AWS
  aws ec2 terminate-instances --instance-ids "$INSTANCE"
  aws ec2 wait instance-terminated --instance-ids "$INSTANCE"
  aws ec2 delete-security-group --group-id "$SG"
  aws ec2 delete-key-pair --key-name bridgr
  # Google Cloud
  gcloud compute instances delete bridgr --project="$PROJECT" --zone="$ZONE" --quiet
  gcloud compute firewall-rules delete bridgr-web --project="$PROJECT" --quiet
  # DigitalOcean
  doctl compute droplet delete "$DROPLET" --force
  doctl compute firewall delete "$FIREWALL" --force
  doctl compute ssh-key delete "$SSH_ID" --force
  # Hetzner
  hcloud server delete bridgr
  hcloud firewall delete bridgr
  hcloud ssh-key delete bridgr
  ```

  Run only the chosen cloud's lines, only after the owner says yes. The no-prompt flags are not permission to
  delete anything. Never delete a shared key entry or firewall. On Hetzner, check for a remaining
  primary IPv4 and remove it in the console if it belongs only to this server. Remove only this installation's
  DNS record too. Deleting the server doesn't cancel the Bridgr subscription. The owner uses the manage link in
  their licence email to cancel it.

## Command references

Checked against the providers' official references on 12 November 2026. Recheck prices and availability when you
install. These are references, not extra steps to run.

- AWS: [Ubuntu images](https://ubuntu.com/aws/docs/aws-how-to/instances/find-ubuntu-images/),
  [instances](https://docs.aws.amazon.com/cli/latest/reference/ec2/run-instances.html),
  [SSH keys](https://docs.aws.amazon.com/cli/latest/reference/ec2/import-key-pair.html),
  [firewall](https://docs.aws.amazon.com/cli/latest/reference/ec2/authorize-security-group-ingress.html).
- Google Cloud: [instances](https://docs.cloud.google.com/sdk/gcloud/reference/compute/instances/create),
  [firewall](https://docs.cloud.google.com/sdk/gcloud/reference/compute/firewall-rules/create),
  [SSH access](https://docs.cloud.google.com/compute/docs/instances/access-overview).
- DigitalOcean: [servers](https://docs.digitalocean.com/reference/doctl/reference/compute/droplet/create/),
  [SSH keys](https://docs.digitalocean.com/reference/doctl/reference/compute/ssh-key/import/),
  [firewall](https://docs.digitalocean.com/reference/doctl/reference/compute/firewall/create/).
- Hetzner: [servers](https://github.com/hetznercloud/cli/blob/main/docs/reference/manual/hcloud_server_create.md),
  [SSH keys](https://github.com/hetznercloud/cli/blob/main/docs/reference/manual/hcloud_ssh-key_create.md),
  [firewall](https://github.com/hetznercloud/cli/blob/main/docs/reference/manual/hcloud_firewall_add-rule.md).
