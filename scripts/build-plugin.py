#!/usr/bin/env python3
"""Build the installable plugin bundles into dist/.

  motion-design-agent-skills.zip           Claude.ai / Cowork upload (Customize > Plugins > Upload)
  motion-design-agent-skills.plugin        same bytes, for Cowork's .plugin preview
  motion-design-agent-skills-universal.zip Claude Code, Codex, Antigravity and Hermes (offline install)

Archives are deterministic: sorted members, fixed timestamps, explicit permissions.
"""

import argparse
import hashlib
import json
from pathlib import Path
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
NAME = "motion-design-agent-skills"
FIXED_TIME = (2026, 1, 1, 0, 0, 0)

# Claude.ai/Cowork: the Claude manifest, skills, hooks (ignored on web chat), icon and notices.
CLAUDE_AI = [
    ".claude-plugin/plugin.json",
    "skills",
    "hooks",
    "assets/icon.png",
    "LICENSE",
    "THIRD_PARTY_NOTICES.md",
    "docs/plugin-guide.pt-BR.md",
]
# Universal: every manifest plus installer, memory templates and guides.
UNIVERSAL = CLAUDE_AI + [
    ".claude-plugin/marketplace.json",
    "plugin.json",
    ".antigravity-plugin/plugin.json",
    ".agents/plugins/marketplace.json",
    "rules",
    "memory",
    "install.sh",
    "PLUGIN.md",
    "skills-lock.json",
    "vendor/vendor-lock.json",
]
EXECUTABLE = {"install.sh"}


def collect(entries):
    files = []
    for entry in entries:
        path = ROOT / entry
        if path.is_dir():
            files.extend(p for p in sorted(path.rglob("*")) if p.is_file())
        elif path.is_file():
            files.append(path)
        else:
            raise SystemExit(f"missing bundle input: {entry}")
    for p in files:
        if p.is_symlink():
            raise SystemExit(f"symlink cannot be bundled: {p.relative_to(ROOT)}")
    return sorted(set(files), key=lambda p: p.relative_to(ROOT).as_posix())


def write_zip(target, files, prefix="", readme=None):
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        members = [(p.relative_to(ROOT).as_posix(), p.read_bytes()) for p in files]
        if readme:
            members.append(("README.md", readme.read_bytes()))
        for rel, data in sorted(members):
            info = zipfile.ZipInfo(prefix + rel, FIXED_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            mode = 0o755 if rel in EXECUTABLE else 0o644
            info.external_attr = (0o100000 | mode) << 16
            z.writestr(info, data)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--out", type=Path, default=ROOT / "dist")
    args = parser.parse_args()
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=True)

    manifest = json.loads((ROOT / ".claude-plugin/plugin.json").read_text(encoding="utf-8"))
    if manifest.get("name") != NAME:
        raise SystemExit(f"plugin.json name is {manifest.get('name')!r}, expected {NAME!r}")

    claude = out / f"{NAME}.zip"
    write_zip(claude, collect(CLAUDE_AI), readme=ROOT / "PLUGIN.md")
    (out / f"{NAME}.plugin").write_bytes(claude.read_bytes())
    universal = out / f"{NAME}-universal.zip"
    write_zip(universal, collect(UNIVERSAL), prefix=f"{NAME}/")

    sums = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in (claude, out / f"{NAME}.plugin", universal)}
    (out / "PLUGIN-SHA256SUMS").write_text("".join(f"{v}  {k}\n" for k, v in sums.items()), encoding="utf-8")
    for k, v in sums.items():
        with zipfile.ZipFile(out / k) as z:
            print(f"{k}: {len(z.namelist())} files, {(out / k).stat().st_size // 1024} KiB, sha256 {v[:12]}")
    print(f"version {manifest.get('version')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
