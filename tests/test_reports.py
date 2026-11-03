
import unittest
import json
import csv
import os
import tempfile
from unittest.mock import patch

from output.reports import save_json, save_csv


class TestReportGeneration(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()

        self.results = {
            "target_ip": "127.0.0.1",
            "hostname": "localhost",
            "start_port": 1,
            "end_port": 1000,
            "open_ports": [
                {
                    "port": 22,
                    "status": "Open",
                    "registered_service": "ssh",
                    "detected_service": "SSH",
                    "banner": "SSH-2.0-Test"
                }
            ],
            "total_scanned": 1000,
            "duration": 1.25
        }

    def tearDown(self):
        self.temp_dir.cleanup()

    @patch("output.reports.REPORTS_DIR")
    def test_json_report(self, mock_dir):
        # Use a temporary directory.
        mock_dir = self.temp_dir.name

        with patch("output.reports.REPORTS_DIR", mock_dir):
            filepath = save_json(self.results)

        self.assertTrue(os.path.exists(filepath))

        with open(filepath, "r", encoding="utf-8") as file:
            data = json.load(file)

        self.assertEqual(data["target_ip"], "127.0.0.1")
        self.assertEqual(data["open_ports"][0]["port"], 22)

    @patch("output.reports.REPORTS_DIR")
    def test_csv_report(self, mock_dir):
        mock_dir = self.temp_dir.name

        with patch("output.reports.REPORTS_DIR", mock_dir):
            filepath = save_csv(self.results)

        self.assertTrue(os.path.exists(filepath))

        with open(filepath, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            rows = list(reader)

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["port"], "22")
        self.assertEqual(rows[0]["detected_service"], "SSH")

    @patch("output.reports.REPORTS_DIR")
    def test_empty_csv_report(self, mock_dir):
        empty_results = self.results.copy()
        empty_results["open_ports"] = []

        mock_dir = self.temp_dir.name

        with patch("output.reports.REPORTS_DIR", mock_dir):
            filepath = save_csv(empty_results)

        self.assertTrue(os.path.exists(filepath))

        with open(filepath, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            rows = list(reader)

        self.assertEqual(rows, [])


if __name__ == "__main__":
    unittest.main()
