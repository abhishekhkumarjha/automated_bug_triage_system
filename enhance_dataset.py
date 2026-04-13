#!/usr/bin/env python3
"""
Enhanced dataset integration script for bug triage system.
This script can integrate multiple data sources to expand training data.
"""

import pandas as pd
import numpy as np
import os
import requests
from pathlib import Path
import json

def load_current_data():
    """Load the current training data."""
    try:
        df = pd.read_csv("data/bug_reports.csv")
        print(f"Loaded current dataset: {len(df)} samples")
        return df
    except Exception as e:
        print(f"Error loading current data: {e}")
        return pd.DataFrame()

def generate_synthetic_data(num_samples=100):
    """Generate synthetic bug reports to augment training data."""
    print(f"Generating {num_samples} synthetic bug reports...")

    # Templates for different types of bugs
    frontend_issues = [
        "Button not clickable on {page}",
        "Text alignment broken in {component}",
        "CSS styling not loading in {browser}",
        "Responsive design issue on {device}",
        "Form validation not working for {field}",
        "Navigation menu not displaying correctly",
        "Image not loading on {page}",
        "Color scheme inconsistent across pages",
        "Font size too small on mobile devices",
        "Hover effects not working on {element}"
    ]

    backend_issues = [
        "Database connection timeout during {operation}",
        "API endpoint returning {status_code} error",
        "Server response time over {time} seconds",
        "Authentication failing for {user_type}",
        "Data not saving to database",
        "File upload failing with large files",
        "Email notifications not sending",
        "Cache invalidation not working",
        "Background job processing stuck",
        "Memory leak in {component}"
    ]

    mobile_issues = [
        "App crashing on {device} when {action}",
        "Push notifications not received",
        "Offline mode not working properly",
        "GPS location accuracy issues",
        "Battery drain faster than expected",
        "App not compatible with {os_version}",
        "In-app purchase failing",
        "Screen rotation causing layout issues",
        "Touch gestures not responding",
        "Network connectivity problems"
    ]

    # Fillers for templates
    pages = ["homepage", "login page", "dashboard", "profile page", "settings"]
    components = ["header", "footer", "sidebar", "modal", "dropdown"]
    browsers = ["Chrome", "Firefox", "Safari", "Edge"]
    devices = ["iPhone", "Android phone", "tablet", "desktop"]
    fields = ["email", "password", "username", "phone number"]
    operations = ["login", "registration", "checkout", "search"]
    status_codes = ["500", "404", "403", "502"]
    times = ["5", "10", "15", "30"]
    user_types = ["admin users", "regular users", "new users"]
    actions = ["opening", "closing", "scrolling", "tapping"]
    os_versions = ["iOS 17", "Android 13", "iOS 16", "Android 12"]
    elements = ["buttons", "links", "images", "icons"]

    # Priority levels
    priorities = ["low", "medium", "high"]
    priority_weights = [0.3, 0.5, 0.2]  # More medium priority issues

    # Team assignments
    teams = ["frontend_team", "backend_team", "mobile_team"]
    team_weights = [0.35, 0.45, 0.2]  # Backend gets more issues

    synthetic_data = []

    for _ in range(num_samples):
        team = np.random.choice(teams, p=team_weights)
        priority = np.random.choice(priorities, p=priority_weights)

        if team == "frontend_team":
            template = np.random.choice(frontend_issues)
            title = template.format(
                page=np.random.choice(pages),
                component=np.random.choice(components),
                browser=np.random.choice(browsers),
                device=np.random.choice(devices),
                field=np.random.choice(fields),
                element=np.random.choice(elements)
            )
            description = f"The {title.lower()}. This is affecting user experience and needs immediate attention."

        elif team == "backend_team":
            template = np.random.choice(backend_issues)
            title = template.format(
                operation=np.random.choice(operations),
                status_code=np.random.choice(status_codes),
                time=np.random.choice(times),
                user_type=np.random.choice(user_types),
                component=np.random.choice(components)
            )
            description = f"Users are experiencing {title.lower()}. This is impacting system reliability."

        else:  # mobile_team
            template = np.random.choice(mobile_issues)
            title = template.format(
                device=np.random.choice(devices),
                action=np.random.choice(actions),
                os_version=np.random.choice(os_versions)
            )
            description = f"Mobile users report that {title.lower()}. This affects app usability."

        synthetic_data.append({
            "title": title,
            "description": description,
            "assigned_to": team,
            "priority": priority
        })

    return pd.DataFrame(synthetic_data)

def try_load_github_issues():
    """Attempt to load GitHub issues dataset."""
    try:
        from datasets import load_dataset
        print("Attempting to load GitHub issues dataset...")
        # This requires authentication for gated datasets
        dataset = load_dataset("bigcode/the-stack-github-issues", split="train", use_auth_token=True)
        print(f"Successfully loaded {len(dataset)} GitHub issues")

        # Convert to our format
        issues_data = []
        for item in dataset:
            # Try to extract assignment and priority from labels
            labels = item.get("labels", [])
            assigned_to = "backend_team"  # default
            priority = "medium"  # default

            # Simple heuristics based on labels
            if any(label.lower() in ["frontend", "ui", "css", "html"] for label in labels):
                assigned_to = "frontend_team"
            elif any(label.lower() in ["mobile", "ios", "android"] for label in labels):
                assigned_to = "mobile_team"

            if any(label.lower() in ["critical", "urgent", "p0"] for label in labels):
                priority = "high"
            elif any(label.lower() in ["low", "minor", "p3"] for label in labels):
                priority = "low"

            issues_data.append({
                "title": item.get("title", ""),
                "description": item.get("body", "")[:500],  # Truncate long descriptions
                "assigned_to": assigned_to,
                "priority": priority
            })

        return pd.DataFrame(issues_data)

    except Exception as e:
        print(f"Could not load GitHub issues dataset: {e}")
        print("Note: This dataset requires HuggingFace authentication")
        return pd.DataFrame()

def download_eclipse_bugs():
    """Download Eclipse bug reports dataset if available."""
    try:
        print("Attempting to download Eclipse bug reports...")
        # Eclipse bug reports are available from various sources
        # This is a simplified example - in practice you'd need to find a good source

        # For now, return empty - this would need actual implementation
        print("Eclipse dataset integration not implemented yet")
        return pd.DataFrame()

    except Exception as e:
        print(f"Error downloading Eclipse bugs: {e}")
        return pd.DataFrame()

def combine_datasets():
    """Combine all available datasets."""
    print("Combining datasets for enhanced training...")

    # Load current data
    current_df = load_current_data()

    # Generate synthetic data
    synthetic_df = generate_synthetic_data(200)  # Generate 200 synthetic samples

    # Try to load external datasets
    github_df = try_load_github_issues()
    eclipse_df = download_eclipse_bugs()

    # Combine all datasets
    combined_df = pd.concat([current_df, synthetic_df, github_df, eclipse_df], ignore_index=True)

    # Remove duplicates based on title
    combined_df = combined_df.drop_duplicates(subset=['title'], keep='first')

    # Shuffle the data
    combined_df = combined_df.sample(frac=1, random_state=42).reset_index(drop=True)

    print(f"Combined dataset: {len(combined_df)} samples")
    print(f"Distribution by team:\n{combined_df['assigned_to'].value_counts()}")
    print(f"Distribution by priority:\n{combined_df['priority'].value_counts()}")

    return combined_df

def save_enhanced_dataset(df, filename="data/enhanced_bug_reports.csv"):
    """Save the enhanced dataset."""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    df.to_csv(filename, index=False)
    print(f"Enhanced dataset saved to {filename}")

def main():
    print("Bug Triage Dataset Enhancement Tool")
    print("=" * 40)

    # Combine all available data sources
    enhanced_df = combine_datasets()

    # Save the enhanced dataset
    save_enhanced_dataset(enhanced_df)

    # Show sample of enhanced data
    print("\nSample of enhanced dataset:")
    print(enhanced_df.head(10))

    print(f"\nNext steps:")
    print("1. Review the enhanced dataset for quality")
    print("2. Retrain the model with: python main.py train")
    print("3. Test the improved predictions")

if __name__ == "__main__":
    main()