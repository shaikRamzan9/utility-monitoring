#  Utility Event Monitoring System – Technical Summary

**Overview**

This system ingests utility-related news events, classifies them into predefined categories (Power, Water, Logistics), extracts associated cities, stores structured data in PostgreSQL, and provides a searchable web interface for analysis.
The objective is to simulate a lightweight real-time monitoring pipeline for critical infrastructure disruptions.

**Data Sources**

Currently, the ingestion layer uses structured sample events to simulate real-world feeds.
The architecture supports extension to:
->ews APIs
->RSS feeds
->Government outage reports
->Logistics disruption alerts
The system is source-agnostic and designed for extensibility.

**Category Inference Approach**

Event categorization is performed using rule-based keyword matching.
Categories:
->power_failure
->water_issue
->logistics_disruption

Method:
The classifier inspects:
->Article title
->Article summary
It searches for domain-specific keywords:
Category	    Example Keywords
Power	        outage, blackout, grid, electricity
Water	        shortage, drought, reservoir, supply
Logistics	    delay, port, shipment, congestion
The first matching rule assigns the category.
If no rule matches, the event can be labeled as other (future extension).

**Location (City) Extraction Approach**

City extraction is rule-based and uses predefined city matching.
The system scans:
->Title
->Summary
It checks against a list of known cities (e.g., Mumbai, Chennai, Kolkata, Delhi).
If a city is detected in text:
->It is stored in the city field.
->Otherwise, the value defaults to "Unknown".
This approach ensures deterministic behavior without external NLP dependencies.

**Database Design**
PostgreSQL schema:
events (
    id SERIAL PRIMARY KEY,
    title TEXT,
    summary TEXT,
    category TEXT,
    city TEXT,
    published_at TIMESTAMP
)

The schema supports:
->Category filtering
->City filtering
->Time-based sorting
->Future indexing for performance optimization

**Success Examples**

✔ "Power outage hits Mumbai grid"
→ Category: power_failure
→ City: Mumbai

✔ "Water shortage reported in Chennai"
→ Category: water_issue
→ City: Chennai

✔ "Logistics delays at Kolkata port"
→ Category: logistics_disruption
→ City: Kolkata

**Failure / Limitations**

->If the city is not in predefined list, it will not be detected.
->If wording differs significantly from keyword list, classification may fail.
->No deduplication logic implemented yet.
->No advanced NLP or ML model used.

**Production Improvements**
To make the system production-ready:
1. Replace rule-based classifier with ML/NLP model (e.g., fine-tuned transformer).
2. Use Named Entity Recognition (NER) for robust location extraction.
3. Add event deduplication using hash-based fingerprinting.
4. Add indexing on category, city, and published_at.
5. Add logging, monitoring, and retry logic.
6. Add rate limiting and error handling for external APIs.
7. Deploy behind production WSGI server (e.g., Gunicorn).

**Conclusion**

This project demonstrates:

- End-to-end ETL pipeline design
- Rule-based text classification
- Structured relational database modeling
- Containerized microservice-style deployment
- Backend system design principles