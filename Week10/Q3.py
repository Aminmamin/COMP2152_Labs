# ============================================================
#  WEEK 10 LAB — Q3: SECURITY AUDIT LOG + UNIT TESTS
#  COMP2152 — Muhammad-Amin Farhan Ali
# ============================================================

import sqlite3
import unittest

DB_NAME = "audit.db"


# --- Helpers (provided) ---
def seed_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS audit_log")
    cursor.execute("""CREATE TABLE audit_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        user TEXT,
        action TEXT,
        severity TEXT,
        details TEXT
    )""")

    sample_data = [
        ("2026-03-16 08:00:00", "admin", "LOGIN", "LOW", "Successful login"),
        ("2026-03-16 08:05:00", "root", "FAILED_LOGIN", "HIGH", "SSH failed"),
        ("2026-03-16 08:10:00", "admin", "FILE_ACCESS", "LOW", "Read config"),
        ("2026-03-16 08:15:00", "root", "FAILED_LOGIN", "HIGH", "SSH failed"),
        ("2026-03-16 08:20:00", "guest", "FILE_MODIFY", "MEDIUM", "Modified file"),
        ("2026-03-16 08:25:00", "admin", "PERMISSION_CHANGE", "HIGH", "Changed perms"),
        ("2026-03-16 08:30:00", "guest", "LOGOUT", "LOW", "Session ended"),
        ("2026-03-16 08:35:00", "backup", "FILE_ACCESS", "LOW", "Backup read"),
        ("2026-03-16 08:40:00", "guest", "FILE_MODIFY", "MEDIUM", "Edited file"),
        ("2026-03-16 08:45:00", "admin", "LOGOUT", "LOW", "Session ended"),
    ]

    cursor.executemany(
        "INSERT INTO audit_log (timestamp, user, action, severity, details) VALUES (?, ?, ?, ?, ?)",
        sample_data
    )
    conn.commit()
    conn.close()


def display_events(events):
    if not events:
        print("  (no events)")
        return
    for row in events:
        print(f"  [{row[1]}] {row[4]:<6} {row[2]:<8} {row[3]:<18} {row[5]}")


# ---------------- FUNCTIONS ----------------

def get_events_by_severity(severity):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM audit_log WHERE severity = ?", (severity,))
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_recent_events(limit):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM audit_log ORDER BY timestamp DESC LIMIT ?",
        (limit,)
    )
    rows = cursor.fetchall()
    conn.close()
    return rows


def count_by_severity():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT severity, COUNT(*) FROM audit_log GROUP BY severity ORDER BY COUNT(*) DESC"
    )
    rows = cursor.fetchall()
    conn.close()
    return rows


def safe_query(query):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []
    finally:
        conn.close()


# ---------------- UNIT TESTS ----------------

class TestAuditLog(unittest.TestCase):

    def setUp(self):
        seed_database()

    def test_high_severity(self):
        events = get_events_by_severity("HIGH")
        self.assertEqual(len(events), 3)

    def test_recent_events(self):
        events = get_recent_events(5)
        self.assertEqual(len(events), 5)

    def test_count(self):
        counts = count_by_severity()
        self.assertIn(("HIGH", 3), counts)

    def test_safe_bad_query(self):
        result = safe_query("SELECT * FROM fake_table")
        self.assertEqual(result, [])


# ---------------- MAIN ----------------

if __name__ == "__main__":
    print("=" * 60)
    print("  SECURITY AUDIT LOG")
    print("=" * 60)

    seed_database()

    print("\n--- HIGH Severity Events ---")
    display_events(get_events_by_severity("HIGH"))

    print("\n--- 5 Most Recent Events ---")
    display_events(get_recent_events(5))

    print("\n--- Event Counts ---")
    for severity, count in count_by_severity():
        print(f"  {severity:<8} {count}")

    print("\n--- Safe Query ---")
    results = safe_query("SELECT user, action FROM audit_log WHERE severity = 'HIGH'")
    for r in results:
        print(f"  {r[0]} - {r[1]}")

    print("\n--- Bad Query Test ---")
    print(safe_query("SELECT * FROM wrong_table"))

    print("\n--- Running Tests ---")
    unittest.main(verbosity=2, exit=False)

    print("\n" + "=" * 60)
    