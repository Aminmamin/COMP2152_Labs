# ============================================================
#  WEEK 10 LAB — Q2: LOGIN ATTEMPT TRACKER
#  COMP2152 — Muhammad-Amin Farhan Ali
# ============================================================

import sqlite3
import datetime

DB_NAME = "login_tracker.db"


# --- Helpers (provided) ---
def setup_database():
    """Create the login_attempts table if it doesn't exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS login_attempts")
    cursor.execute("""CREATE TABLE login_attempts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        success INTEGER,
        attempt_date TEXT
    )""")
    conn.commit()
    conn.close()


def display_attempts(attempts):
    """Pretty-print a list of attempt rows."""
    if not attempts:
        print("  (no results)")
        return
    for row in attempts:
        status = "success" if row[2] else "FAILED"
        print(f"  {row[1]:<8} | {status:<7} | {row[3]}")


def record_attempt(username, success):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    current_time = str(datetime.datetime.now())
    cursor.execute(
        "INSERT INTO login_attempts (username, success, attempt_date) VALUES (?, ?, ?)",
        (username, success, current_time)
    )
    conn.commit()
    conn.close()


def get_failed_attempts(username):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM login_attempts WHERE username = ? AND success = 0",
        (username,)
    )
    rows = cursor.fetchall()
    conn.close()
    return rows


def count_failures_per_user():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT username, COUNT(*) FROM login_attempts WHERE success = 0 GROUP BY username"
    )
    rows = cursor.fetchall()
    conn.close()
    return rows


def delete_old_attempts(username):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM login_attempts WHERE username = ?", (username,))
    conn.commit()
    deleted_rows = cursor.rowcount
    conn.close()
    return deleted_rows


# --- Main (provided) ---
if __name__ == "__main__":
    print("=" * 60)
    print("  LOGIN ATTEMPT TRACKER")
    print("=" * 60)

    setup_database()

    print("\n--- Recording Login Attempts ---")
    attempts = [
        ("admin", True),
        ("admin", False),
        ("admin", False),
        ("admin", False),
        ("guest", True),
        ("guest", False),
        ("root", False),
        ("root", False),
        ("root", False),
        ("root", False),
    ]

    for user, success in attempts:
        record_attempt(user, success)
        status = "success" if success else "FAILED"
        print(f"  Recorded: {user} ({status})")

    print("\n--- Failed Attempts for 'admin' ---")
    display_attempts(get_failed_attempts("admin"))

    print("\n--- Failure Counts ---")
    counts = count_failures_per_user()
    if counts:
        for user, count in counts:
            msg = f"  {user:<10}  {count} failed attempts"
            if count >= 4:
                msg += f"  ⚠ {user} has {count} failed attempts — possible brute-force!"
            print(msg)
    else:
        print("  (no failures)")

    print("\n--- Reset 'root' account (delete all attempts) ---")
    deleted = delete_old_attempts("root")
    if deleted:
        print(f"  Deleted {deleted} records for root")
    else:
        print("  (nothing to delete)")

    print("\n--- Failure Counts (after reset) ---")
    counts = count_failures_per_user()
    if counts:
        for user, count in counts:
            print(f"  {user:<10}  {count} failed attempts")
    else:
        print("  (no failures)")

    print("\n" + "=" * 60)