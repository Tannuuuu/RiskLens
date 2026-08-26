"""Generates a synthetic credit-card-style transaction dataset for local
development and demos. Shaped like the classic Kaggle "creditcard.csv"
(Time, V1..V28, Amount, Class) so it drops straight into FraudModel.train().
"""
import numpy as np
import pandas as pd


def generate_sample_data(n_samples: int = 20000, fraud_ratio: float = 0.015, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)

    n_fraud = max(1, int(n_samples * fraud_ratio))
    n_normal = n_samples - n_fraud

    # Normal transactions: tight cluster of PCA-like features around 0
    normal_features = rng.normal(loc=0.0, scale=1.0, size=(n_normal, 28))
    normal_amount = np.round(np.abs(rng.normal(loc=60, scale=45, size=n_normal)), 2)

    # Fraudulent transactions: shifted / higher-variance features, so the
    # anomaly detector has something real to key on
    fraud_features = rng.normal(loc=0.0, scale=3.2, size=(n_fraud, 28))
    fraud_features[:, :6] += rng.normal(loc=4.0, scale=1.5, size=(n_fraud, 6))
    fraud_amount = np.round(np.abs(rng.normal(loc=340, scale=260, size=n_fraud)), 2)

    features = np.vstack([normal_features, fraud_features])
    amounts = np.concatenate([normal_amount, fraud_amount])
    labels = np.concatenate([np.zeros(n_normal, dtype=int), np.ones(n_fraud, dtype=int)])
    time = np.sort(rng.integers(0, 172800, size=n_samples))  # 48h of seconds

    columns = {f"V{i}": features[:, i - 1] for i in range(1, 29)}
    df = pd.DataFrame(columns)
    df.insert(0, "Time", time)
    df["Amount"] = amounts
    df["Class"] = labels

    # Shuffle rows so fraud isn't all at the end
    df = df.sample(frac=1.0, random_state=seed).reset_index(drop=True)
    return df


if __name__ == "__main__":
    df = generate_sample_data()
    df.to_csv("data/creditcard.csv", index=False)
    print(f"Generated {len(df)} rows ({df['Class'].sum()} fraud) -> data/creditcard.csv")
