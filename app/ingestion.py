import psycopg2
import time
from datetime import datetime
from classifier import classify_event

# -----------------------
# Database Configuration
# -----------------------

DB_CONFIG = {
    "host": "db",
    "dbname": "utility_events",
    "user": "postgres",
    "password": "postgres",
    "port": 5432
}

# -----------------------
# Wait for DB
# -----------------------

def get_connection():
    while True:
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            print("Connected to DB")
            return conn
        except psycopg2.OperationalError:
            print("Waiting for DB...")
            time.sleep(3)

# -----------------------
# Create Table
# -----------------------

def create_table():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id SERIAL PRIMARY KEY,
            title TEXT,
            summary TEXT,
            category TEXT,
            city TEXT,
            published_at TIMESTAMP
        );
    """)

    conn.commit()
    cur.close()
    conn.close()

# -----------------------
# Fetch Sample Data
# -----------------------

def fetch_articles():
    cities = ["Mumbai", "Chennai", "Kolkata", "Delhi", "Hyderabad", "Bangalore", "Pune"]
    
    events = []

    for i in range(20):
        events.append({
            "title": f"Power outage reported in {cities[i % len(cities)]}",
            "summary": f"Electricity disruption affecting multiple areas in {cities[i % len(cities)]}.",
            "published_at": datetime.now()
        })

    for i in range(20):
        events.append({
            "title": f"Water shortage crisis in {cities[i % len(cities)]}",
            "summary": f"Reservoir levels critically low in {cities[i % len(cities)]}.",
            "published_at": datetime.now()
        })

    for i in range(20):
        events.append({
            "title": f"Logistics delay at {cities[i % len(cities)]} transport hub",
            "summary": f"Supply chain disruption impacting deliveries in {cities[i % len(cities)]}.",
            "published_at": datetime.now()
        })

    return events
# -----------------------
# Store Articles
# -----------------------

def store_articles():
    conn = get_connection()
    cur = conn.cursor()

    articles = fetch_articles()

    for article in articles:
        title = article["title"]
        summary = article["summary"]
        published_at = article["published_at"]

        category, city = classify_event(title, summary)

        cur.execute("""
            INSERT INTO events (title, summary, category, city, published_at)
            VALUES (%s, %s, %s, %s, %s)
        """, (title, summary, category, city, published_at))

    conn.commit()
    cur.close()
    conn.close()

    print("Articles stored successfully")

# -----------------------
# Main
# -----------------------

if __name__ == "__main__":
    create_table()
    store_articles()
