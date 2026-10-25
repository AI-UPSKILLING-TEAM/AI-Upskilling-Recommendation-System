"""Dependency-free educational prototype for project 22.

Sprints: authentication, profile, skills, goals, gap analysis and a learning dashboard.
The recommendation ranking is rules-based, not a trained AI model.
"""
import hashlib
import json
import os
from pathlib import Path
import re
import secrets
import sqlite3
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent
DB_PATH = Path(os.getenv("UPSKILL_DB", str(ROOT / "upskill.db")))

CAREER_PATHS = {
    "Data Analyst": ["Python", "SQL", "Excel", "Statistics", "Data Visualization"],
    "Data Scientist": ["Python", "SQL", "Statistics", "Machine Learning", "Data Visualization"],
    "Web Developer": ["HTML", "CSS", "JavaScript", "Git", "APIs"],
    "Backend Developer": ["Python", "SQL", "APIs", "Git", "Testing"],
    "Cloud Engineer": ["Linux", "Networking", "Python", "Cloud Fundamentals", "Git"],
    "Cybersecurity Analyst": ["Networking", "Linux", "Python", "Security Fundamentals", "Git"],
}
ALL_SKILLS = sorted({skill for skills in CAREER_PATHS.values() for skill in skills})


def connect_db(db_path=None):
    connection = sqlite3.connect(str(db_path or DB_PATH), timeout=5)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize(db_path=None):
    with connect_db(db_path) as db:
        db.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                salt TEXT NOT NULL,
                password_hash TEXT NOT NULL,
                interests TEXT NOT NULL DEFAULT '',
                goal TEXT NOT NULL DEFAULT ''
            );
            CREATE TABLE IF NOT EXISTS skills (
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                skill TEXT NOT NULL,
                PRIMARY KEY (user_id, skill)
            );
            CREATE TABLE IF NOT EXISTS progress (
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                skill TEXT NOT NULL,
                completed_at INTEGER NOT NULL,
                PRIMARY KEY (user_id, skill)
            );
            CREATE TABLE IF NOT EXISTS sessions (
                token_hash TEXT PRIMARY KEY,
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                expires_at INTEGER NOT NULL
            );
        """)


def password_digest(password, salt):
    return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), bytes.fromhex(salt), 300_000).hex()


def gap_report(goal, existing):
    required = CAREER_PATHS.get(goal, [])
    present = set(existing)
    missing = [skill for skill in required if skill not in present]
    return {
        "career_goal": goal,
        "required_skills": required,
        "matching_skills": [s for s in required if s in present],
        "missing_skills": missing,
        "readiness_percent": round(100 * (len(required) - len(missing)) / len(required)) if required else 0,
        "recommendations": [
            {"skill": skill, "resource": f"Study {skill} fundamentals", "activity": f"Build a small project using {skill}"}
            for skill in missing
        ],
        "method": "deterministic skill-gap baseline (not trained AI)",
    }


class API(BaseHTTPRequestHandler):
    db_path = None
    server_version = "UpskillMVP/0.1"

    def log_message(self, fmt, *args):
        # Avoid logging request bodies or authorization headers.
        super().log_message(fmt, *args)

    def send_json(self, status, value):
        payload = json.dumps(value).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")
        self.end_headers()
        self.wfile.write(payload)

    def read_json(self):
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if not 0 < length <= 16384:
                return None
            value = json.loads(self.rfile.read(length))
            return value if isinstance(value, dict) else None
        except (ValueError, TypeError, UnicodeError, json.JSONDecodeError):
            return None

    def user_id(self, db):
        authorization = self.headers.get("Authorization", "")
        if not authorization.startswith("Bearer "):
            return None
        token = authorization.removeprefix("Bearer ").strip()
        if not re.fullmatch(r"[0-9a-f]{64}", token):
            return None
        token_hash = hashlib.sha256(token.encode("ascii")).hexdigest()
        row = db.execute("SELECT user_id FROM sessions WHERE token_hash=? AND expires_at>?", (token_hash, int(time.time()))).fetchone()
        return row["user_id"] if row else None

    def serve_static(self, name, mimetype):
        path = ROOT / name
        if not path.is_file():
            return self.send_json(404, {"error": "File not found"})
        content = path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", mimetype)
        self.send_header("Content-Length", str(len(content)))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Content-Security-Policy", "default-src 'self'; script-src 'self'; style-src 'self'; connect-src 'self'; object-src 'none'; base-uri 'none'")
        self.end_headers()
        self.wfile.write(content)

    def do_GET(self):
        route = urlparse(self.path).path
        if route in ("/", "/index.html"):
            return self.serve_static("index.html", "text/html; charset=utf-8")
        if route == "/app.js":
            return self.serve_static("app.js", "application/javascript; charset=utf-8")
        if route == "/style.css":
            return self.serve_static("style.css", "text/css; charset=utf-8")
        if route == "/health":
            return self.send_json(200, {"status": "ok"})
        if route == "/api/catalog":
            return self.send_json(200, {"career_paths": CAREER_PATHS, "skills": ALL_SKILLS})
        with connect_db(self.db_path) as db:
            uid = self.user_id(db)
            if not uid:
                return self.send_json(401, {"error": "Sign in first"})
            if route == "/api/dashboard":
                user = db.execute("SELECT id, name, email, interests, goal FROM users WHERE id=?", (uid,)).fetchone()
                skills = [r["skill"] for r in db.execute("SELECT skill FROM skills WHERE user_id=? ORDER BY skill", (uid,))]
                completed = [r["skill"] for r in db.execute("SELECT skill FROM progress WHERE user_id=? ORDER BY skill", (uid,))]
                return self.send_json(200, {"profile": dict(user), "skills": skills, "completed": completed, "analysis": gap_report(user["goal"], skills)})
        return self.send_json(404, {"error": "Unknown endpoint"})

    def do_POST(self):
        route = urlparse(self.path).path
        data = self.read_json()
        if data is None:
            return self.send_json(400, {"error": "A JSON object under 16 KB is required"})
        with connect_db(self.db_path) as db:
            if route == "/api/register":
                name = str(data.get("name", "")).strip()
                email = str(data.get("email", "")).strip().lower()
                password = data.get("password", "")
                if not (1 <= len(name) <= 80 and re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", email) and isinstance(password, str) and 8 <= len(password) <= 128):
                    return self.send_json(400, {"error": "Enter a name, valid email and password of at least 8 characters"})
                salt = secrets.token_hex(16)
                try:
                    db.execute("INSERT INTO users (name,email,salt,password_hash) VALUES (?,?,?,?)", (name,email,salt,password_digest(password,salt)))
                    db.commit()
                except sqlite3.IntegrityError:
                    return self.send_json(409, {"error": "Email already registered"})
                return self.send_json(201, {"message": "Account created. Sign in to continue."})
            if route == "/api/login":
                email = str(data.get("email", "")).strip().lower()
                password = data.get("password", "")
                row = db.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
                if not isinstance(password, str) or not row or not secrets.compare_digest(row["password_hash"],password_digest(password,row["salt"])):
                    return self.send_json(401, {"error": "Incorrect email or password"})
                token = secrets.token_hex(32)
                db.execute("INSERT INTO sessions (token_hash,user_id,expires_at) VALUES (?,?,?)", (hashlib.sha256(token.encode()).hexdigest(),row["id"],int(time.time()) + 8*3600))
                db.commit()
                return self.send_json(200, {"token": token, "expires_in_seconds": 28800})
            uid = self.user_id(db)
            if not uid:
                return self.send_json(401, {"error": "Sign in first"})
            if route == "/api/profile":
                name = str(data.get("name", "")).strip()
                interests = str(data.get("interests", "")).strip()
                goal = str(data.get("goal", ""))
                if not 1 <= len(name) <= 80 or len(interests) > 300 or goal not in CAREER_PATHS:
                    return self.send_json(400, {"error": "Enter a name and valid career goal"})
                db.execute("UPDATE users SET name=?,interests=?,goal=? WHERE id=?", (name,interests,goal,uid))
            elif route == "/api/skills":
                skills = data.get("skills")
                if not isinstance(skills, list) or len(skills) > len(ALL_SKILLS) or any(not isinstance(skill,str) or skill not in ALL_SKILLS for skill in skills):
                    return self.send_json(400, {"error": "Select only skills in the catalog"})
                db.execute("DELETE FROM skills WHERE user_id=?", (uid,))
                db.executemany("INSERT OR IGNORE INTO skills (user_id,skill) VALUES (?,?)", [(uid,s) for s in skills])
            elif route == "/api/progress":
                skill = data.get("skill")
                completed = data.get("completed")
                if skill not in ALL_SKILLS or not isinstance(completed,bool):
                    return self.send_json(400, {"error": "Invalid skill or completed value"})
                if completed:
                    db.execute("INSERT OR REPLACE INTO progress (user_id,skill,completed_at) VALUES (?,?,?)", (uid,skill,int(time.time())))
                else:
                    db.execute("DELETE FROM progress WHERE user_id=? AND skill=?", (uid,skill))
            elif route == "/api/logout":
                token = self.headers.get("Authorization", "").removeprefix("Bearer ").strip()
                db.execute("DELETE FROM sessions WHERE token_hash=?", (hashlib.sha256(token.encode()).hexdigest(),))
            else:
                return self.send_json(404, {"error": "Unknown endpoint"})
            db.commit()
        return self.send_json(200, {"message": "Saved"})


def make_server(host="127.0.0.1", port=8000, db_path=None):
    path = Path(db_path or DB_PATH)
    path.parent.mkdir(parents=True, exist_ok=True)
    initialize(path)
    handler = type("ProjectAPI", (API,), {"db_path": path})
    return ThreadingHTTPServer((host, port), handler)


if __name__ == "__main__":
    server = make_server(os.getenv("HOST", "127.0.0.1"), int(os.getenv("PORT", "8000")))
    print(f"Upskilling MVP running at http://{server.server_address[0]}:{server.server_address[1]}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()
