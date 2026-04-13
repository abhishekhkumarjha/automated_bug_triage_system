#!/usr/bin/env python3
"""
Script to explore and potentially integrate external datasets for bug triage training.
"""

import pandas as pd
from datasets import load_dataset
import os

def explore_github_issues():
    """Explore the GitHub issues dataset from The Stack."""
    print("Loading GitHub issues dataset...")
    try:
        dataset = load_dataset("bigcode/the-stack-github-issues", split="train")
        print(f"Dataset size: {len(dataset)}")
        print(f"Columns: {dataset.column_names}")

        # Show a few examples
        for i in range(min(5, len(dataset))):
            item = dataset[i]
            print(f"\nExample {i+1}:")
            print(f"Title: {item.get('title', 'N/A')}")
            print(f"Body: {item.get('body', 'N/A')[:200]}...")
            print(f"Labels: {item.get('labels', [])}")
            print(f"State: {item.get('state', 'N/A')}")

        return dataset
    except Exception as e:
        print(f"Error loading GitHub issues dataset: {e}")
        return None

def explore_buganizer():
    """Explore the Google Buganizer dataset."""
    print("\nLoading Buganizer dataset...")
    try:
        dataset = load_dataset("google/buganizer-public", split="train")
        print(f"Dataset size: {len(dataset)}")
        print(f"Columns: {dataset.column_names}")

        # Show a few examples
        for i in range(min(5, len(dataset))):
            item = dataset[i]
            print(f"\nExample {i+1}:")
            print(f"Title: {item.get('title', 'N/A')}")
            print(f"Description: {item.get('description', 'N/A')[:200]}...")
            print(f"Priority: {item.get('priority', 'N/A')}")
            print(f"Status: {item.get('status', 'N/A')}")
            print(f"Assignee: {item.get('assignee', 'N/A')}")

        return dataset
    except Exception as e:
        print(f"Error loading Buganizer dataset: {e}")
        return None

def explore_stackoverflow():
    """Explore the Stack Overflow corpus."""
    print("\nLoading Stack Overflow corpus...")
    try:
        # This might be a GitHub repo, not HuggingFace dataset
        # Let's try to see if it's available as a dataset
        try:
            dataset = load_dataset("lukovnikov/stackoverflow-corpus")
            print(f"Dataset size: {len(dataset)}")
            print(f"Columns: {dataset.column_names}")

            # Show a few examples
            for i in range(min(3, len(dataset))):
                item = dataset[i]
                print(f"\nExample {i+1}:")
                print(f"Title: {item.get('title', 'N/A')}")
                print(f"Body: {item.get('body', 'N/A')[:200]}...")
                print(f"Tags: {item.get('tags', [])}")

            return dataset
        except:
            print("Stack Overflow corpus not available as HuggingFace dataset.")
            print("You may need to download it manually from https://github.com/lukovnikov/stackoverflow-corpus")
            return None
    except Exception as e:
        print(f"Error with Stack Overflow dataset: {e}")
        return None

def analyze_current_data():
    """Analyze the current training data."""
    print("\nAnalyzing current training data...")
    try:
        df = pd.read_csv("data/bug_reports.csv")
        print(f"Current dataset size: {len(df)}")
        print(f"Columns: {list(df.columns)}")
        print(f"Assigned to distribution:\n{df['assigned_to'].value_counts()}")
        print(f"Priority distribution:\n{df['priority'].value_counts()}")
        return df
    except Exception as e:
        print(f"Error reading current data: {e}")
        return None

def main():
    print("Exploring external datasets for bug triage enhancement...")

    # Analyze current data
    current_df = analyze_current_data()

    # Explore external datasets
    github_dataset = explore_github_issues()
    buganizer_dataset = explore_buganizer()
    so_dataset = explore_stackoverflow()

    print("\n" + "="*50)
    print("SUMMARY:")
    print("="*50)

    if github_dataset:
        print(f"GitHub Issues: {len(github_dataset)} samples available")
        print("Potential for extracting bug reports with labels indicating assignment/priority")

    if buganizer_dataset:
        print(f"Buganizer: {len(buganizer_dataset)} samples available")
        print("Structured bug data with priority and assignee information")

    if so_dataset:
        print(f"Stack Overflow: {len(so_dataset)} samples available")
        print("Q&A data that could be used for additional context")

    if current_df is not None:
        print(f"Current training data: {len(current_df)} samples")
        print("These external datasets could significantly expand training data")

if __name__ == "__main__":
    main()