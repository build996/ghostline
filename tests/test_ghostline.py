import tempfile
import unittest
from pathlib import Path

from ghostline import collect, redact, validate


class GhostlineTests(unittest.TestCase):
    def test_collect_deleted_source(self):
        # Build a genuine two-commit Git repository, not a mocked Git response.
        import subprocess

        with tempfile.TemporaryDirectory() as root:
            repo = Path(root) / "repo"
            repo.mkdir()
            def git(*args):
                subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True)
            git("init", "-q")
            git("config", "user.name", "Test")
            git("config", "user.email", "test@example.invalid")
            (repo / "gone.py").write_text("def hello():\n    return 42\n")
            git("add", "gone.py")
            git("commit", "-qm", "Add helper")
            (repo / "gone.py").unlink()
            git("add", "-A")
            git("commit", "-qm", "Remove helper")
            bundle = collect(repo, "gone.py")
            self.assertIn("return 42", bundle["evidence"]["S1"])
            self.assertIn("Remove helper", bundle["evidence"]["C1"])

    def test_reject_invented_citation(self):
        with self.assertRaises(ValueError):
            validate({"voice": "Hello", "citations": ["S1", "S999"], "uncertainty": "Unknown"}, {"S1": "real"})

    def test_redact_token(self):
        self.assertNotIn("topsecret", redact("api_key=topsecret"))


if __name__ == "__main__":
    unittest.main()
