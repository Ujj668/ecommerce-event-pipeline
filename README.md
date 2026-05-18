# E-Commerce Event Analytics Pipeline

## Problem Statement
An e-commerce company generates thousands of customer events daily : page views, add-to-carts, purchases, and drop-offs. This raw data lands in S3 as unstructured JSON files with no quality checks and no way to answer business questions quickly.

This project builds an end-to-end pipeline that ingests, transforms, and models this data into clean, tested, documented tables

## Business Questions Answered
- What is the purchase conversion rate by product category?
- Which products are frequently added to cart but never purchased?
- What is the revenue trend by country?
- Where in the funnel are users dropping off most?

## Architecture
Python Producer → AWS Lambda → S3 (raw/) → AWS Glue → S3 (processed/) → Databricks → dbt → Mart Tables

## Tech Stack
| Tool | Purpose |

| Python + Faker | Simulate e-commerce event stream |
| AWS Lambda | Event ingestion and validation |
| AWS S3 | Raw and processed data lake storage |
| AWS Glue (PySpark) | JSON to Parquet transformation |
| AWS Athena | Ad-hoc SQL on processed data |
| Databricks | Delta table hosting |
| dbt Core + dbt-databricks | Modular SQL transformations and data quality |
| GitHub | Version control |

## Pipeline Walkthrough

### Phase 1 — Ingest
- Python script simulates 50 e-commerce events (page_view, add_to_cart, purchase, remove_from_cart)
- Each event sent to AWS Lambda via boto3
- Lambda validates required fields and writes JSON to S3 partitioned by date:
  `raw/year=2026/month=05/day=17/event-uuid.json`

### Phase 2 — Transform
- AWS Glue PySpark job reads all raw JSON files recursively
- Removes duplicates on event_id and drops null records
- Writes clean Parquet file to `processed/`
- Glue Crawler scans processed folder and registers schema in Glue Data Catalog
- Athena used for ad-hoc SQL validation on processed data

### Phase 3 — dbt Models
- dbt-databricks adapter connects local dbt to Databricks SQL Warehouse via OAuth
- Two models built following staging → marts pattern:
  - `stg_events` — cleans raw_events table, casts types, filters nulls
  - `mart_revenue` — aggregates revenue and purchase counts by event_type, category, country
- `schema.yml` adds 5 automated data quality tests:
  - event_id: not_null, unique
  - event_type: not_null, accepted_values
  - user_id: not_null
- `dbt docs generate` produces lineage graph showing model dependencies

  ## Dashbord : 
  https://dbc-cea0aa49-c937.cloud.databricks.com/dashboardsv3/01f15284a7f21bd99e8c2cc50e6e086b/published?o=4242966323867709


## Key Learnings
- AWS Lambda IAM roles are auto-created during function setup, always verify the role has required permissions
- Databricks Community Edition uses Unity Catalog which restricts direct S3 access,worked around by uploading Parquet to a Databricks Volume
- Databricks tokens on free tier don't have SQL warehouse scope, OAuth is the correct auth method
- dbt `{{ ref() }}` function automatically resolves model dependencies and determines execution order

## Repository Structure
ecommerce-event-pipeline/
├── producer/
│   └── generate_events.py       # Fake event generator
├── lambda/
│   └── ingest_handler.py        # Lambda ingestion function
├── glue/
│   └── transform_job.py         # Glue PySpark ETL job
├── athena/
│   └── queries.sql              # Athena validation queries
├── dbt/
│   └── ecommerce_dbt/
│       ├── models/
│       │   ├── staging/
│       │   │   ├── stg_events.sql
│       │   │   └── schema.yml
│       │   └── marts/
│       │       └── mart_revenue.sql
│       └── dbt_project.yml
└── README.md

## Author
**Ujjwal Tyagi**  
Data Engineer  
[GitHub](https://github.com/Ujj668) | [LinkedIn](https://www.linkedin.com/in/ujjwal-tyagi-758004148/)
