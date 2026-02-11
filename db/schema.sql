DROP TABLE IF EXISTS events;

CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    title TEXT,
    summary TEXT,
    full_text TEXT,
    city VARCHAR(100),
    state VARCHAR(100),
    category VARCHAR(50),
    source TEXT,
    published_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);