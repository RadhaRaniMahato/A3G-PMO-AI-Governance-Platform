def calculate_risk(data):
    activity_score = min(data.get("recent_commits", 0) * 2, 100)
    community_score = min(
        data.get("stars", 0) * 0.01 +
        data.get("forks", 0) * 0.02 +
        data.get("contributors", 0) * 2,
        100
    )

    backlog_pressure = (
        data.get("open_issues", 0) * 0.7 +
        data.get("open_prs", 0) * 1.2 +
        data.get("bugs", 0) * 4 +
        data.get("security_issues", 0) * 10
    )

    inactivity_penalty = min(data.get("days_since_last_push", 0) * 0.5, 100)

    risk_score = backlog_pressure + inactivity_penalty - activity_score * 0.5 - community_score * 0.3

    if risk_score < 50:
        risk_level = "Low"
    elif risk_score < 150:
        risk_level = "Medium"
    else:
        risk_level = "High"

    recommendation = (
        "Review backlog, pull requests, commit activity, and security-labelled issues before the next release."
    )

    return round(max(risk_score, 0), 2), risk_level, recommendation