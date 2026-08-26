# RiskLens

A transaction fraud monitoring app: FastAPI backend running an Isolation
Forest model over a Postgres ledger, with a React frontend for logging
transactions and working the alert queue.

```
RiskLens/
├── backend/            FastAPI app, ML model, services
│   ├── app/
│   │   ├── api/        routes.py
│   │   ├── ml/         model.py (Isolation Forest)
│   │   ├── models/     SQLAlchemy models + Pydantic schemas
│   │   ├── services/   transaction / scoring / alert logic
│   │   ├── config.py
│   │   └── main.py     FastAPI entrypoint
│   ├── scripts/        generate_data.py, train_model.py
│   ├── data/            (creditcard.csv lands here)
│   └── requirements.txt
├── frontend/           React + Vite app
├── database/init.sql   Postgres schema
├── docker/              Dockerfiles
└── docker-compose.yml
```

## Run it locally with Docker (recommended)

```bash
docker-compose up --build
```

- Frontend: http://localhost:3000
- Backend docs: http://localhost:8000/docs

The Postgres container applies `database/init.sql` on first boot. The
backend doesn't ship a trained model by default, so train one once the
stack is up:

```bash
docker exec -it risklens-backend python scripts/train_model.py
```

This generates a synthetic dataset (if `data/creditcard.csv` isn't already
there) and trains the model into the shared `model_data` volume.

## Run it locally without Docker

You'll need Python 3.11+, Node 18+, and a Postgres instance (the compose
file's `postgres` service works fine on its own: `docker-compose up -d postgres`).

**Backend**

```bash
cd backend
python setup.py            # creates venv, installs deps, trains a starter model
cp .env.example .env       # adjust DATABASE_URL if your Postgres differs
source venv/bin/activate   # venv\Scripts\activate on Windows
uvicorn app.main:app --reload
```

**Frontend** (new terminal)

```bash
cd frontend
cp .env.example .env
npm install
npm run dev
```

Visit http://localhost:3000. It talks to the API at the URL in
`frontend/.env` (`VITE_API_URL`, default `http://localhost:8000/api/v1`).

## Deploying

The frontend and backend deploy separately.

**Frontend on Vercel**

1. Import the repo in Vercel and set the project root to `frontend/`.
2. Framework preset: Vite. Build command `npm run build`, output directory `dist`.
3. Add an environment variable `VITE_API_URL` pointing at your deployed API,
   e.g. `https://your-api.example.com/api/v1`.
4. Deploy. `frontend/vercel.json` handles client-side routing.

**Backend**

Vercel's serverless functions aren't a good fit for this API: the Isolation
Forest model and scikit-learn/pandas dependencies are heavier than the
platform's function size and cold-start budget expect, and the app holds a
long-lived DB connection pool. Deploy the backend to something built for a
persistent Python process instead, for example:

- **Render / Railway / Fly.io**: point them at `docker/Dockerfile.backend`
  with build context `backend/`, and provision a managed Postgres instance.
- **Your own Docker host**: run `docker-compose up -d postgres backend` and
  put a reverse proxy in front of port 8000.

Either way, set `DATABASE_URL` to your managed Postgres connection string
and `CORS_ORIGINS` to your Vercel frontend's URL so the browser can reach
the API.

## API

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

Full interactive docs live at `/docs` once the backend is running.

## Configuration

Backend (`backend/.env`, see `.env.example`):

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/risklens
MODEL_PATH=trained_models
FRAUD_THRESHOLD=0.7
CORS_ORIGINS=http://localhost:3000
```

Frontend (`frontend/.env`, see `.env.example`):

```env
VITE_API_URL=http://localhost:8000/api/v1
```

MIT
