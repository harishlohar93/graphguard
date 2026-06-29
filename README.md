# GraphGuard — Social Graph Anomaly Detector

![GraphGuard Dashboard](https://img.shields.io/badge/status-live-brightgreen) ![Python](https://img.shields.io/badge/python-3.11-blue) ![Django](https://img.shields.io/badge/django-5.2-green) ![React](https://img.shields.io/badge/react-18-61dafb) ![Docker](https://img.shields.io/badge/docker-compose-2496ed)

> A full-stack ML-powered system that detects bot networks, fake accounts, and coordinated inauthentic behaviour in social graphs using Isolation Forest trained on NetworkX graph features.

**Live Demo:** [https://graphguard-git-main-harish-lohar.vercel.app](https://graphguard-git-main-harish-lohar.vercel.app)  
**Backend API:** [https://graphguard-y35d.onrender.com/api/health/](https://graphguard-y35d.onrender.com/api/health/)

---

## What it does

GraphGuard models a social network as a graph — accounts are nodes, follow relationships are edges. It extracts structural and behavioural features from this graph (PageRank, clustering coefficient, follow velocity, degree centrality) and trains an Isolation Forest model to score every account for anomalous behaviour. Accounts that score above 0.8 are flagged as bots, above 0.6 as suspects. The results are displayed in a real-time React dashboard with a D3.js force-directed graph where node colours encode the ML anomaly score.

---

## Key results

| Metric | Value |
|---|---|
| Total accounts monitored | 500 |
| Bot accounts detected | 27 |
| Suspect accounts detected | 28 |
| Average bot anomaly score | 0.83 |
| Average normal anomaly score | 0.19 |
| Score separation gap | 4.3× |

---

## Architecture

```
Data source (synthetic / Kaggle)
        ↓
Neo4j — social graph database (Account nodes + FOLLOWS edges)
        ↓
NetworkX — loads graph into memory, computes 11 features per account
        ↓
Isolation Forest — scores every account 0.0 → 1.0
        ↓
PostgreSQL — stores Alert records (score, label, status)
        ↓
Django REST API — serves JSON to React
        ↓
Django Channels — WebSocket pushes live alerts
        ↓
React + D3.js — renders force graph + alert panel
```

---

## Tech stack

### Backend
| Technology | Purpose |
|---|---|
| Django 5.2 | Web framework, ORM, admin panel |
| Django REST Framework | REST API endpoints, serializers, ViewSets |
| Django Channels | WebSocket server for live alerts |
| Celery | Async background task queue |
| Daphne | ASGI server (HTTP + WebSocket) |
| PostgreSQL | Relational store — alerts, accounts, audit log |
| Redis | Celery broker + Django Channels layer |

### Graph & ML
| Technology | Purpose |
|---|---|
| Neo4j | Graph database — accounts and relationships |
| NetworkX | In-memory graph analysis, feature extraction |
| scikit-learn | Isolation Forest anomaly detection model |
| pandas | Feature engineering, DataFrame manipulation |
| numpy | Array math |
| joblib | Model serialisation (save/load .pkl) |

### Frontend
| Technology | Purpose |
|---|---|
| React 18 | UI components, state management |
| Vite | Build tool and dev server |
| D3.js | Force-directed graph visualisation |
| React Query | API data fetching and caching |
| Tailwind CSS | Utility-first styling |
| Axios | HTTP client for Django API |

### DevOps
| Technology | Purpose |
|---|---|
| Docker | Container for each service |
| Docker Compose | One-command local development |
| GitHub | Version control with conventional commits |
| Render | Backend deployment (free tier) |
| Vercel | Frontend deployment (free tier) |

---

## Project structure

```
graphguard/
├── backend/
│   ├── api/
│   │   ├── management/commands/
│   │   │   ├── seed_graph.py         # seed Neo4j with fake accounts
│   │   │   ├── seed_postgres.py      # seed PostgreSQL directly
│   │   │   ├── sync_accounts.py      # sync Neo4j → PostgreSQL
│   │   │   ├── train_model.py        # extract features + train Isolation Forest
│   │   │   ├── extract_features.py   # NetworkX feature extraction
│   │   │   └── storescore_in_db.py   # score all accounts + save alerts
│   │   ├── models.py                 # Account, Alert, Cluster, AuditLog
│   │   ├── views.py                  # API endpoints + WebSocket
│   │   ├── serializers.py            # DRF serializers
│   │   ├── urls.py                   # URL routing
│   │   ├── neo4j_service.py          # Neo4j connection singleton
│   │   ├── feature_extractor.py      # NetworkX graph feature extraction
│   │   ├── anomaly_detector.py       # Isolation Forest wrapper
│   │   ├── scoring_service.py        # single account + bulk scoring
│   │   ├── consumers.py              # Django Channels WebSocket consumer
│   │   └── routing.py                # WebSocket URL routing
│   ├── graphguard/
│   │   ├── settings.py               # Django settings
│   │   ├── settings_prod.py          # Production settings
│   │   ├── urls.py                   # Project URL config
│   │   ├── asgi.py                   # ASGI config (HTTP + WebSocket)
│   │   └── celery.py                 # Celery app config
│   ├── models/
│   │   └── anomaly_model.pkl         # trained Isolation Forest model
│   ├── requirements.txt
│   ├── Dockerfile
│   └── build.sh                      # Render build script
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   │   ├── client.js             # Axios base config
│   │   │   └── endpoints.js          # API function exports
│   │   ├── components/
│   │   │   ├── Layout.jsx            # App shell (sidebar + topbar)
│   │   │   ├── Sidebar.jsx           # Navigation
│   │   │   ├── Topbar.jsx            # Header with live indicator
│   │   │   ├── StatCard.jsx          # Metric cards
│   │   │   ├── GraphPanel.jsx        # D3.js force graph
│   │   │   └── AlertList.jsx         # Live alert feed
│   │   ├── pages/
│   │   │   └── Dashboard.jsx         # Main dashboard page
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── tailwind.config.js
│   └── vite.config.js
├── ml/                               # ML experiments (future)
├── docker-compose.yml
├── .gitignore
└── README.md
```

---

## API endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/health/` | Health check |
| GET | `/api/accounts/` | List all accounts |
| GET | `/api/alerts/` | List all alerts (filterable) |
| GET | `/api/alerts/?label=bot` | Filter by label |
| GET | `/api/alerts/?status=pending` | Filter by status |
| GET | `/api/alerts/?ordering=-score` | Sort by score |
| GET | `/api/clusters/` | List clusters |
| GET | `/api/graph/` | Graph nodes + edges for D3 |
| POST | `/api/score/<account_id>/` | Score a single account |
| WS | `ws://…/ws/alerts/` | Live alert stream |

---

## ML pipeline

### Feature extraction (NetworkX)

Each account gets 11 features computed from the graph structure:

| Feature | What it captures |
|---|---|
| `degree_centrality` | Fraction of all possible connections |
| `in_degree_centrality` | Incoming connections (followers) |
| `pagerank` | Influence score in the network |
| `clustering_coefficient` | How tightly connected neighbours are |
| `follower_count` | Raw follower count |
| `following_count` | Raw following count |
| `follow_velocity` | Following count ÷ account age in days |
| `created_days_ago` | Account age |

### Bot detection pattern

Bots in the seed data have these characteristics:
- Account age: 1–10 days (very new)
- Follower count: 2,000–8,000 (inflated)
- Follow velocity: 500–5,000 follows/day (extreme)
- Clustering coefficient: 0.95+ (tight bot ring)
- PageRank: low (closed ring, no real influence)

### Model

```python
IsolationForest(
    n_estimators=100,
    contamination=0.1,   # expect ~10% anomalies
    random_state=42
)
```

Scores are normalised to [0.0, 1.0]:
- `score > 0.8` → **bot**
- `score > 0.6` → **suspect**
- `score ≤ 0.6` → **normal**

---

## Local development

### Prerequisites
- Docker Desktop
- Git
- Node.js 20+

### Setup

```bash
# Clone the repo
git clone https://github.com/harishlohar93/graphguard.git
cd graphguard

# Start all backend services
docker-compose up -d

# Verify everything is running
docker-compose ps

# Seed the graph data
docker-compose exec django python manage.py seed_graph

# Sync accounts to PostgreSQL
docker-compose exec django python manage.py sync_accounts

# Train the ML model
docker-compose exec django python manage.py train_model

# Score all accounts and save alerts
docker-compose exec django python manage.py storescore_in_db

# Create admin user
docker-compose exec django python manage.py createsuperuser
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Open [http://localhost:5173](http://localhost:5173)

### API docs (DRF Browsable API)

Open [http://localhost:8000/api/](http://localhost:8000/api/)

### Django Admin

Open [http://localhost:8000/admin/](http://localhost:8000/admin/)

---

## Environment variables

Create `backend/.env`:

```env
SECRET_KEY=your-django-secret-key-here
DEBUG=True
DATABASE_URL=postgres://USER:PASSWORD@HOST:5432/DB_NAME
REDIS_URL=redis://localhost:6379/0
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your-neo4j-password
ALLOWED_HOSTS=localhost,127.0.0.1
```

---

## Deployment

| Service | Platform | URL |
|---|---|---|
| Django backend | Render (free) | https://graphguard-y35d.onrender.com |
| React frontend | Vercel (free) | https://graphguard-git-main-harish-lohar.vercel.app |
| PostgreSQL | Render PostgreSQL (free) | managed |
| Redis | Upstash (free) | managed |

---

## Dashboard features

- **Force-directed graph** — 500 nodes rendered with D3.js, colour-coded by ML anomaly score (green = normal, orange = suspect, red = bot). Zoom and drag supported.
- **Live alert panel** — real-time scored account feed via Django Channels WebSocket
- **Stat cards** — total accounts, flagged count, cluster count, reviewed count — all from live API
- **Alert filtering** — filter by label (bot/suspect/normal) and status
- **Dark theme** — professional dark UI built with Tailwind CSS

---

## What I learned

- Graph databases (Neo4j, Cypher queries) and how graph structure reveals patterns invisible in tabular data
- Unsupervised ML anomaly detection — Isolation Forest, feature engineering on graph data
- Django Channels + ASGI for real-time WebSocket communication
- D3.js force simulation integrated inside React via useRef + useEffect
- Full Docker Compose orchestration of 5 services
- Production deployment with Render + Vercel

---

## Author

**Harish Lohar**  
B.Tech — Artificial Intelligence & Robotics, MITS Gwalior  
[LinkedIn](https://www.linkedin.com/in/harishlohar) | [GitHub](https://github.com/harishlohar93)
