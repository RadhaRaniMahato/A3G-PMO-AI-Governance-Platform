import pandas as pd
import shap
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

FEATURES = [
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


def get_shap_explanation(data):

    df = pd.read_csv("data/governance_real_dataset.csv")

    X = df[FEATURES]

    encoder = LabelEncoder()
    y = encoder.fit_transform(df["risk_level"])

    model = RandomForestClassifier(
        n_estimators=150,
        random_state=42
    )

    model.fit(X, y)

    feature_row = pd.DataFrame([{
        feature: data.get(feature, 0)
        for feature in FEATURES
    }])

    explainer = shap.TreeExplainer(model)

    shap_values = explainer.shap_values(feature_row)

    predicted_class = model.predict(feature_row)[0]

    if isinstance(shap_values, list):
        values = shap_values[predicted_class][0]
    else:
        values = shap_values[0, :, predicted_class]

    explanation_df = pd.DataFrame({
        "feature": FEATURES,
        "value": feature_row.iloc[0].values,
        "shap_value": values
    })

    explanation_df = explanation_df.sort_values(
        by="shap_value",
        ascending=False
    )

    return explanation_df