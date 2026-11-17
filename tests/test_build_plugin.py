"""Regression cases for the installable plugin bundles."""

import hashlib
from pathlib import Path
import stat
import subprocess
import sys
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
NAME = "motion-design-agent-skills"


def build(out):
    subprocess.run([sys.executable, str(ROOT / "scripts/build-plugin.py"), "--out", str(out)],
                   check=True, capture_output=True, text=True)


class BuildPluginTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="motion-plugin-build-")
        self.addCleanup(self.temporary.cleanup)
        self.out = Path(self.temporary.name)
        build(self.out)
        self.skills = sorted(p.name for p in (ROOT / "skills").iterdir() if (p / "SKILL.md").is_file())

    def test_claude_ai_bundle_is_a_loadable_plugin(self):
        with zipfile.ZipFile(self.out / f"{NAME}.zip") as z:
            names = set(z.namelist())
        self.assertIn(".claude-plugin/plugin.json", names)
        self.assertIn("README.md", names)
        for skill in self.skills:
            self.assertIn(f"skills/{skill}/SKILL.md", names)
        # claude.ai and Cowork refuse a plugin with a top-level bin/ directory.
        self.assertFalse(any(n.startswith("bin/") for n in names))
        self.assertFalse(any(n.startswith(("dist/", ".git/", "tests/")) for n in names))

    def test_universal_bundle_carries_every_manifest_and_installer(self):
        with zipfile.ZipFile(self.out / f"{NAME}-universal.zip") as z:
            names = set(z.namelist())
            installer = z.getinfo(f"{NAME}/install.sh")
        for manifest in (".claude-plugin/plugin.json", ".claude-plugin/marketplace.json", "plugin.json",
                         ".antigravity-plugin/plugin.json", ".agents/plugins/marketplace.json",
                         "rules/motion-design-routing.md", "memory/motion-design-routing.md"):
            self.assertIn(f"{NAME}/{manifest}", names)
        self.assertTrue(stat.S_IMODE(installer.external_attr >> 16) & 0o111)

    def test_builds_are_deterministic(self):
        second = self.out / "again"
        build(second)
        for name in (f"{NAME}.zip", f"{NAME}-universal.zip"):
            first = hashlib.sha256((self.out / name).read_bytes()).hexdigest()
            self.assertEqual(first, hashlib.sha256((second / name).read_bytes()).hexdigest(), name)


if __name__ == "__main__":
    unittest.main()
