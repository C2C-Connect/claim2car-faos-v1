import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import Settings, create_app

class AppTests(unittest.TestCase):
    def test_liveness(self):
        response = TestClient(create_app(Settings("test"))).get("/health/live")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "alive")
    def test_unwired_database_not_ready(self):
        response = TestClient(create_app(Settings("test", "postgresql://unused"))).get("/health/ready")
        self.assertEqual(response.status_code, 503)
    def test_probe_success(self):
        response = TestClient(create_app(Settings("test", "postgresql://unused"), lambda: True)).get("/health/ready")
        self.assertEqual(response.status_code, 200)
    def test_probe_failure(self):
        def broken(): raise RuntimeError("secret must not leak")
        response = TestClient(create_app(Settings("test", "postgresql://unused"), broken)).get("/health/ready")
        self.assertEqual(response.status_code, 503)
        self.assertNotIn("secret", response.text)
    def test_live_and_unknown_environments_blocked(self):
        for environment in ("staging", "production", "unknown"):
            with self.subTest(environment=environment):
                with self.assertRaises(ValueError): create_app(Settings(environment))
    def test_non_postgres_rejected(self):
        with patch.dict("os.environ", {"FAOS_ENV":"test", "DATABASE_URL":"mongodb://unused"}):
            with self.assertRaises(ValueError): create_app()
    def test_direct_settings_also_validated(self):
        with self.assertRaises(ValueError): create_app(Settings("test", "sqlite://unused"))

if __name__ == "__main__": unittest.main()
