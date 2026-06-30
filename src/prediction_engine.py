import joblib
import pandas as pd


FEATURES = [
    "stars", "forks", "watchers", "repo_open_issues",
    "open_issues", "bugs", "security_issues", "open_prs",
    "recent_commits", "releases", "contributors",
    "repo_age_days", "days_since_last_push"
]


model = joblib.load("models/risk_prediction_model.pkl")
label_encoder = joblib.load("models/risk_label_encoder.pkl")


def predict_repository_risk(data):
    features = pd.DataFrame([{
        feature: data.get(feature, 0)
        for feature in FEATURES
    }])

    prediction = model.predict(features)[0]
    risk_level = label_encoder.inverse_transform([prediction])[0]

    probabilities = model.predict_proba(features)[0]
    confidence = float(max(probabilities) * 100)

    return risk_level, round(confidence, 2)