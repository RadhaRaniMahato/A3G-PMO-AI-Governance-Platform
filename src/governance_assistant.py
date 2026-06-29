def answer_governance_question(question, data, risk_score, risk_level, compliance_score, compliance_status, health_score, health_status, recommendation, actions):
    q = question.lower()

    if "risk" in q:
        return (
            f"The current governance risk level is {risk_level} with a risk score of {risk_score}. "
            f"Main contributors are {data['open_issues']} open issues and {data['open_prs']} open pull requests."
        )
    if "health" in q:
        return (
            f"The project health status is {health_status} with a health score of {health_score}. "
            f"Recent commits are {data['recent_commits']}, which affects project activity health."
        )
    if "compliance" in q:
        return (
            f"The compliance status is {compliance_status} with a compliance score of {compliance_score}. "
            "Security issues, unresolved bugs, and large backlogs reduce compliance confidence."
        )
    if "recommend" in q or "suggest" in q or "action" in q:
        return "Recommended governance actions are: " + " ".join(actions)
    if "summary" in q or "summarize" in q:
        return (
            f"This repository has {data['open_issues']} open issues, {data['open_prs']} open pull requests, "
            f"{data['recent_commits']} recent commits, risk score {risk_score}, compliance score {compliance_score}, "
            f"and health score {health_score}. Overall status: {risk_level} risk, {compliance_status} compliance, "
            f"and {health_status} project health."
        )

    return "I can answer questions about risk, compliance, health, recommendations, action plans, and repository summary."
