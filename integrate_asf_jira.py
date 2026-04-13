#!/usr/bin/env python3
"""
Script to integrate ASF JIRA dataset into bug triage training data.
"""

import pandas as pd
import numpy as np
import os

def load_asf_jira_data(filepath):
    """Load and process the ASF JIRA dataset."""
    print(f"Loading ASF JIRA dataset from {filepath}...")
    df = pd.read_csv(filepath)
    print(f"Loaded {len(df)} records")
    print(f"Columns: {list(df.columns[:25])}\n")
    
    return df

def map_assignee_to_team(assignee):
    """
    Map individual assignees to teams.
    Group assignees into 3 main teams: frontend_team, backend_team, mobile_team
    """
    if pd.isna(assignee) or assignee == "":
        return "backend_team"  # default
    
    assignee_lower = str(assignee).lower()
    
    # Frontend team keywords
    frontend_keywords = ["ui", "css", "html", "frontend", "web", "javascript", "react", "vue", "angular"]
    
    # Mobile team keywords  
    mobile_keywords = ["mobile", "ios", "android", "app", "phone", "tablet"]
    
    # Check for keywords
    for keyword in frontend_keywords:
        if keyword in assignee_lower:
            return "frontend_team"
    
    for keyword in mobile_keywords:
        if keyword in assignee_lower:
            return "mobile_team"
    
    # Default to backend
    return "backend_team"

def normalize_priority(priority):
    """Normalize priority levels."""
    if pd.isna(priority) or priority == "":
        return "medium"
    
    priority_lower = str(priority).lower().strip()
    
    priority_map = {
        "blocker": "high",
        "critical": "high",
        "highest": "high",
        "high": "high",
        "major": "medium",
        "medium": "medium",
        "normal": "medium",
        "default": "medium",
        "minor": "low",
        "low": "low",
        "lowest": "low",
        "trivial": "low",
        "none": "low"
    }
    
    return priority_map.get(priority_lower, "medium")

def transform_asf_jira_to_format(df):
    """Transform ASF JIRA data to our bug report format."""
    print("Transforming ASF JIRA data to standard format...")
    
    transformed_data = []
    
    for idx, row in df.iterrows():
        # Skip rows without summary or description
        summary = str(row.get('Summary', '')).strip()
        description = str(row.get('Description', '')).strip()
        
        if not summary or len(summary) < 5:
            continue
        
        # Keep description reasonable length
        if description:
            description = description[:500]
        else:
            description = summary  # Use summary as description if missing
        
        # Map assignee to team
        assignee = row.get('Assignee', '')
        assigned_to = map_assignee_to_team(assignee)
        
        # Normalize priority
        priority = normalize_priority(row.get('Priority', ''))
        
        # Get issue type for reference
        issue_type = str(row.get('Issue Type', 'Bug')).strip()
        
        transformed_data.append({
            'title': summary,
            'description': description,
            'assigned_to': assigned_to,
            'priority': priority,
            'issue_type': issue_type,
            'source': 'asf_jira'
        })
    
    result_df = pd.DataFrame(transformed_data)
    print(f"Transformed {len(result_df)} records")
    print(f"Assignment distribution:\n{result_df['assigned_to'].value_counts()}")
    print(f"\nPriority distribution:\n{result_df['priority'].value_counts()}")
    
    return result_df

def combine_all_datasets():
    """Combine ASF JIRA, original, and synthetic data."""
    print("\n" + "="*60)
    print("COMBINING ALL DATASETS")
    print("="*60 + "\n")
    
    # Load ASF JIRA data
    asf_df = load_asf_jira_data(r'c:\Users\Abhishekh Kumar Jha\Downloads\ASF JIRA 2.csv')
    asf_transformed = transform_asf_jira_to_format(asf_df)
    asf_transformed = asf_transformed[['title', 'description', 'assigned_to', 'priority']]
    
    # Load current data
    print("\nLoading current training data...")
    current_df = pd.read_csv("data/bug_reports.csv")
    print(f"Current dataset: {len(current_df)} samples")
    
    # Load synthetic data if it exists
    synthetic_df = pd.DataFrame()
    if os.path.exists("data/enhanced_bug_reports.csv"):
        print("Loading synthetic data...")
        synthetic_df = pd.read_csv("data/enhanced_bug_reports.csv")
        print(f"Synthetic dataset: {len(synthetic_df)} samples")
        if 'source' in synthetic_df.columns:
            synthetic_df = synthetic_df[['title', 'description', 'assigned_to', 'priority']]
    
    # Combine all datasets
    print("\nCombining datasets...")
    all_dfs = [asf_transformed, current_df]
    if not synthetic_df.empty:
        all_dfs.append(synthetic_df)
    
    combined_df = pd.concat(all_dfs, ignore_index=True)
    
    # Remove duplicates
    combined_df = combined_df.drop_duplicates(subset=['title'], keep='first')
    
    # Shuffle
    combined_df = combined_df.sample(frac=1, random_state=42).reset_index(drop=True)
    
    print(f"\n" + "="*60)
    print(f"FINAL COMBINED DATASET: {len(combined_df)} samples")
    print("="*60)
    print(f"\nAssignment distribution:\n{combined_df['assigned_to'].value_counts()}")
    print(f"\nPriority distribution:\n{combined_df['priority'].value_counts()}")
    
    # Show sample
    print(f"\nSample records:")
    print(combined_df[['title', 'assigned_to', 'priority']].head(10))
    
    return combined_df

def save_dataset(df, filename="data/combined_bug_reports.csv"):
    """Save the combined dataset."""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    df.to_csv(filename, index=False)
    print(f"\nDataset saved to {filename}")

def main():
    # Combine all datasets
    combined_df = combine_all_datasets()
    
    # Save it
    save_dataset(combined_df, "data/combined_bug_reports.csv")
    
    print("\n" + "="*60)
    print("Next steps:")
    print("1. Retrain the model: python main.py train")
    print("2. Test the improved predictions: python test_api.py")
    print("="*60)

if __name__ == "__main__":
    main()