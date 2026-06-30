import os
import json
import joblib
import pandas as pd

from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier, GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report
from sklearn.preprocessing import LabelEncoder


def run_model_benchmark():
    os.makedirs("models", exist_ok=True)

    df = pd.read_csv("data/governance_real_dataset.csv")

    features = [
        "stars", "forks", "watchers", "repo_open_issues",
        "open_issues", "bugs", "security_issues", "open_prs",
        "recent_commits", "releases", "contributors",
        "repo_age_days", "days_since_last_push"
    ]

    X = df[features]

    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(df["risk_level"])

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    models = {
        "Decision Tree": DecisionTreeClassifier(random_state=42),
        "Random Forest": RandomForestClassifier(n_estimators=150, random_state=42),
        "Extra Trees": ExtraTreesClassifier(n_estimators=150, random_state=42),
        "Gradient Boosting": GradientBoostingClassifier(random_state=42)
    }

    results = []
    best_model = None
    best_score = -1
    best_name = ""

    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, average="weighted", zero_division=0)
        recall = recall_score(y_test, y_pred, average="weighted", zero_division=0)
        f1 = f1_score(y_test, y_pred, average="weighted", zero_division=0)

        results.append({
            "model": name,
            "accuracy": round(accuracy, 4),
            "precision": round(precision, 4),
            "recall": round(recall, 4),
            "f1_score": round(f1, 4)
        })

        if f1 > best_score:
            best_score = f1
            best_model = model
            best_name = name

    joblib.dump(best_model, "models/risk_prediction_model.pkl")
    joblib.dump(label_encoder, "models/risk_label_encoder.pkl")

    results_df = pd.DataFrame(results)
    results_df.to_csv(
    "models/model_benchmark_results.csv",
    index=False
)
    with open("models/model_benchmark_results.json", "w") as f:
        json.dump({
            "best_model": best_name,
            "results": results
        }, f, indent=4)

    return best_name, results