# Cloud Cost Knowledge Graph RAG

Hybrid RAG system for cloud cost intelligence aligned with FOCUS 1.0 specification.

# 📁 Project Structure
```bash
cloud-cost-kb/
│
├── app.py
├── ingest.py
├── rag.py
├── ontology_design.md
├── schema.cypher
├── README.md
├── test_queries.md
│
├── data/
│   └── sample_data.csv
│
└── screenshots/
    └── screenshos
```

## Architecture

CSV → Neo4j Graph → Embeddings → Hybrid Retrieval → Groq LLM → Streamlit UI

## Technologies

- Python 3.11
- Neo4j
- SentenceTransformers
- Groq LLM
- Streamlit

## Setup

1. Create conda environment
2. Install dependencies
3. Configure .env
4. Run ingest.py
5. Run streamlit app.py

## Features

- Graph-based cost modeling
- Semantic search with embeddings
- Hybrid retrieval
- Aggregation queries
- Cost ranking analysis

## References

- FinOps Foundation
- FOCUS 1.0 Specification
- AWS Billing Docs

- Azure Billing Docs
