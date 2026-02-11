# Utility Event Monitoring System

A containerized end-to-end data pipeline that ingests utility-related news events, extracts structured information (category and city), stores them in PostgreSQL, and provides a searchable web dashboard.

This project demonstrates practical backend system design, text processing, database modeling, and containerized deployment.

---

## Overview

The system monitors news feeds for utility-related incidents including:

- Power failures and grid outages
- Water supply issues
- Logistics disruptions

It transforms unstructured news articles into structured, queryable records and exposes them through a lightweight web interface.

---

## Architecture

### High-Level Design
RSS Feeds
│
▼
Ingestion Service (Python ETL)
│ • Fetch articles
│ • Parse metadata
│ • Classify category
│ • Extract city
▼
PostgreSQL Database
│ • Structured storage
│ • Indexed queries
▼
Flask Web Application
• Filter by city
• Filter by category
• View recent incidents

---

## Components

### 1. Ingestion Service

Responsible for transforming raw RSS content into structured records.

**Responsibilities:**
- Fetch articles from RSS feeds
- Extract title, summary, source, and publication timestamp
- Perform rule-based classification
- Extract city from text
- Insert records into PostgreSQL

The ingestion logic is implemented in `ingestion.py`.

---

### 2. Classification Logic

Implemented in `classifier.py`.

The system categorizes events into:

- `power_failure`
- `water_issue`
- `logistics_disruption`
- `other`

Classification uses deterministic keyword matching to ensure explainability and predictable behavior.

---

### 3. Location Extraction

Implemented in `location_extractor.py`.

The system:
- Searches for known city names in title and summary
- Uses case-insensitive matching
- Stores the first detected city
- Defaults to `Unknown` if no match is found

This lightweight approach keeps the pipeline efficient while maintaining reasonable accuracy.

---

### 4. Database Layer

PostgreSQL is used for structured storage.

**Table: `events`**

Key fields:
- `id`
- `title`
- `summary`
- `city`
- `category`
- `source`
- `published_at`

The schema supports efficient filtering by:
- Category
- City
- Publication date

---

### 5. Web Application

The Flask-based UI (`app.py`) provides:

- Display of latest events
- Filtering by category
- Filtering by city
- Results sorted by publication time

Accessible at:
http://localhost:8000


## Project Structure
utility-monitoring/
│
├── app/
│ ├── app.py
│ ├── ingestion.py
│ ├── classifier.py
│ ├── location_extractor.py
│ ├── Dockerfile
│ └── templates/index.html
│
├── db/
│ └── schema.sql
│
├── docker-compose.yml
├── README.md
├── REPORT.md
├── events_dump.sql
## Database Dump

A database export file (`events_dump.sql`) is included.

To restore:

docker exec -i utility_db psql -U postgres utility_events < events_dump.sql
This shows:
- Reproducibility
- Production mindset
- Deployment awareness

## Running the Project

### Prerequisites

- Docker
- Docker Compose

---

### Start Services

From the project root:
docker-compose up --build
This will start:

- PostgreSQL database
- Ingestion service
- Flask web application

---

### Verify Running Containers
docker ps


### Database Access

To connect to PostgreSQL:
docker exec -it utility_db psql -U postgres -d utility_events

Example queries:

SELECT COUNT(*) FROM events;

SELECT category, COUNT(*)
FROM events
GROUP BY category;

SELECT *
FROM events
ORDER BY published_at DESC
LIMIT 10;

## Tech Stack

- Python
- Flask
- PostgreSQL
- Docker & Docker Compose

---

## Summary

This project demonstrates:

- End-to-end data ingestion pipeline design
- Text classification and information extraction
- Relational database modeling
- Containerized deployment
- Modular backend architecture

It provides a structured and extensible foundation for real-time utility event monitoring.