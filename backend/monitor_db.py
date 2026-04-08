
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "database.sqlite")

def monitor_activities():
    if not os.path.exists(DB_PATH):
        print(f"Database not found at {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("\n--- Registered Users ---")
    cursor.execute("SELECT id, name, email FROM users")
    users = cursor.fetchall()
    for user in users:
        print(f"ID: {user[0]}, Name: {user[1]}, Email: {user[2]}")

    print("\n--- Recent Activities (Logins, Signups, Summaries) ---")
    cursor.execute("""
        SELECT u.name, t.title, t.description, t.timestamp 
        FROM timeline_events t
        JOIN users u ON t.user_id = u.id
        ORDER BY t.timestamp DESC
        LIMIT 20
    """)
    activities = cursor.fetchall()
    for act in activities:
        print(f"[{act[3]}] {act[0]} - {act[1]}: {act[2]}")

    conn.close()

if __name__ == "__main__":
    monitor_activities()
