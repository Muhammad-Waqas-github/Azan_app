import sqlite3
from flask import Flask, g, jsonify, request

app = Flask(__name__, static_url_path="")

DATABASE = "database.db"


# Get the SQLite database connection
def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_db(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


# Create the table if it doesn't exist
def create_table():
    with app.app_context():
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS azan_table (
                prayer TEXT PRIMARY KEY,
                azan_time TEXT,
                azan_status TEXT,
                dua_status TEXT
            )
        """
        )
        prayer_times = [
            ("Fajr", "01:21 pm", "on", "on"),
            ("Dhuhr", "01:21 pm", "on", "on"),
            ("Asr", "01:21 pm", "on", "on"),
            ("Maghrib", "01:21 pm", "on", "on"),
            ("Isha", "01:21 pm", "on", "on"),
        ]

        cursor.executemany(
            """
            INSERT OR REPLACE INTO azan_table (prayer, azan_time, azan_status, dua_status) VALUES (?, ?, ?, ?)
        """,
            prayer_times,
        )

        conn.commit()
        cursor.close()


# create_table()  # Call the function to create the table


def update_times(prayer_times):
    with app.app_context():
        conn = get_db()
        cursor = conn.cursor()

        for prayer, time in prayer_times.items():  # Iterate over key-value pairs
            cursor.execute(
                """
                UPDATE azan_table SET azan_time = ? WHERE prayer = ?
                """,
                (time, prayer.capitalize()),
            )

        conn.commit()

        cursor.execute("SELECT * FROM azan_table")
        updated_data = cursor.fetchall()
        for row in updated_data:
            print(row)

        cursor.close()


# Define a Flask route that retrieves data from the database
@app.route("/api", methods=["POST"])
def get_data():
    print("start")
    with app.app_context():
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM azan_table")
        data = cursor.fetchall()

        cursor.close()

        try:
            if request.method == "POST":
                return jsonify(data)
        except:
            print("here", "\n")
            print(data)
            print("here", "\n")
            return data


@app.route("/api/update", methods=["POST"])
def update_prayer_status():
    with app.app_context():
        conn = get_db()
        cursor = conn.cursor()

        request_data = request.get_json()
        prayer = request_data.get("prayer")
        field = request_data.get("field")
        value = request_data.get("value")

        # Update the specified field of the prayer in the database
        cursor.execute(
            """
            UPDATE azan_table SET {} = ? WHERE prayer = ?
            """.format(
                field
            ),
            (value, prayer),
        )
        conn.commit()

        # Retrieve the updated data from the database
        cursor.execute("SELECT * FROM azan_table")
        data = cursor.fetchall()

        cursor.close()
        return jsonify(data)


@app.route("/", methods=["GET"])
def serve_index():
    # print(static_dir)
    return app.send_static_file("index.html")


if __name__ == "__main__":
    app.run(debug=True)
