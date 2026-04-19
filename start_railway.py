#!/usr/bin/env python3
"""
Railway deployment script for Automated Bug Triage System.
Ensures database and model are ready before starting the server.
"""

import os
import sys
import subprocess

def setup_railway():
    """Setup application for Railway deployment."""
    
    print("🚀 Setting up Bug Triage System for Railway...")
    
    # Create necessary directories
    os.makedirs("model", exist_ok=True)
    os.makedirs("data", exist_ok=True)
    
    # Initialize database
    print("📊 Creating database tables...")
    try:
        subprocess.run([sys.executable, "main.py", "db"], check=True, capture_output=True)
        print("✅ Database created successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Database creation failed: {e}")
        return False
    
    # Train model if not exists
    model_path = "model/bug_triage_model.pkl"
    if not os.path.exists(model_path):
        print("🤖 Training ML model...")
        try:
            subprocess.run([sys.executable, "train_with_large_dataset.py"], check=True, capture_output=True)
            print("✅ Model trained successfully")
        except subprocess.CalledProcessError as e:
            print(f"❌ Model training failed: {e}")
            return False
    else:
        print("✅ Model already exists")
    
    # Start server
    print("🌐 Starting FastAPI server...")
    try:
        subprocess.run([sys.executable, "main.py", "run"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Server startup failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = setup_railway()
    sys.exit(0 if success else 1)
