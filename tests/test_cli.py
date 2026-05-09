from __future__ import annotations

import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from chat2workflow.cli import main


SAMPLE = """********************2024-01-01********************
2024-01-01 09:00:00 system notice
t__;:我要投简历
21会计2郑思语:这个论文怎么写
"""


class CliTest(unittest.TestCase):
    def test_analyze_json_writes_stdout(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = Path(tmpdir) / "sample.txt"
            input_path.write_text(SAMPLE, encoding="utf-8")
            stdout = io.StringIO()

            with redirect_stdout(stdout):
                exit_code = main(["analyze", str(input_path), "--format", "json"])

        payload = json.loads(stdout.getvalue())
        self.assertEqual(exit_code, 0)
        self.assertIn("stats", payload)
        self.assertIn("workflow_cards", payload)

    def test_export_workflows_writes_json_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = Path(tmpdir) / "sample.txt"
            output_path = Path(tmpdir) / "workflows.json"
            input_path.write_text(SAMPLE, encoding="utf-8")

            exit_code = main(
                ["export-workflows", str(input_path), "--out", str(output_path)]
            )

            payload = json.loads(output_path.read_text(encoding="utf-8"))
            output_exists = output_path.exists()

        self.assertEqual(exit_code, 0)
        self.assertTrue(output_exists)
        self.assertGreaterEqual(len(payload["workflow_cards"]), 2)
