"""Repeatable non-functional security and persistence smoke tests."""
import hashlib
import json
from pathlib import Path
import sqlite3
import tempfile
import threading
import unittest
from urllib import request, error

from app import make_server


class NonFunctionalTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.db = Path(self.temp.name) / "app.sqlite"
        self.server = make_server("127.0.0.1",0,self.db)
        self.thread = threading.Thread(target=self.server.serve_forever,daemon=True)
        self.thread.start()
        self.base = "http://127.0.0.1:%d" % self.server.server_address[1]

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join()
        self.temp.cleanup()

    def call(self, path, body=None, token=None):
        headers = {}
        if token:
            headers["Authorization"] = "Bearer " + token
        if body is not None:
            headers["Content-Type"]="application/json"
        req=request.Request(self.base+path,json.dumps(body).encode() if body is not None else None,headers)
        try:
            res=request.urlopen(req,timeout=5)
        except error.HTTPError as exception:
            res=exception
        with res:
            return res.status,dict(res.headers),res.read()

    def test_password_is_salted_and_never_stored_in_plaintext(self):
        status,_,_=self.call("/api/register",{"name":"Security Test","email":"test@example.com","password":"securepass2026"})
        self.assertEqual(status,201)
        with sqlite3.connect(self.db) as db:
            row=db.execute("SELECT salt,password_hash FROM users").fetchone()
        self.assertNotEqual(row[1],"securepass2026")
        self.assertEqual(len(row[0]),32)
        self.assertEqual(len(row[1]),64)
        stored=hashlib.pbkdf2_hmac("sha256","securepass2026".encode(),bytes.fromhex(row[0]),300_000).hex()
        self.assertEqual(stored,row[1])

    def test_client_cache_headers_and_static_content_security(self):
        status,headers,_=self.call("/api/catalog")
        self.assertEqual(status,200)
        self.assertEqual(headers.get("Cache-Control"),"no-store")
        self.assertEqual(headers.get("X-Content-Type-Options"),"nosniff")
        status,headers,_=self.call("/")
        self.assertEqual(status,200)
        self.assertIn("script-src 'self'",headers.get("Content-Security-Policy",""))

    def test_expired_session_denied(self):
        self.call("/api/register",{"name":"Student","email":"student@example.com","password":"passphrase123"})
        status,_,body=self.call("/api/login",{"email":"student@example.com","password":"passphrase123"})
        self.assertEqual(status,200)
        token=json.loads(body)["token"]
        self.assertEqual(self.call("/api/dashboard",token=token)[0],200)
        hashed=hashlib.sha256(token.encode()).hexdigest()
        with sqlite3.connect(self.db) as db:
            db.execute("UPDATE sessions SET expires_at=1 WHERE token_hash=?",(hashed,))
            db.commit()
        self.assertEqual(self.call("/api/dashboard",token=token)[0],401)

    def test_request_validation_rejects_unstructured_input(self):
        status,_,_=self.call("/api/register",["not a dictionary"])
        self.assertEqual(status,400)
        status,_,_=self.call("/api/register",{"name":"x","email":"bad","password":"goodpassword"})
        self.assertEqual(status,400)


if __name__=="__main__":
    unittest.main()
