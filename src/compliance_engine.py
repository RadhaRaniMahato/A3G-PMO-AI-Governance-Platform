def calculate_compliance_score(open_issues, bugs, security_issues):
    score = 100 - (open_issues * 0.3) - (bugs * 2) - (security_issues * 10)
    score = max(0, min(100, score))

    if score >= 80:
        status = "Compliant"
    elif score >= 50:
        status = "Partially Compliant"
    else:
        status = "Non-Compliant"

    return round(score, 2), status
