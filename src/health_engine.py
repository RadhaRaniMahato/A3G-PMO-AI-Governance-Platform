def calculate_health_score(risk_score, compliance_score, recent_commits):
    health_score = 100 - (risk_score * 0.4) + (compliance_score * 0.3)

    if recent_commits >= 20:
        health_score += 10
    elif recent_commits < 5:
        health_score -= 10

    health_score = max(0, min(100, health_score))

    if health_score >= 80:
        status = "Healthy"
    elif health_score >= 50:
        status = "Needs Attention"
    else:
        status = "Critical"

    return round(health_score, 2), status
