#!/usr/bin/env python3
"""Build the Bridgr plugin as an uploadable zip (Claude Desktop: Settings → Customize → Plugins → Add → Upload).

    tools/build_zip.py                                                     the generic zip: asks for the address
    tools/build_zip.py --company "Company Name" --url https://yourcompany.eastridge-analytics.com
                                                                           one company's zip: its name, its address
    tools/build_zip.py --codex --company ... --url ...                     the same for Codex (unzip, then
                                                                           codex plugin marketplace add <folder>)

A company's zip is the same plugin (name `bridgr`, same skills) with three things set: the display name
("Bridgr · Company Name"), the connector address (Claude's .mcp.json and Codex's codex.mcp.json), and the
version label (0.3.0+company-name). It asks nothing on install. Bridgr itself builds the same thing for its own company (bridgr/plugin_zip.py in bridgr-v3); this script is
the reference and the generic release.
"""
from __future__ import annotations

import argparse
import io
import json
import re
import sys
import zipfile
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent.parent
PLUGIN = ROOT / "plugins" / "bridgr"
# Keep icon: Desktop's uploaded plugin needs the path to its bundled artwork. Older Code may warn, but loads it.
LISTING = ("documentationUrl", "supportUrl", "privacyPolicyUrl")


def slug(name: str) -> str:
    name = name.replace("'", "").replace("\u2019", "")   # Company's Bridgr -> companys-bridgr, as Bridgr's own builder
    return re.sub(r"-{2,}", "-", re.sub(r"[^a-z0-9]+", "-", name.lower())).strip("-")[:60]


def company_address(url: str) -> str:
    """https:// and the host only: a trailing slash or /mcp makes the connection fail."""
    parts = urlsplit((url or "").strip())
    if parts.scheme not in ("https", "http") or not parts.hostname:
        raise ValueError(f"not an address: {url!r}")
    if parts.scheme == "http" and parts.hostname not in ("127.0.0.1", "localhost"):
        raise ValueError("https only, except a Bridgr on this computer")
    return f"{parts.scheme}://{parts.netloc}"


def files(company: str = "", url: str = "") -> dict[str, bytes]:
    """Every file of the zip, by path inside it."""
    out = {p.relative_to(PLUGIN).as_posix(): p.read_bytes() for p in sorted(PLUGIN.rglob("*"))
           if p.is_file() and p.name != ".DS_Store"}
    claude = json.loads(out[".claude-plugin/plugin.json"])
    codex = json.loads(out[".codex-plugin/plugin.json"])
    for k in LISTING:
        claude.pop(k, None)
    if company:
        address = company_address(url)
        label = slug(company)
        claude.pop("userConfig", None)
        claude["displayName"] = codex["interface"]["displayName"] = f"Bridgr · {company}"
        claude["version"] = codex["version"] = f"{claude['version']}+{label}"
        server = {"type": "http", "url": f"{address}/mcp"}
        out[".mcp.json"] = (json.dumps({"mcpServers": {"bridgr": server}}, indent=2) + "\n").encode()
        out["codex.mcp.json"] = (json.dumps({"mcpServers": {"bridgr": {"url": f"{address}/mcp"}}}, indent=2) + "\n").encode()
    out[".claude-plugin/plugin.json"] = (json.dumps(claude, indent=2, ensure_ascii=False) + "\n").encode()
    out[".codex-plugin/plugin.json"] = (json.dumps(codex, indent=2, ensure_ascii=False) + "\n").encode()
    return out


MARKETPLACE = "bridgr-company"


def codex_files(company: str, url: str) -> dict[str, bytes]:
    """One company's plugin for Codex, which installs from a folder: the folder holds a marketplace and the plugin.
    Unzip, then codex plugin marketplace add <folder> and codex plugin add bridgr@bridgr-company."""
    top = codex_file_name(company).removesuffix(".zip")
    market = {"name": MARKETPLACE, "interface": {"displayName": f"Bridgr · {company}"},
              "plugins": [{"name": "bridgr", "source": {"source": "local", "path": "./plugins/bridgr"},
                           "policy": {"installation": "AVAILABLE", "authentication": "ON_USE"},
                           "category": "Productivity"}]}
    out = {f"{top}/.agents/plugins/marketplace.json": (json.dumps(market, indent=2, ensure_ascii=False) + "\n").encode()}
    out.update({f"{top}/plugins/bridgr/{k}": v for k, v in files(company, url).items()})
    return out


def codex_file_name(company: str) -> str:
    return f"bridgr-{slug(company)}-codex.zip"


def zip_bytes(company: str = "", url: str = "", codex: bool = False) -> bytes:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        for name, data in (codex_files(company, url) if codex else files(company, url)).items():
            info = zipfile.ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))   # same input, same bytes
            info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(info, data)
    return buf.getvalue()


def file_name(company: str = "") -> str:
    version = json.loads((PLUGIN / ".claude-plugin" / "plugin.json").read_text())["version"]
    return f"bridgr-{slug(company)}.zip" if company else f"bridgr-plugin-{version}.zip"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--company", default="", help="the company's name as people know it")
    ap.add_argument("--url", default="", help="the company's Bridgr address")
    ap.add_argument("--out", type=Path, default=ROOT / "dist")
    ap.add_argument("--codex", action="store_true", help="the Codex zip: a folder with its own marketplace")
    a = ap.parse_args()
    if bool(a.company) != bool(a.url):
        ap.error("--company and --url go together")
    if a.codex and not a.company:
        ap.error("--codex needs --company and --url")
    a.out.mkdir(parents=True, exist_ok=True)
    path = a.out / (codex_file_name(a.company) if a.codex else file_name(a.company))
    path.write_bytes(zip_bytes(a.company, a.url, a.codex))
    print(path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
