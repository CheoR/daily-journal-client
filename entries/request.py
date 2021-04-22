import sqlite3
import json

from models import Entry
from models import Mood


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
                e.mood_id AS entry_mood,
                m.id AS mood_id,
                m.label AS mood
            FROM entries e
            JOIN moods m
                ON e.mood_id = m.id
        """)

        entries = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            entry = Entry(row["id"], row["date"], row["concept"],
                          row["entry"], row["entry_mood"])
            mood = Mood(row["mood_id"], row["mood"])

            entry.mood = mood.__dict__
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
                e.mood_id AS entry_mood,
                m.id AS mood_id,
                m.label AS mood
            FROM entries e
            JOIN moods m
                ON e.mood_id = m.id
            WHERE e.id = ?
        """, (id, ))

        row = db_cursor.fetchone()

        entry = Entry(row["id"], row["date"], row["concept"],
                      row["entry"], row["entry_mood"])
        mood = Mood(row["mood_id"], row["mood"])

        entry.mood = mood.__dict__
        return json.dumps(entry.__dict__)


def delete_single_entry(id):
    with sqlite3.connect("./dailyjournal.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
            DELETE FROM entries
            WHERE id = ?
        """, (id, ))


def search_entries(term):
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
            WHERE e.entry LIKE ? OR e.concept LIKE ?
        """, (f"%{term}%", f"%{term}%", ))

    entries = []
    data = db_cursor.fetchall()

    for row in data:
        entry = Entry(row["id"], row["date"], row["concept"],
                      row["entry"], row["mood"])
        entries.append(entry.__dict__)

    return json.dumps(entries)


def create_journal_entry(new_entry):
    with sqlite3.connect("./dailyjournal.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
            INSERT INTO entries
                ( date, entry, concept, mood_id )
            VALUES
                ( ?, ?, ?, ? );
        """, (new_entry["date"], new_entry["entry"], new_entry["concept"], new_entry["mood_id"], ))

        id = db_cursor.lastrowid

        new_entry["id"] = id

    return json.dumps(new_entry)


def update_entry(id, new_entry):
    with sqlite3.connect("./dailyjournal.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
            UPDATE entries
                SET
                    date = ?,
                    entry = ?,
                    concept = ?,
                    mood_id = ?
            WHERE id = ?
        """, (new_entry["date"], new_entry["entry"], new_entry["concept"], new_entry["mood_id"], id))

        rows_affected = db_cursor.rowcount

        # If rows affected, return 204, else 404
        return True if rows_affected else False
