#!/usr/bin/env python3
"""Vendor pinned, permissively licensed third-party skills into skills/.

Usage:
  python3 scripts/sync-vendor-skills.py           # fetch pinned commits, copy, record hashes
  python3 scripts/sync-vendor-skills.py --check   # offline: verify vendored skills match the lock

Only sources listed in vendor/vendor-lock.json are fetched. The script never runs
code from the fetched repositories; it copies files and records SHA-256 digests.
"""

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
LOCK = ROOT / "vendor" / "vendor-lock.json"
DEST = ROOT / "skills"
ALLOWED_LICENSES = {"MIT", "Apache-2.0"}


def digest_tree(folder):
    return {
        f"{folder.name}/{p.relative_to(folder).as_posix()}": hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sorted(folder.rglob("*"))
        if p.is_file()
    }


def check(lock):
    errors = []
    expected = lock.get("files", {})
    names = {s for src in lock["sources"] for s in src["skills"]}
    found = {p.name for p in DEST.iterdir() if p.is_dir() and p.name in names}
    if found != names:
        errors.append(f"vendored inventory differs: missing={sorted(names - found)}")
    actual = {}
    for name in sorted(found & names):
        folder = DEST / name
        if any(p.is_symlink() for p in folder.rglob("*")):
            errors.append(f"{name}: symlinks are not allowed in vendored skills")
        if not (folder / "SKILL.md").is_file():
            errors.append(f"{name}: missing SKILL.md")
        if not (folder / "LICENSE").is_file():
            errors.append(f"{name}: missing upstream LICENSE")
        actual.update(digest_tree(folder))
    if actual != expected:
        changed = sorted(k for k in set(actual) | set(expected) if actual.get(k) != expected.get(k))
        errors.append(f"vendored files drift from vendor-lock.json: {changed[:10]}")
    return errors


def sync(lock):
    files = {}
    for name in {s for src in lock["sources"] for s in src["skills"]}:
        if (DEST / name).exists():
            shutil.rmtree(DEST / name)
    for src in lock["sources"]:
        if src["license"] not in ALLOWED_LICENSES:
            raise SystemExit(f"{src['repo']}: license {src['license']} is not allowed for vendoring")
        with tempfile.TemporaryDirectory(prefix="vendor-skill-") as tmp:
            repo = Path(tmp) / "repo"
            url = f"https://github.com/{src['repo']}.git"
            subprocess.run(["git", "init", "-q", str(repo)], check=True)
            subprocess.run(["git", "-C", str(repo), "fetch", "-q", "--depth", "1", url, src["commit"]], check=True)
            subprocess.run(["git", "-C", str(repo), "-c", "advice.detachedHead=false", "checkout", "-q", "FETCH_HEAD"], check=True)
            head = subprocess.run(["git", "-C", str(repo), "rev-parse", "HEAD"], check=True, capture_output=True, text=True).stdout.strip()
            if head != src["commit"]:
                raise SystemExit(f"{src['repo']}: fetched {head}, expected {src['commit']}")
            license_file = repo / src["licenseFile"]
            if not license_file.is_file():
                raise SystemExit(f"{src['repo']}: missing {src['licenseFile']}")
            for name in src["skills"]:
                source = repo / src["skillsDir"] / name
                if not (source / "SKILL.md").is_file() or source.is_symlink():
                    raise SystemExit(f"{src['repo']}: {name}/SKILL.md not found")
                shutil.copytree(source, DEST / name, symlinks=False, ignore=shutil.ignore_patterns(".git", ".DS_Store"))
                shutil.copyfile(license_file, DEST / name / "LICENSE")
                files.update(digest_tree(DEST / name))
    lock["files"] = dict(sorted(files.items()))
    LOCK.write_text(json.dumps(lock, indent=2) + "\n", encoding="utf-8")
    print(f"Vendored {len({k.split('/')[0] for k in files})} skills, {len(files)} files")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true", help="verify only, no network")
    args = parser.parse_args()
    lock = json.loads(LOCK.read_text(encoding="utf-8"))
    if args.check:
        errors = check(lock)
        print("\n".join(errors) if errors else "OK: vendored skills match vendor/vendor-lock.json")
        return 1 if errors else 0
    sync(lock)
    errors = check(json.loads(LOCK.read_text(encoding="utf-8")))
    print("\n".join(errors) if errors else "OK: vendored skills match vendor/vendor-lock.json")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
