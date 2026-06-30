import pandas as pd

from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.preprocessing import LabelEncoder

from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    RandomForestClassifier,
    ExtraTreesClassifier,
    GradientBoostingClassifier,
)


def evaluate_models():

    df = pd.read_csv("data/governance_real_dataset.csv")

    features = [
        "stars",
        "forks",
        "watchers",
        "repo_open_issues",
        "open_issues",
        "bugs",
        "security_issues",
        "open_prs",
        "recent_commits",
        "releases",
        "contributors",
        "repo_age_days",
        "days_since_last_push",
    ]

    X = df[features]

    encoder = LabelEncoder()
    y = encoder.fit_transform(df["risk_level"])

    cv = StratifiedKFold(
        n_splits=5,
        shuffle=True,
        random_state=42
    )

    models = {
        "Decision Tree": DecisionTreeClassifier(random_state=42),
        "Random Forest": RandomForestClassifier(
            n_estimators=150,
            random_state=42
        ),
        "Extra Trees": ExtraTreesClassifier(
            n_estimators=150,
            random_state=42
        ),
        "Gradient Boosting": GradientBoostingClassifier(
            random_state=42
        ),
    }

    results = []

    scoring = [
        "accuracy",
        "precision_weighted",
        "recall_weighted",
        "f1_weighted",
    ]

    for name, model in models.items():

        scores = cross_validate(
            model,
            X,
            y,
            cv=cv,
            scoring=scoring
        )

        results.append({
            "Model": name,
            "Accuracy": round(scores["test_accuracy"].mean(), 4),
            "Precision": round(scores["test_precision_weighted"].mean(), 4),
            "Recall": round(scores["test_recall_weighted"].mean(), 4),
            "F1 Score": round(scores["test_f1_weighted"].mean(), 4),
            "Std Accuracy": round(scores["test_accuracy"].std(), 4),
        })

    results = pd.DataFrame(results)

    print(results)

    return results