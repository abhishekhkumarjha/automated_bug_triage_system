#!/usr/bin/env python3
"""
Main entry point for the Automated Bug Triage System.
This script provides commands to train the model, run the API server, and manage the system.
"""

import argparse
import subprocess
import sys
import os

def train_model():
    """
    Train the machine learning model.
    """
    print("Training the bug triage model...")
    try:
        subprocess.run([sys.executable, "model/bug_triage_model.py"], check=True)
        print("Model trained successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Training failed: {e}")
        sys.exit(1)

def run_server():
    """
    Run the FastAPI server.
    """
    print("Starting the FastAPI server...")
    try:
        host = os.getenv("HOST", "0.0.0.0")
        port = os.getenv("PORT", "8000")
        reload_enabled = os.getenv("RELOAD", "false").lower() == "true"
        command = [
            sys.executable,
            "-m",
            "uvicorn",
            "app.main:app",
            "--host",
            host,
            "--port",
            port,
        ]
        if reload_enabled:
            command.append("--reload")
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Server failed to start: {e}")
        sys.exit(1)

def create_database():
    """
    Create the database tables.
    """
    print("Creating database tables...")
    try:
        subprocess.run([sys.executable, "app/database.py"], check=True)
        print("Database tables created successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Database creation failed: {e}")
        sys.exit(1)

def install_dependencies():
    """
    Install Python dependencies.
    """
    print("Installing dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("Dependencies installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Installation failed: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Automated Bug Triage System")
    parser.add_argument("command", choices=["install", "train", "run", "db"], help="Command to execute")

    args = parser.parse_args()

    if args.command == "install":
        install_dependencies()
    elif args.command == "train":
        train_model()
    elif args.command == "run":
        run_server()
    elif args.command == "db":
        create_database()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
