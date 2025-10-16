# utils.py
import sqlite3
import csv
import io
from typing import List, Dict

DB_FILE = "disk_runs.db"

def parse_requests(text: str) -> List[int]:
    if text is None:
        return []
    s = text.strip()
    if s == "":
        return []
    parts = s.replace(",", " ").split()
    nums = []
    for p in parts:
        try:
            nums.append(int(p))
        except:
            raise ValueError(f"Invalid request value: {p}")
    return nums

def compute_disk_metrics(path: List[int], requests_count: int, seek_time_per_cylinder_ms: float = 1.0) -> Dict:
    total_movement = 0
    for i in range(1, len(path)):
        total_movement += abs(path[i] - path[i-1])
    avg_seek = total_movement / requests_count if requests_count > 0 else 0
    total_time_seconds = (total_movement * seek_time_per_cylinder_ms) / 1000.0
    throughput = (requests_count / total_time_seconds) if total_time_seconds > 0 else 0
    return {
        "total_head_movement": int(total_movement),
        "average_seek_distance": round(avg_seek, 3),
        "total_time_seconds": round(total_time_seconds, 5),
        "throughput_req_per_sec": round(throughput, 3)
    }

# --- SQLite helpers ---
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            requests TEXT,
            head INTEGER,
            algorithm TEXT,
            direction TEXT,
            disk_start INTEGER,
            disk_end INTEGER,
            seek_ms REAL,
            total_movement INTEGER,
            avg_seek REAL,
            throughput REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_run(name: str, requests_text: str, head: int, algorithm: str, direction: str,
             disk_start: int, disk_end: int, seek_ms: float, metrics: Dict):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        INSERT INTO runs (name, requests, head, algorithm, direction, disk_start, disk_end, seek_ms, total_movement, avg_seek, throughput)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (name, requests_text, head, algorithm, direction, disk_start, disk_end, seek_ms,
          metrics.get("total_head_movement", 0), metrics.get("average_seek_distance", 0), metrics.get("throughput_req_per_sec", 0)))
    conn.commit()
    conn.close()

def fetch_history():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT id, name, requests, head, algorithm, direction, disk_start, disk_end, seek_ms, total_movement, avg_seek, throughput, timestamp FROM runs ORDER BY id DESC')
    rows = c.fetchall()
    conn.close()
    return rows

def history_to_csv(rows):
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["id","name","requests","head","algorithm","direction","disk_start","disk_end","seek_ms","total_movement","avg_seek","throughput","timestamp"])
    for r in rows:
        writer.writerow(r)
    return output.getvalue()
