"""Offline tests: a fake ~/.claude in a temp folder, the script run as the hooks run it."""

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "compartilhar.py"


def memory(name, desc, body="Body."):
    return f"---\nname: {name}\ndescription: {desc}\nmetadata:\n  type: feedback\n---\n\n{body}\n"


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name) / ".claude"
        self.store = self.root / "memorias-compartilhadas"
        self.store.mkdir(parents=True)
        self.groups({"dev": ["-a", "-b", "/home/me/Dev/*"], "outro": ["-c"]})
        for slug in ("-a", "-b", "-c"):
            (self.root / "projects" / slug / "memory").mkdir(parents=True)
        self.put("-a", "regra.md", memory("regra", "Rule for all dev"))
        self.index("-a", "- [Mine](local.md) — stays\n- [Regra](regra.md) — Rule for all dev\n")
        self.put("-a", "local.md", memory("local", "stays"))

    def tearDown(self):
        self.tmp.cleanup()

    def groups(self, g):
        (self.store / "grupos.json").write_text(json.dumps({"grupos": g}))

    def mem(self, slug):
        return self.root / "projects" / slug / "memory"

    def put(self, slug, name, text):
        (self.mem(slug) / name).write_text(text)

    def index(self, slug, text=None):
        p = self.mem(slug) / "MEMORY.md"
        if text is not None:
            p.write_text(text)
        return p.read_text() if p.exists() else ""

    def run_script(self, *args, stdin=None, ok=True):
        env = dict(os.environ, CLAUDE_CONFIG_DIR=str(self.root))
        r = subprocess.run([sys.executable, str(SCRIPT), *args], input=stdin,
                           capture_output=True, text=True, env=env)
        if ok:
            self.assertEqual(r.returncode, 0, r.stderr)
        return r

    def hook(self, data):
        out = self.run_script("hook", stdin=json.dumps(data)).stdout
        return json.loads(out)["hookSpecificOutput"]["additionalContext"] if out.strip() else None

    def share(self):
        self.run_script("compartilhar", str(self.mem("-a") / "regra.md"), "dev")


class Share(Base):
    def test_moves_links_and_indexes_members_only(self):
        self.share()
        self.assertTrue((self.store / "dev" / "regra.md").is_file())
        for slug in ("-a", "-b"):
            link = self.mem(slug) / "regra.md"
            self.assertTrue(link.is_symlink())
            self.assertEqual(os.readlink(link), "../../../memorias-compartilhadas/dev/regra.md")
            self.assertIn("- [regra](regra.md) — Rule for all dev _(grupo dev)_", self.index(slug))
        self.assertFalse((self.mem("-c") / "regra.md").exists())
        # Claude's own line for it is gone from the free part; other lines stay.
        a = self.index("-a")
        self.assertNotIn("[Regra](regra.md)", a)
        self.assertTrue(a.startswith("- [Mine](local.md) — stays\n"))

    def test_refuses_project_outside_group(self):
        self.put("-c", "x.md", memory("x", "d"))
        r = self.run_script("compartilhar", str(self.mem("-c") / "x.md"), "dev", ok=False)
        self.assertNotEqual(r.returncode, 0)
        self.assertTrue((self.mem("-c") / "x.md").is_file())

    def test_refuses_name_taken_in_overlapping_group(self):
        self.groups({"dev": ["-a", "-b"], "todos": ["*"]})
        (self.store / "todos").mkdir()
        (self.store / "todos" / "regra.md").write_text(memory("regra", "other"))
        r = self.run_script("compartilhar", str(self.mem("-a") / "regra.md"), "dev", ok=False)
        self.assertIn("já existe todos/regra.md", r.stderr)
        self.assertTrue((self.mem("-a") / "regra.md").is_file())

    def test_different_local_file_is_a_conflict_not_overwritten(self):
        self.put("-b", "regra.md", memory("regra", "b's own"))
        r = self.run_script("compartilhar", str(self.mem("-a") / "regra.md"), "dev")
        self.assertIn("conflito: -b/regra.md", r.stdout)
        self.assertIn("b's own", (self.mem("-b") / "regra.md").read_text())
        self.assertFalse((self.mem("-b") / "regra.md").is_symlink())


class Sync(Base):
    def test_edit_of_shared_copy_refreshes_every_index(self):
        self.share()
        shared = self.store / "dev" / "regra.md"
        shared.write_text(memory("regra", "New description"))
        self.assertIsNone(self.hook({"hook_event_name": "PostToolUse", "tool_name": "Edit",
                                     "tool_input": {"file_path": str(shared)}}))
        for slug in ("-a", "-b"):
            self.assertIn("— New description _(grupo dev)_", self.index(slug))
            self.assertNotIn("Rule for all dev", self.index(slug))

    def test_plain_copy_with_same_content_becomes_link_again(self):
        # e.g. `sed -i` replaced the symlink with a regular file
        self.share()
        link = self.mem("-b") / "regra.md"
        content = link.read_text()
        link.unlink()
        link.write_text(content)
        self.run_script("sincronizar")
        self.assertTrue(link.is_symlink())

    def test_rewritten_index_gets_block_back(self):
        self.share()
        self.index("-b", "- [Other](other.md) — x\n")
        self.hook({"hook_event_name": "PostToolUse", "tool_name": "Write",
                   "tool_input": {"file_path": str(self.mem("-b") / "MEMORY.md")},
                   "tool_response": {"type": "update"}})
        b = self.index("-b")
        self.assertTrue(b.startswith("- [Other](other.md) — x\n\n<!-- compartilhar-memorias:inicio"))
        self.assertIn("(regra.md)", b)

    def test_leaving_group_removes_link_and_block(self):
        self.share()
        self.groups({"dev": ["-a"]})
        self.run_script("sincronizar")
        self.assertFalse((self.mem("-b") / "regra.md").exists())
        self.assertEqual(self.index("-b"), "")
        self.assertTrue((self.mem("-a") / "regra.md").is_symlink())

    def test_status_lists_pending_without_changing(self):
        self.share()
        (self.mem("-b") / "regra.md").unlink()
        out = self.run_script("status").stdout
        self.assertIn("-b: falta regra.md", out)
        self.assertIn("aviso: os hooks não estão", out)
        self.assertFalse((self.mem("-b") / "regra.md").exists())


class Hooks(Base):
    def test_session_start_links_new_project_matched_by_path(self):
        self.share()
        slug = "-home-me-Dev-novo"
        (self.root / "projects" / slug).mkdir()
        ctx = self.hook({"hook_event_name": "SessionStart",
                         "transcript_path": str(self.root / "projects" / slug / "s.jsonl")})
        self.assertIn("(regra.md)", ctx)
        self.assertTrue((self.mem(slug) / "regra.md").is_symlink())
        self.assertIn("(regra.md)", self.index(slug))
        # second start: nothing new to say
        self.assertIsNone(self.hook({"hook_event_name": "SessionStart",
                                     "transcript_path": str(self.root / "projects" / slug / "s.jsonl")}))

    def test_session_start_outside_groups_is_silent_and_creates_nothing(self):
        slug = "-solto"
        (self.root / "projects" / slug).mkdir()
        self.assertIsNone(self.hook({"hook_event_name": "SessionStart",
                                     "transcript_path": str(self.root / "projects" / slug / "s.jsonl")}))
        self.assertFalse(self.mem(slug).exists())

    def nudge(self, slug, kind="create", tool="Write"):
        return self.hook({"hook_event_name": "PostToolUse", "tool_name": tool,
                          "tool_input": {"file_path": str(self.mem(slug) / "nova.md")},
                          "tool_response": {"type": kind}})

    def test_new_memory_in_member_gets_one_nudge(self):
        self.put("-b", "nova.md", memory("nova", "d"))
        self.assertIn("New memory `nova.md`", self.nudge("-b"))
        self.assertIn("dev", self.nudge("-b"))
        self.assertIsNone(self.nudge("-b", kind="update"))
        self.assertIsNone(self.nudge("-b", kind=None, tool="Edit"))

    def test_new_memory_outside_groups_is_silent(self):
        (self.root / "projects" / "-solto" / "memory").mkdir(parents=True)
        self.put("-solto", "nova.md", memory("nova", "d"))
        self.assertIsNone(self.nudge("-solto"))

    def test_other_files_are_ignored(self):
        self.assertIsNone(self.hook({"hook_event_name": "PostToolUse", "tool_name": "Write",
                                     "tool_input": {"file_path": "/x/src/main.rs"},
                                     "tool_response": {"type": "create"}}))


class Unshare(Base):
    def test_keep_plain_copy_in_one_project(self):
        self.share()
        self.run_script("descompartilhar", "dev/regra.md", "--manter", "-a")
        a = self.mem("-a") / "regra.md"
        self.assertTrue(a.is_file() and not a.is_symlink())
        self.assertFalse((self.mem("-b") / "regra.md").exists())
        self.assertFalse((self.store / "dev" / "regra.md").exists())
        self.assertEqual(self.index("-a"), "- [Mine](local.md) — stays\n- [regra](regra.md) — Rule for all dev\n")
        self.assertEqual(self.index("-b"), "")


if __name__ == "__main__":
    unittest.main()
