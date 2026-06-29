import joblib
import pandas as pd


model = joblib.load("models/risk_prediction_model.pkl")
label_encoder = joblib.load("models/risk_label_encoder.pkl")


def predict_repository_risk(data):

    features = pd.DataFrame([{
        "open_issues": data["open_issues"],
        "bugs": data["bugs"],
        "security_issues": data["security_issues"],
        "open_prs": data["open_prs"],
        "recent_commits": data["recent_commits"]
    }])

    prediction = model.predict(features)[0]

    risk_level = label_encoder.inverse_transform([prediction])[0]

    probabilities = model.predict_proba(features)[0]

    confidence = float(max(probabilities) * 100)

    return risk_level, round(confidence, 2)