import os
import time

import psycopg2
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
DATABASE_URL = os.environ["DATABASE_URL"]


def get_conn():
    return psycopg2.connect(DATABASE_URL)


def init_db(retries=10):
    for attempt in range(retries):
        try:
            with get_conn() as conn, conn.cursor() as cur:
                cur.execute(
                    """
                    CREATE TABLE IF NOT EXISTS stores (
                        id SERIAL PRIMARY KEY,
                        name TEXT NOT NULL,
                        address TEXT,
                        city TEXT,
                        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
                    )
                    """
                )
            return
        except psycopg2.OperationalError:
            if attempt == retries - 1:
                raise
            time.sleep(2)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        if name:
            with get_conn() as conn, conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO stores (name, address, city) VALUES (%s, %s, %s)",
                    (name, request.form.get("address", "").strip(), request.form.get("city", "").strip()),
                )
        return redirect(url_for("index"))

    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("SELECT id, name, address, city, created_at FROM stores ORDER BY id DESC")
        stores = cur.fetchall()
    return render_template("index.html", stores=stores)


init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
