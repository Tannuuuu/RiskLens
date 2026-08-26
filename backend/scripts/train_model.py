"""Trains the Isolation Forest fraud model on data/creditcard.csv and saves
it to trained_models/. Generates sample data first if none exists.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.ml.model import FraudModel  # noqa: E402


def main():
    data_path = "data/creditcard.csv"

    if not os.path.exists(data_path):
        print("No dataset found, generating a synthetic one...")
        from scripts.generate_data import generate_sample_data

        os.makedirs("data", exist_ok=True)
        generate_sample_data().to_csv(data_path, index=False)

    model = FraudModel(model_path="trained_models")
    metrics = model.train(data_path)

    print("\nTraining complete.")
    print(metrics)


if __name__ == "__main__":
    main()
