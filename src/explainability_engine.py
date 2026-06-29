import joblib
import pandas as pd


model = joblib.load("models/risk_prediction_model.pkl")


def explain_prediction(data):
    feature_values = {
        "open_issues": data["open_issues"],
        "bugs": data["bugs"],
        "security_issues": data["security_issues"],
        "open_prs": data["open_prs"],
        "recent_commits": data["recent_commits"]
    }

    explanations = []

    if feature_values["open_issues"] > 50:
        explanations.append("High open issues increased governance risk.")

    if feature_values["open_prs"] > 50:
        explanations.append("Large pull request backlog increased review and release risk.")

    if feature_values["recent_commits"] < 5:
        explanations.append("Low recent commit activity reduced project health confidence.")

    if feature_values["bugs"] > 5:
        explanations.append("Bug-labelled issues increased quality risk.")

    if feature_values["security_issues"] > 0:
        explanations.append("Security-labelled issues increased compliance risk.")

    if not explanations:
        explanations.append("No major negative governance signals were detected.")

    return explanations