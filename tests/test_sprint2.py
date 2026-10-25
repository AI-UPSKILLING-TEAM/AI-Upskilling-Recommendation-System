"""Sprint 2 API integration and security regression tests (stdlib only)."""
import json
from pathlib import Path
import sqlite3
import tempfile
import threading
import unittest
from urllib import request, error

from app import make_server, promote_admin
from recommendations import CATALOG, rank_learning


class SprintTwoTests(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.db = Path(self.folder.name) / "test.sqlite"
        self.server = make_server("127.0.0.1", 0, self.db)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.host = "http://127.0.0.1:%d" % self.server.server_address[1]
        self.token = None

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join()
        self.folder.cleanup()

    def call(self, route, body=None, token="CURRENT"):
        headers = {}
        if body is not None:
            headers["Content-Type"] = "application/json"
        bearer = self.token if token == "CURRENT" else token
        if bearer:
            headers["Authorization"] = "Bearer " + bearer
        req = request.Request(self.host + route, json.dumps(body).encode() if body is not None else None, headers)
        try:
            with request.urlopen(req, timeout=5) as response:
                return response.status, json.load(response)
        except error.HTTPError as response:
            return response.code, json.load(response)

    def student(self, email="student@example.com"):
        self.assertEqual(self.call("/api/register", {"name":"Student","email":email,"password":"passphrase!123"})[0],201)
        code,data = self.call("/api/login", {"email":email,"password":"passphrase!123"})
        self.assertEqual(code,200)
        self.token = data["token"]
        return self.token

    def test_catalog_uses_only_https_resources(self):
        code,data = self.call("/api/resources")
        self.assertEqual(code, 200)
        self.assertGreaterEqual(len(data["curated"]), 10)
        self.assertTrue(all(r["url"].startswith("https://") for r in data["curated"]))
        self.assertEqual(len(CATALOG), len(data["curated"]))

    def test_personalized_recommendation_has_real_resource_metadata(self):
        for interest in ("web frontend", "machine learning data"):
            rows = rank_learning(["HTML","SQL","Python"],"Data Analyst",interest)
            self.assertEqual({r["skill"] for r in rows},{"HTML","SQL","Python"})
            self.assertTrue(all(r["url"].startswith("https://") for r in rows))
            self.assertTrue(all(0 <= r["relevance_score"] <= 1.00001 for r in rows))
            self.assertEqual(rows,rank_learning(["HTML","SQL","Python"],"Data Analyst",interest))

    def test_notification_opt_in_and_isolation(self):
        original = self.student()
        self.assertEqual(self.call("/api/notifications")[1]["items"], [])
        self.assertEqual(self.call("/api/notifications/preferences", {"enabled":"yes"})[0],400)
        self.assertEqual(self.call("/api/notifications/preferences", {"enabled":True})[0],200)
        self.assertEqual(self.call("/api/progress", {"skill":"Python","completed":True})[0],200)
        self.assertEqual(self.call("/api/progress", {"skill":"Python","completed":True})[0],200)
        code,data = self.call("/api/notifications")
        self.assertTrue(data["enabled"])
        self.assertEqual(len(data["items"]), 1)
        event_id = data["items"][0]["id"]
        self.assertEqual(self.call("/api/notifications/read", {"id":event_id})[0],200)
        self.assertIsNotNone(self.call("/api/notifications")[1]["items"][0]["read_at"])
        self.student("second@example.com")
        self.assertEqual(self.call("/api/notifications")[1]["items"], [])
        self.assertEqual(self.call("/api/notifications/read", {"id":event_id})[0],200)
        self.token = original
        self.assertEqual(len(self.call("/api/notifications")[1]["items"]), 1)
        self.assertEqual(self.call("/api/notifications/preferences", {"enabled":False})[0],200)
        self.assertEqual(self.call("/api/progress", {"skill":"SQL","completed":True})[0],200)
        self.assertEqual(len(self.call("/api/notifications")[1]["items"]), 1)

    def test_admin_access_and_audit(self):
        self.student()
        self.assertEqual(self.call("/api/admin/users")[0],403)
        self.assertEqual(self.call("/api/admin/audit")[0],403)
        resource = {"skill":"Python","title":"Python exercise","url":"https://docs.python.org/3/tutorial/","description":"Practice"}
        self.assertEqual(self.call("/api/admin/resources",resource)[0],403)
        self.assertTrue(promote_admin("student@example.com",self.db))
        self.assertFalse(promote_admin("missing@example.com",self.db))
        self.assertEqual(self.call("/api/admin/users")[0],200)
        self.assertEqual(self.call("/api/admin/resources",{**resource,"url":"javascript:alert(1)"})[0],400)
        self.assertEqual(self.call("/api/admin/resources",{**resource,"url":"https://[broken"})[0],400)
        self.assertEqual(self.call("/api/admin/resources",{**resource,"url":"https://localhost/private"})[0],400)
        self.assertEqual(self.call("/api/admin/resources",resource)[0],200)
        self.assertEqual(self.call("/api/admin/audit")[1]["audit"][0]["action"],"add-resource")
        self.assertEqual(self.call("/api/resources")[1]["custom"][0]["title"],"Python exercise")
        self.assertEqual(self.call("/api/profile",{"name":"Student","interests":"python","goal":"Data Analyst"})[0],200)
        data = self.call("/api/dashboard")[1]
        python_row = next(r for r in data["analysis"]["recommendations"] if r["skill"] == "Python")
        self.assertEqual(python_row["resource"],"Python exercise")

    def test_courses_projects_and_certifications_are_private(self):
        first = self.student()
        items = [
            ("course","Python Fundamentals","Python"),
            ("project","SQL mini project","SQL"),
            ("certification","Excel Essentials","Excel"),
        ]
        for kind,title,skill in items:
            self.assertEqual(self.call("/api/portfolio/add",
                {"kind":kind,"title":title,"skill":skill})[0],200)
        ids = [r["id"] for r in self.call("/api/portfolio")[1]["items"]]
        self.assertEqual(len(ids),3)
        self.assertEqual(len(self.call("/api/dashboard")[1]["portfolio"]),3)
        self.assertEqual(self.call("/api/portfolio/add",
            {"kind":"invalid","title":"bad","skill":"Python"})[0],400)
        self.student("other@example.com")
        self.assertEqual(self.call("/api/portfolio")[1]["items"],[])
        self.assertEqual(self.call("/api/portfolio/delete",{"id":ids[0]})[0],200)
        self.token=first
        self.assertEqual(len(self.call("/api/portfolio")[1]["items"]),3)
        self.assertEqual(self.call("/api/portfolio/delete",{"id":ids[0]})[0],200)
        self.assertEqual(len(self.call("/api/portfolio")[1]["items"]),2)

    def test_admin_can_edit_career_requirements(self):
        self.student()
        new_role = {"role":"Data Analyst","skills":["Python","SQL"]}
        self.assertEqual(self.call("/api/admin/roles",new_role)[0],403)
        self.assertTrue(promote_admin("student@example.com",self.db))
        self.assertEqual(self.call("/api/admin/roles",{"role":"", "skills":["SQL"]})[0],400)
        self.assertEqual(self.call("/api/admin/roles",new_role)[0],200)
        self.assertEqual(self.call("/api/catalog")[1]["career_paths"]["Data Analyst"],["Python","SQL"])
        self.assertEqual(self.call("/api/profile",
            {"name":"Student","interests":"","goal":"Data Analyst"})[0],200)
        self.assertEqual(self.call("/api/dashboard")[1]["analysis"]["required_skills"],["Python","SQL"])
        self.assertEqual(self.call("/api/admin/audit")[1]["audit"][0]["action"],"edit-role-requirements")

    def test_unauthorized_write_and_validation(self):
        self.student()
        self.assertEqual(self.call("/api/notifications",token=None)[0],401)
        self.assertEqual(self.call("/api/notifications/preferences",{"enabled":True},token=None)[0],401)
        self.assertEqual(self.call("/api/notifications/read",{"id":True})[0],400)
        self.assertEqual(self.call("/api/notifications/read",{"id":-1})[0],400)


if __name__ == "__main__":
    unittest.main()
