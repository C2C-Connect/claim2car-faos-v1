"""Canonical contract tests only; not capture or hardware validation."""
import json
from pathlib import Path
import unittest

class ShotListContractTests(unittest.TestCase):
    def setUp(self):
        path = Path(__file__).resolve().parents[1] / "contracts" / "shot-list.json"
        self.contract = json.loads(path.read_text(encoding="utf-8"))

    def test_versions_and_shape(self):
        self.assertEqual(set(self.contract), {"schema_version", "shot_list_version", "required_angles"})
        self.assertEqual(self.contract["schema_version"], "0.1")
        self.assertEqual(self.contract["shot_list_version"], "claims2car-12-v1")

    def test_canonical_order_and_uniqueness(self):
        expected = ["vin_ocr", "doc_ocr", "front", "front_left", "driver_side", "rear_left", "rear", "rear_right", "passenger_side", "front_right", "interior_front", "undercarriage_engine"]
        self.assertEqual(self.contract["required_angles"], expected)
        self.assertEqual(len(set(self.contract["required_angles"])), 12)

if __name__ == "__main__":
    unittest.main()
