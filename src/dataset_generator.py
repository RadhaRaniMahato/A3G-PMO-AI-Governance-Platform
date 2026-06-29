import pandas as pd
from src.database import get_analysis_history


def generate_training_dataset():
    rows = get_analysis_history()

    columns = [
        "timestamp", "owner", "repo",
        "stars", "forks", "watchers", "repo_open_issues",
        "open_issues", "bugs", "security_issues", "open_prs",
        "recent_commits", "releases", "contributors",
        "repo_age_days", "days_since_last_push",
        "risk_score", "risk_level",
        "compliance_score", "compliance_status",
        "health_score", "health_status"
    ]

    df = pd.DataFrame(rows)

    if df.empty:
        return None

    df.columns = columns
    df.to_csv("data/governance_training_dataset.csv", index=False)

    return df