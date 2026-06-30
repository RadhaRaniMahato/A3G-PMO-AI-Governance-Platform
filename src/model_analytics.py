import json
import pandas as pd
import streamlit as st
import plotly.express as px
import joblib


def render_model_analytics():
    st.title("Model Analytics")

    results_df = pd.read_csv("models/model_benchmark_results.csv")

    with open("models/model_benchmark_results.json", "r") as f:
        benchmark_data = json.load(f)

    best_model = benchmark_data["best_model"]

    st.subheader("Best Performing Model")
    st.success(best_model)

    st.subheader("Model Comparison")
    st.dataframe(results_df, use_container_width=True)

    fig = px.bar(
        results_df,
        x="model",
        y="f1_score",
        title="Model F1 Score Comparison"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Feature Importance")

    model = joblib.load("models/risk_prediction_model.pkl")

    features = [
        "stars", "forks", "watchers", "repo_open_issues",
        "open_issues", "bugs", "security_issues", "open_prs",
        "recent_commits", "releases", "contributors",
        "repo_age_days", "days_since_last_push"
    ]

    if hasattr(model, "feature_importances_"):
        importance_df = pd.DataFrame({
            "feature": features,
            "importance": model.feature_importances_
        }).sort_values(by="importance", ascending=False)

        st.dataframe(importance_df, use_container_width=True)

        fig2 = px.bar(
            importance_df,
            x="feature",
            y="importance",
            title="Feature Importance"
        )
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.warning("Selected model does not support feature importance.")