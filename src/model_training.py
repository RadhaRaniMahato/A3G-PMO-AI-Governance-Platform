import os
import joblib
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder


def train_risk_model():
    os.makedirs("models", exist_ok=True)

    df = pd.read_csv("data/governance_real_dataset.csv")

    features = [
        "open_issues",
        "bugs",
        "security_issues",
        "open_prs",
        "recent_commits"
    ]

    X = df[features]

    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(df["risk_level"])

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42
    )

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(
        y_test,
        y_pred,
        target_names=label_encoder.classes_
    )

    joblib.dump(model, "models/risk_prediction_model.pkl")
    joblib.dump(label_encoder, "models/risk_label_encoder.pkl")

    return accuracy, report