import pandas as pd
import plotly.express as px


def create_risk_chart(open_issues, bugs, security_issues, open_prs, recent_commits):
    df = pd.DataFrame({
        "Metric": ["Open Issues", "Bug Issues", "Security Issues", "Open Pull Requests", "Recent Commits"],
        "Count": [open_issues, bugs, security_issues, open_prs, recent_commits]
    })
    return px.bar(df, x="Metric", y="Count", title="Repository Governance Metrics")


def create_trend_chart(df):
    if df.empty:
        return None
    return px.line(
        df,
        x="Timestamp",
        y=["Risk Score", "Compliance Score", "Health Score"],
        title="Governance Trend Over Time",
        markers=True
    )
