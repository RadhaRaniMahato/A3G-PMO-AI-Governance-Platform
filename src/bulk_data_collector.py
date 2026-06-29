import pandas as pd
from src.github_connector import analyze_github_repo
from src.risk_engine import calculate_risk
from src.compliance_engine import calculate_compliance_score
from src.health_engine import calculate_health_score
from src.database import save_analysis


def collect_bulk_data():
    repos = pd.read_csv("data/repositories.csv")

    success = 0
    failed = 0

    for _, row in repos.iterrows():

        owner = row["owner"]
        repo = row["repo"]

        print(f"Analyzing {owner}/{repo}...")

        data = analyze_github_repo(owner, repo)

        if data["error"]:
            print(f"Failed: {owner}/{repo}")
            failed += 1
            continue

        risk_score, risk_level, recommendation = calculate_risk(data)

        compliance_score, compliance_status = calculate_compliance_score(
            data["open_issues"],
            data["bugs"],
            data["security_issues"]
        )

        health_score, health_status = calculate_health_score(
            risk_score,
            compliance_score,
            data["recent_commits"]
        )

        save_analysis(
            owner,
            repo,
            data,
            risk_score,
            risk_level,
            compliance_score,
            compliance_status,
            health_score,
            health_status
        )

        success += 1

    print("\nCollection Completed")
    print(f"Successful: {success}")
    print(f"Failed: {failed}")