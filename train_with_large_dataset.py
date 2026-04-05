#!/usr/bin/env python3
"""
Script to train the bug triage model with large datasets.
"""

import os
import sys
import pandas as pd
from model.bug_triage_model import BugTriageModel

def main():
    print("Training model with large datasets...")
    
    model = BugTriageModel()
    
    # Use the large archive datasets
    archive_path = os.path.join(os.path.dirname(__file__), "data", "_archive_inspect")
    
    # Load assignment data (fix_train.csv has fixing time info)
    fix_train_path = os.path.join(archive_path, "fix_train.csv")
    # Load priority data (sev_train.csv has severity info)  
    sev_train_path = os.path.join(archive_path, "sev_train.csv")
    
    try:
        print("Loading assignment dataset...")
        fix_df = pd.read_csv(fix_train_path)
        print(f"Loaded {len(fix_df)} assignment records")
        
        print("Loading priority dataset...")
        sev_df = pd.read_csv(sev_train_path)
        print(f"Loaded {len(sev_df)} priority records")
        
        # Prepare assignment dataframe
        assignment_df = pd.DataFrame({
            'title': fix_df['Description'].str.slice(0, 120).fillna(""),
            'description': fix_df['Description'].fillna(""),
            'assigned_to': fix_df['Label'].fillna("unknown")
        })
        
        # Prepare priority dataframe  
        priority_df = pd.DataFrame({
            'title': sev_df['Description'].str.slice(0, 120).fillna(""),
            'description': sev_df['Description'].fillna(""),
            'priority': sev_df['Label'].fillna("medium")
        })
        
        print(f"Prepared assignment dataset: {len(assignment_df)} records")
        print(f"Prepared priority dataset: {len(priority_df)} records")
        
        # Train the model
        print("Starting model training...")
        model.train_from_frames(assignment_df, priority_df)
        
        # Save the model
        model_path = os.path.join(os.path.dirname(__file__), "model", "bug_triage_model.pkl")
        model.save_model(model_path)
        
        print(f"Model trained and saved successfully to {model_path}")
        print("Model is now ready with much larger training dataset!")
        
    except Exception as e:
        print(f"Error during training: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
