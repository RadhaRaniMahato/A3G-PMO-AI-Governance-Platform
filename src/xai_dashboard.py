import streamlit as st
import pandas as pd
import joblib
import plotly.express as px


def render_xai_dashboard():
    st.title("Explainable AI Dashboard")

    st.write("This page explains which GitHub features influence governance risk prediction.")

    model = joblib.load("models/risk_prediction_model.pkl")

    features = [
        "stars", "forks", "watchers", "repo_open_issues",
        "open_issues", "bugs", "security_issues", "open_prs",
        "recent_commits", "releases", "contributors",
        "repo_age_days", "days_since_last_push"
    ]

    if not hasattr(model, "feature_importances_"):
        st.warning("The current model does not support feature importance.")
        return

    importance_df = pd.DataFrame({
        "Feature": features,
        "Importance": model.feature_importances_
    }).sort_values(by="Importance", ascending=False)

    st.subheader("Feature Importance Ranking")
    st.dataframe(importance_df, use_container_width=True)

    fig = px.bar(
        importance_df,
        x="Feature",
        y="Importance",
        title="Explainable AI: Feature Importance"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Human-Readable Explanation")

    top_features = importance_df.head(5)

    for _, row in top_features.iterrows():
        st.write(
            f"• **{row['Feature']}** strongly influences the AI governance risk prediction."
        )