import sqlite3
import json

from models import Entry


def get_all_entries():
    with sqlite3.connect("./dailyjournal.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
            SELECT
                e.id,
                e.date,
                e.concept,
                e.entry,
                e.mood_id AS mood
            FROM entries e
        """)

        entries = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            entry = Entry(row["id"], row["date"], row["concept"],
                          row["entry"], row["mood"])
            entries.append(entry.__dict__)

        return json.dumps(entries)


def get_single_entry(id):
    with sqlite3.connect("./dailyjournal.db") as conn:
        conn.row_factory = sqlite3.Row

        db_cursor = conn.cursor()
        db_cursor.execute("""
            SELECT
                e.id,
                e.date,
                e.concept,
                e.entry,
                e.mood_id AS mood
            FROM entries e
            WHERE e.id = ?
        """, (id, ))

        row = db_cursor.fetchone()

        entry = Entry(row["id"], row["date"], row["concept"],
                      row["entry"], row["mood"])

        return json.dumps(entry.__dict__)
