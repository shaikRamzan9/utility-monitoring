from flask import Flask, render_template, request
import psycopg2

app = Flask(__name__)

DB_CONFIG = {
    "host": "db",        # Docker service name
    "database": "utility_events",
    "user": "postgres",
    "password": "postgres",
    "port": 5432
}

@app.route("/")
def index():
    city = request.args.get("city")
    category = request.args.get("category")

    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    query = """
        SELECT title, city, category, published_at
        FROM events
        WHERE 1=1
    """
    params = []

    # Apply city filter only if provided
    if city and city.strip() != "":
        query += " AND city ILIKE %s"
        params.append(f"%{city}%")

    # Apply category filter only if selected and not "All"
    if category and category != "All":
        query += " AND category = %s"
        params.append(category)

    query += " ORDER BY published_at DESC LIMIT 50"

    cur.execute(query, params)
    rows = cur.fetchall()

    cur.close()
    conn.close()

    return render_template("index.html", rows=rows)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
