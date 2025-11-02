# AI-Assisted Content Management System (CMS)

A scalable, air-gapped-friendly CMS that enables **semantic + keyword search** over large corpora of scientific PDFs. The stack uses **Flask** (API), **MongoDB** (metadata/users), **Typesense** (vector + lexical search), **Ollama** (local embeddings/LLM), optional **Celery + Redis** for background ingestion, and **React + Vite** dashboards for Admin and Users.

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Directory Structure](#directory-structure)
- [Prerequisites](#prerequisites)
- [Quick Start — Linux/macOS](#quick-start--linuxmacos)
- [Quick Start — Windows (PowerShell)](#quick-start--windows-powershell)
- [Environment Variables](#environment-variables)
- [Ollama & Embedding Models](#ollama--embedding-models)
- [Typesense Setup](#typesense-setup)
- [MongoDB Setup](#mongodb-setup)
- [Ingestion & Indexing Workflow](#ingestion--indexing-workflow)
- [Running the Dashboards](#running-the-dashboards)
- [API Endpoints (Snapshot)](#api-endpoints-snapshot)
- [Backup & Restore](#backup--restore)
- [Troubleshooting](#troubleshooting)
- [Security Notes](#security-notes)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

The system enables researchers to locate relevant documents by meaning, not just keywords. PDFs are parsed, chunked, embedded locally via **Ollama**, indexed in **Typesense**, and served via a **Flask** API with role-based access (Admin/User). Designed for on-prem institutional LANs.

---

## Architecture

```
+-------------------+        REST        +-------------------+
|   Admin/User UI   |  <---------------->|     Flask API     |
|   (React + Vite)  |                   /|  Auth, CRUD, RAG  |
+-------------------+                  / +-------------------+
             |                        /
             v                       v
    +------------------+     +------------------+
    |    Celery/RQ     |     |     MongoDB      |
    |  Ingest Workers  |     |  metadata/users  |
    +------------------+     +------------------+
             |
             v
    +------------------+     +------------------+
    |      Ollama      |<--->|    Typesense     |
    |   embeddings     |     | vector + keyword |
    +------------------+     +------------------+
```

---

## Features

- **Hybrid Retrieval:** Vector (semantic) + lexical with field boosts and filters.
- **Air-Gapped Ready:** All inference local via **Ollama**; no external calls after model pull.
- **Admin Dashboard:** Users/roles, collections, ingestion jobs, re-index operations.
- **User Dashboard:** Faceted search, result previews, metadata filters.
- **Robust Ingestion:** Text + tables extraction, chunking, deduping, resumable jobs.
- **JWT Auth & RBAC:** Access/refresh tokens, role guards on admin routes.

---

## Tech Stack

- **Backend:** Python 3.11, Flask, Uvicorn/Gunicorn
- **DB:** MongoDB 6.x
- **Search:** Typesense 0.25+ (vector fields enabled)
- **Embeddings/LLM:** Ollama (e.g., `nomic-embed-text`, `mxbai-embed-large`)
- **Workers:** Celery + Redis (or RQ)
- **Parsing:** `pypdf`, `pdfminer.six`, `unstructured`
- **Frontend:** React + Vite (Admin & User dashboards)

---

## Directory Structure

```
ai-cms/
├─ backend/
│  ├─ app.py
│  ├─ api/
│  ├─ core/
│  ├─ services/
│  ├─ workers/
│  ├─ models/
│  ├─ scripts/
│  └─ requirements.txt
├─ frontend/
│  ├─ admin/
│  └─ user/
├─ tools/
│  ├─ docker/
│  └─ configs/
├─ data/
│  ├─ incoming/
│  └─ processed/
├─ .env.example
└─ README.md
```

---

## Prerequisites

- Python 3.11+
- Node.js 18+
- MongoDB 6.x
- Typesense 0.25+
- Ollama 0.3+
- Redis (optional)
- Docker (recommended)

---

## Quick Start — Linux/macOS

```bash
git clone https://github.com/<your-org>/ai-cms.git
cd ai-cms
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
cp .env.example .env
docker compose -f tools/docker/docker-compose.yml up -d
python backend/scripts/init_typesense.py
uvicorn backend.app:app --host 0.0.0.0 --port 8000 --workers 2
```

---

## Quick Start — Windows (PowerShell)

```powershell
git clone https://github.com/<your-org>/ai-cms.git
cd ai-cms
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r backendequirements.txt
Copy-Item .env.example .env
docker compose -f tools\docker\docker-compose.yml up -d
python backend\scripts\init_typesense.py
uvicorn backend.app:app --host 0.0.0.0 --port 8000
```

---

## License

MIT License © 2025 Ganesh Maharaj Kamatham
