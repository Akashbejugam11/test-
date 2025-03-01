import git
import pandas as pd
import os
from datetime import datetime

# ✅ Update this path to match your actual local GitHub repository location
REPO_PATH = "/Users/akshithabejugam/Desktop/test-"  # Your local repo path
FILE_NAME = "task_dataset.csv"  # Dataset filename

# Ensure the repository path exists
if not os.path.exists(REPO_PATH):
    raise FileNotFoundError(f"Repository path '{REPO_PATH}' does not exist. Check your local path.")

def update_dataset():
    """Updates the dataset by adding 100 new rows daily."""
    file_path = os.path.join(REPO_PATH, FILE_NAME)

    # Load existing dataset or create a new one
    if os.path.exists(file_path):
        df_existing = pd.read_csv(file_path)
    else:
        df_existing = pd.DataFrame(columns=["TicketID", "SystemName", "IssueType", "Timestamp"])

    # Generate 100 new rows
    new_data = pd.DataFrame({
        "TicketID": ["TCKT" + str(i) for i in range(len(df_existing), len(df_existing) + 100)],
        "SystemName": ["SystemX"] * 100,
        "IssueType": ["Bug"] * 100,
        "Timestamp": [pd.Timestamp.now()] * 100
    })

    # Append new data
    df_updated = pd.concat([df_existing, new_data], ignore_index=True)

    # Save updated dataset
    df_updated.to_csv(file_path, index=False)
    print(f"✅ Dataset updated. Total rows: {len(df_updated)}")

    return file_path

def git_push():
    """Push the updated dataset to GitHub."""
    try:
        repo = git.Repo(REPO_PATH)

        # ✅ Ensure we are on the correct branch ('main')
        repo.git.checkout("main")  

        repo.git.add(FILE_NAME)
        repo.git.commit("-m", f"Update dataset on {datetime.now().strftime('%Y-%m-%d')}")
        repo.git.push("origin", "main")  # Ensure we push to 'main'
        
        print("🚀 Dataset pushed to GitHub successfully!")
    except Exception as e:
        print(f"❌ Git push failed: {e}")

# Run update process
updated_file = update_dataset()
git_push()
