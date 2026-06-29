import os
import numpy as np
import pandas as pd


def calculate_risk_level(score):
    if score < 120:
        return "Low"
    elif score < 250:
        return "Medium"
    return "High"


def create_synthetic_ml_dataset(n=1000):
    os.makedirs("data", exist_ok=True)

    np.random.seed(42)

    rows = []

    for _ in range(n):
        open_issues = np.random.randint(0, 120)
        bugs = np.random.randint(0, 25)
        security_issues = np.random.randint(0, 8)
        open_prs = np.random.randint(0, 80)
        recent_commits = np.random.randint(0, 50)

        risk_score = (
            open_issues * 1.2
            + bugs * 6
            + security_issues * 18
            + open_prs * 1.5
            - recent_commits * 1.2
        )

        risk_score = max(risk_score, 0)

        rows.append({
            "open_issues": open_issues,
            "bugs": bugs,
            "security_issues": security_issues,
            "open_prs": open_prs,
            "recent_commits": recent_commits,
            "risk_score": risk_score,
            "risk_level": calculate_risk_level(risk_score)
        })

    df = pd.DataFrame(rows)

    df.to_csv("data/ml_governance_dataset.csv", index=False)

    return df