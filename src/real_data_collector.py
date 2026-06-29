from src.github_connector import analyze_github_repo
from src.risk_engine import calculate_risk
from src.compliance_engine import calculate_compliance_score
from src.health_engine import calculate_health_score
from src.database import save_analysis


REAL_REPOSITORIES = [
    ("octocat", "Hello-World"),
    ("streamlit", "streamlit"),
    ("pandas-dev", "pandas"),
    ("numpy", "numpy"),
    ("scikit-learn", "scikit-learn"),
    ("psf", "requests"),
    ("django", "django"),
    ("fastapi", "fastapi"),
    ("plotly", "plotly.py"),
    ("keras-team", "keras")
]


def collect_real_github_data():
    results = []

    for owner, repo in REAL_REPOSITORIES:
        print(f"Analyzing {owner}/{repo}...")

        data = analyze_github_repo(owner, repo)

        if data["error"]:
            print(f"Error for {owner}/{repo}: {data['error']}")
            continue

        risk_score, risk_level, recommendation = calculate_risk(
            data["open_issues"],
            data["bugs"],
            data["security_issues"],
            data["open_prs"],
            data["recent_commits"]
        )

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

        results.append({
            "owner": owner,
            "repo": repo,
            "risk_score": risk_score,
            "risk_level": risk_level,
            "compliance_score": compliance_score,
            "health_score": health_score,
            "health_status": health_status
        })

    return results