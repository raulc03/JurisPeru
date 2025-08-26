# MonoRepo Project

This repository is a **MonoRepo** containing multiple interconnected components for data processing and serving, including two pipelines and an API service.

## Table of Contents
- [Overview](#overview)
- [Project Structure](#project-structure)
- [Pipelines](#pipelines)
  - [Ingest Pipeline](#ingest-pipeline)
- [API Service](#api-service)
- [Getting Started](#getting-started)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)

## Overview
This MonoRepo is designed to streamline data ingestion, retrieval-augmented generation (RAG), and API serving. Each component is modular, allowing for independent development and deployment.

## Project Structure
```
monorepo/
├── ingest-pipeline/
├── api-service/
├── README.md
└── ...
```

- **ingest-pipeline/**: Handles data ingestion and preprocessing.
- **api/**: Exposes endpoints for interacting with the RAG pipeline.

## Pipelines

### Ingest Pipeline
- **Purpose:** Collects, cleans, and preprocesses raw data for downstream tasks.
- **Features:**
  - Data extraction from multiple sources
  - Data validation and transformation
  - Storage in a unified format

### RAG Pipeline
- **Purpose:** Performs retrieval-augmented generation using ingested data.
- **Features:**
  - Efficient document retrieval
  - Integration with language models
  - Output generation based on retrieved context

## API Service
- **Purpose:** Provides a RESTful interface to interact with the RAG pipeline.
- **Features:**
  - Endpoints for triggering RAG tasks
  - Query and retrieval endpoints

## Getting Started
1. **Clone the repository:**
   ```sh
   git clone https://github.com/raulc03/02-project.git
   cd 02-project
   ```
2. **Install dependencies:**
   - Each component has its own `README.md` and setup instructions.
   - Example for the ingest pipeline:
     ```sh
     cd ingest-pipeline
     pip install -r requirements.txt
     ```
3. **Run services:**
   - Start pipelines and API as described in their respective directories.
