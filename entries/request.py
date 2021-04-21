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


# def get_all_customers():
#     # Open a connection to the database
#     with sqlite3.connect("./kennel.db") as conn:

#         # .Row converts plain tuple into more useful object
#         # .cursor is a reference to the db
#         conn.row_factory = sqlite3.Row
#         db_cursor = conn.cursor()

#         # Write the SQL query to get the information you want
#         db_cursor.execute("""
#         SELECT
#             c.id,
#             c.name,
#             c.address,
#             c.email,
#             c.password
#         FROM customer c
#         """)

#         # Initialize an empty list to hold all customer representations
#         customers = []

#         # Convert rows of data into a Python list
#         dataset = db_cursor.fetchall()

#         # Iterate list of data returned from database
#         # For large datasets you can also iterate over the cursor itself.
#         for row in dataset:

#             # Create an customer instance from the current row.
#             # Note that the database fields are specified in
#             # exact order of the parameters defined in the
#             # Customer class above.
#             customer = Customer(row['id'], row['name'], row['address'],
#                                 row['email'], row['password'])

#             customers.append(customer.__dict__)

#     # `json` package serializes list as JSON
#     return json.dumps(customers)
