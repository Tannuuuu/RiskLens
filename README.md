# RiskLens

RiskLens is a real-time transaction fraud detection system. It scores every
incoming transaction with an Isolation Forest model, raises alerts on
anything that crosses the fraud threshold, and gives you a ledger-style
dashboard to review activity and work the alert queue.

## Features

- **Real-time scoring**: every transaction is run through a trained
  Isolation Forest model the moment it's logged.
- **Alert queue**: flagged transactions generate severity-ranked alerts
  that can be reviewed and resolved.
- **Model training dashboard**: retrain the model against a dataset on
  disk and track precision, recall, F1, and AUC-ROC across versions.
- **REST API**: a FastAPI backend with interactive OpenAPI docs.
- **React frontend**: a dashboard for transactions, alerts, and model
  metrics.

## Architecture

```
┌────────────────────┐      ┌────────────────────┐      ┌────────────────────┐
│   React Frontend    │ ───▶ │   FastAPI Backend   │ ───▶ │  PostgreSQL Database │
│  (dashboard / UI)   │      │  + Isolation Forest │      │  transactions, alerts │
└────────────────────┘      └────────────────────┘      └────────────────────┘
```

## Project Structure

```
RiskLens/
├── backend/
│   ├── app/
│   │   ├── api/           # API routes
│   │   ├── ml/            # Isolation Forest model
│   │   ├── models/        # SQLAlchemy models + Pydantic schemas
│   │   ├── services/      # Transaction, scoring, and alert logic
│   │   ├── config.py
│   │   └── main.py
│   ├── scripts/           # Dataset generation and training scripts
│   ├── data/               # Dataset storage
│   └── requirements.txt
├── frontend/
│   └── src/
│       ├── components/
│       ├── pages/
│       └── services/
├── database/
│   └── init.sql            # Postgres schema
├── docker/
│   ├── Dockerfile.backend
│   └── Dockerfile.frontend
└── docker-compose.yml
```

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/) (bundled with
  Docker Desktop)

## Getting Started

Clone or unzip the project, then from the project root:

```bash
docker-compose up --build
```

This starts three services:

| Service | URL |
|---|---|
| Frontend | http://localhost:3000 |
| Backend API | http://localhost:8000 |
| API docs (Swagger) | http://localhost:8000/docs |
| Postgres | localhost:5432 |

The Postgres container applies `database/init.sql` automatically on its
first boot, so the schema is ready as soon as it's healthy.

## Training the Model

The backend doesn't ship with a pre-trained model. Train one once the
stack is running:

```bash
docker exec -it risklens-backend python scripts/train_model.py
```

This generates a synthetic dataset at `data/creditcard.csv` (if one isn't
already there) and trains the Isolation Forest model into the shared
`model_data` volume. You can retrain at any point the same way, or from
the **Model** page in the frontend.

## Stopping the Project

```bash
docker-compose down
```

Add `-v` to also remove the Postgres and model data volumes:

```bash
docker-compose down -v
```

## API Reference

| Method | Path | Description |
|---|---|---|
| POST | `/api/v1/transactions` | Log and score a single transaction |
| POST | `/api/v1/transactions/batch` | Log and score multiple transactions |
| GET | `/api/v1/transactions` | List transactions |
| GET | `/api/v1/transactions/{id}` | Get one transaction |
| GET | `/api/v1/alerts` | List alerts (filter by `severity`, `resolved`) |
| PUT | `/api/v1/alerts/{id}/resolve` | Resolve an alert |
| GET | `/api/v1/dashboard/stats` | Summary stats for the dashboard |
| POST | `/api/v1/model/train` | Retrain the model against a CSV on disk |
| GET | `/api/v1/model/metrics` | Training history |

Full interactive docs are available at `/docs` once the backend is
running.

## Configuration

Environment variables are set in `docker-compose.yml` for the Docker
setup. The defaults:

```env
DATABASE_URL=postgresql://postgres:postgres@postgres:5432/risklens
MODEL_PATH=/app/trained_models
FRAUD_THRESHOLD=0.7
CORS_ORIGINS=http://localhost:3000
```

## License

MIT
