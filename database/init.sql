-- RiskLens database schema
-- Applied automatically by the postgres container on first boot,
-- or manually with: psql -U postgres -d risklens -f database/init.sql

CREATE TYPE alert_severity AS ENUM ('low', 'medium', 'high', 'critical');

CREATE TABLE IF NOT EXISTS transactions (
    id SERIAL PRIMARY KEY,
    transaction_id VARCHAR(50) UNIQUE NOT NULL,
    amount FLOAT NOT NULL,
    timestamp TIMESTAMPTZ DEFAULT now(),
    card_number VARCHAR(20) NOT NULL,
    merchant_id VARCHAR(50) NOT NULL,
    merchant_category VARCHAR(50),
    location VARCHAR(100),
    is_fraud BOOLEAN DEFAULT FALSE,
    fraud_score FLOAT DEFAULT 0.0,
    is_flagged BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT now()
);
CREATE INDEX IF NOT EXISTS ix_transactions_transaction_id ON transactions (transaction_id);

CREATE TABLE IF NOT EXISTS alerts (
    id SERIAL PRIMARY KEY,
    transaction_id VARCHAR(50) NOT NULL,
    severity alert_severity NOT NULL,
    message TEXT NOT NULL,
    fraud_score FLOAT NOT NULL,
    is_resolved BOOLEAN DEFAULT FALSE,
    resolved_by VARCHAR(100),
    resolved_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT now()
);
CREATE INDEX IF NOT EXISTS ix_alerts_transaction_id ON alerts (transaction_id);

CREATE TABLE IF NOT EXISTS model_metrics (
    id SERIAL PRIMARY KEY,
    model_version VARCHAR(50) NOT NULL,
    precision_score FLOAT,
    recall_score FLOAT,
    f1_score FLOAT,
    auc_roc FLOAT,
    trained_at TIMESTAMPTZ DEFAULT now(),
    training_samples INTEGER,
    fraud_ratio FLOAT
);
