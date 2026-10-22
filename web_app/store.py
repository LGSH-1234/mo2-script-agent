import json
import sqlite3
import time
import uuid
from contextlib import contextmanager
from pathlib import Path
from fastapi import HTTPException
from aigc_agent.domain.assets.store import Asset, AssetType


def uid(prefix):
    return prefix + uuid.uuid4().hex[:16]


class Store:
    def __init__(self, path: Path):
        path.parent.mkdir(parents=True, exist_ok=True)
        self.path = path
        with self.connect() as db:
            db.executescript("""
                CREATE TABLE IF NOT EXISTS projects(id TEXT PRIMARY KEY, body TEXT NOT NULL, updated REAL);
                CREATE TABLE IF NOT EXISTS versions(project_id TEXT, version INTEGER, body TEXT NOT NULL,
                    PRIMARY KEY(project_id,version));
                CREATE TABLE IF NOT EXISTS assets(id TEXT PRIMARY KEY, project_id TEXT, body TEXT NOT NULL);
                CREATE TABLE IF NOT EXISTS proposals(id TEXT PRIMARY KEY, project_id TEXT, version INTEGER, body TEXT NOT NULL);
                CREATE TABLE IF NOT EXISTS jobs(id TEXT PRIMARY KEY, project_id TEXT, version INTEGER,
                    shot_id TEXT, status TEXT, created REAL, failure INTEGER, attempt INTEGER,
                    UNIQUE(project_id,version,shot_id,attempt));
            """)

    @contextmanager
    def connect(self):
        db = sqlite3.connect(self.path, timeout=10)
        db.row_factory = sqlite3.Row
        try:
            db.execute("BEGIN IMMEDIATE")
            yield db
            db.commit()
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()

    def get(self, pid, db=None):
        if db is None:
            with self.connect() as conn:
                return self.get(pid, conn)
        row = db.execute("SELECT body FROM projects WHERE id=?", (pid,)).fetchone()
        if row is None:
            raise HTTPException(404, "项目不存在")
        return json.loads(row[0])

    def check(self, p, version):
        if p["version"] != version:
            raise HTTPException(409, "内容已更新，请刷新后操作。")

    def save(self, p, db, asset_type=None):
        if asset_type:
            old = p.get("asset_id")
            asset = Asset(type=AssetType(asset_type), project=p["id"], version=p["version"],
                parent_ids=[old] if old else [], creator=p.get("origin", "human"),
                inline=json.dumps(p.get("shots") if asset_type == "storyboard" else p.get("script"), ensure_ascii=False),
                gen_params={"model": p.get("model"), "prompt_version": "1.0.0"})
            p["asset_id"] = asset.id
            db.execute("INSERT INTO assets VALUES(?,?,?)", (asset.id, p["id"], asset.model_dump_json()))
        raw = json.dumps(p, ensure_ascii=False)
        db.execute("INSERT OR REPLACE INTO projects VALUES(?,?,?)", (p["id"], raw, time.time()))
        db.execute("INSERT OR REPLACE INTO versions VALUES(?,?,?)", (p["id"], p["version"], raw))
        return p

    def changed(self, p):
        p["version"] += 1
        p["approved_version"] = None
        p["stage"] = "storyboard" if p["shots"] else "script" if p["script"] else "brief"

    def jobs(self, pid):
        with self.connect() as db:
            self.get(pid, db)
            # Deterministic simulated provider clock survives server restart.
            now = time.time()
            db.execute("UPDATE jobs SET status='running' WHERE project_id=? AND status='queued' AND created<?", (pid, now-2))
            db.execute("UPDATE jobs SET status=CASE WHEN failure=1 THEN 'failed' ELSE 'succeeded' END WHERE project_id=? AND status='running' AND created<?", (pid, now-7))
            return [dict(r) | {"simulated": True, "video_url": "/media/sample.mp4" if r["status"] == "succeeded" else None}
                for r in db.execute("SELECT * FROM jobs WHERE project_id=? ORDER BY created DESC", (pid,))]
