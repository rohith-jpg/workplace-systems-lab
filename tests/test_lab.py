import csv
import json
import tempfile
import unittest
from datetime import date
from pathlib import Path
import lab


class LabTests(unittest.TestCase):
    def test_known_risks_and_totals(self):
        result = lab.analyze(lab.ROOT / 'data', date(2026, 10, 14))
        self.assertEqual(len(result['findings']), 13)
        self.assertEqual(result['potential_monthly_savings_usd'], 39.0)
        self.assertEqual(result['findings'][0]['severity'], 'critical')
        self.assertTrue(any(f['subject'] == 'LAP-003' and f['control'] == 'Asset lifecycle'
                            for f in result['findings']))

    def test_exports_escape_untrusted_content(self):
        result = lab.analyze(lab.ROOT / 'data', date(2026, 10, 14))
        result['findings'][0]['subject'] = '=1+1<script>'
        (lab.ROOT / 'work').mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=lab.ROOT / 'work') as tmp:
            folder = Path(tmp)
            lab.export(result, folder)
            self.assertIn('&lt;script&gt;', (folder / 'report.html').read_text())
            with (folder / 'findings.csv').open(newline='') as handle:
                first = next(csv.DictReader(handle))
            self.assertTrue(first['subject'].startswith("'="))
            manifest = json.loads((folder / 'manifest.json').read_text())
            for name, digest in manifest['sha256'].items():
                self.assertEqual(lab.hashlib.sha256((folder / name).read_bytes()).hexdigest(), digest)

    def test_closed_and_same_day_tickets_not_overdue(self):
        result = lab.analyze(lab.ROOT / 'data', date(2026, 10, 13))
        self.assertFalse(any(f['control'] == 'Ticket queue' for f in result['findings']))

    def test_no_findings_for_clean_fixtures(self):
        (lab.ROOT / 'work').mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=lab.ROOT / 'work') as tmp:
            folder = Path(tmp)
            for name in ['users', 'assets', 'licenses', 'tickets']:
                rows = lab.load(lab.ROOT / 'data', name)
                if name == 'users':
                    rows = [rows[0]]
                elif name == 'assets':
                    rows = [rows[0]]
                elif name == 'licenses':
                    rows = [rows[0]]
                else:
                    rows = [rows[-1]]
                with (folder / (name + '.csv')).open('w', newline='') as handle:
                    writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
                    writer.writeheader()
                    writer.writerows(rows)
            self.assertEqual(lab.analyze(folder, date(2026, 10, 14))['findings'], [])
