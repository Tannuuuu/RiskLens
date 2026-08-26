"""Local (non-Docker) setup: creates a virtualenv, installs dependencies,
generates a sample dataset, and trains the initial model. Run from the
backend/ directory: python setup.py
"""
import os
import subprocess
import sys


def setup_project():
    print("Setting up RiskLens backend...")

    print("\n1. Creating virtual environment...")
    subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)

    if os.name == "nt":
        pip_path = os.path.join("venv", "Scripts", "pip.exe")
        python_path = os.path.join("venv", "Scripts", "python.exe")
    else:
        pip_path = os.path.join("venv", "bin", "pip")
        python_path = os.path.join("venv", "bin", "python")

    print("\n2. Installing dependencies...")
    subprocess.run([pip_path, "install", "-r", "requirements.txt"], check=True)

    print("\n3. Generating sample dataset and training the model...")
    subprocess.run([python_path, "scripts/train_model.py"], check=True)

    print("\nSetup complete.")
    print("\nNext steps:")
    print("  1. Start Postgres: docker-compose up -d postgres  (run from the project root)")
    print("  2. Copy .env.example to .env and adjust if needed")
    print("  3. Start the API: source venv/bin/activate && uvicorn app.main:app --reload")
    print("  4. In another terminal: cd ../frontend && npm install && npm run dev")


if __name__ == "__main__":
    setup_project()
