"""Integration tests for the local student application."""
import json
from pathlib import Path
import tempfile
import threading
import unittest
from urllib import request, error
from app import gap_report, make_server


class ProjectTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.server = make_server("127.0.0.1", 0, Path(self.temp.name) / "test.sqlite")
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.base = f"http://127.0.0.1:{self.server.server_address[1]}"
        self.token = ""

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join()
        self.temp.cleanup()

    def call(self, endpoint, data=None, token=None):
        headers = {}
        if data is not None:
            headers["Content-Type"] = "application/json"
        bearer = self.token if token is None else token
        if bearer:
            headers["Authorization"] = "Bearer " + bearer
        body = json.dumps(data).encode() if data is not None else None
        req = request.Request(self.base + endpoint, body, headers)
        try:
            with request.urlopen(req, timeout=5) as res:
                return res.status, json.load(res)
        except error.HTTPError as exc:
            return exc.code, json.load(exc)

    def signup(self):
        status, _ = self.call("/api/register", {"name": "Test Student", "email": "test@example.com", "password": "longpass123"})
        self.assertEqual(status, 201)
        status, reply = self.call("/api/login", {"email": "test@example.com", "password": "longpass123"})
        self.assertEqual(status, 200)
        self.token = reply["token"]

    def test_public_endpoints(self):
        self.assertEqual(self.call("/health")[1]["status"], "ok")
        self.assertIn("Data Analyst", self.call("/api/catalog")[1]["career_paths"])
        self.assertEqual(self.call("/api/dashboard")[0], 401)

    def test_auth_duplicate_and_invalid_login(self):
        self.signup()
        self.assertEqual(self.call("/api/register", {"name": "A", "email": "test@example.com", "password": "password123"})[0], 409)
        self.assertEqual(self.call("/api/login", {"email": "test@example.com", "password": "wrongpass"})[0], 401)
        self.assertEqual(self.call("/api/dashboard", token="bad")[0], 401)

    def test_skills_goal_recommendations_and_progress(self):
        self.signup()
        self.assertEqual(self.call("/api/profile", {"name": "Test Student", "goal": "Data Analyst", "interests": "data"})[0], 200)
        self.assertEqual(self.call("/api/skills", {"skills": ["Python", "SQL"]})[0], 200)
        status, result = self.call("/api/dashboard")
        self.assertEqual(status, 200)
        self.assertEqual(result["analysis"]["readiness_percent"], 40)
        self.assertEqual(result["analysis"]["missing_skills"], ["Excel", "Statistics", "Data Visualization"])
        self.assertEqual(self.call("/api/progress", {"skill": "Excel", "completed": True})[0], 200)
        self.assertIn("Excel", self.call("/api/dashboard")[1]["completed"])
        self.assertEqual(self.call("/api/logout", {})[0], 200)
        self.assertEqual(self.call("/api/dashboard")[0], 401)

    def test_validation(self):
        self.signup()
        self.assertEqual(self.call("/api/profile", {"name":"A","goal":"Nonexistent","interests":""})[0], 400)
        self.assertEqual(self.call("/api/skills", {"skills":["Not a real skill"]})[0], 400)
        self.assertEqual(self.call("/api/progress", {"skill":"Python","completed":"yes"})[0], 400)

    def test_gap_report(self):
        report = gap_report("Web Developer", ["HTML", "Git"])
        self.assertEqual(report["readiness_percent"], 40)
        self.assertEqual(len(report["recommendations"]), 3)


if __name__ == "__main__":
    unittest.main()
