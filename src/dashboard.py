import streamlit as st

from src.github_connector import analyze_github_repo
from src.risk_engine import calculate_risk
from src.visualization import create_risk_chart
from src.recommendation_engine import generate_governance_actions
from src.compliance_engine import calculate_compliance_score
from src.health_engine import calculate_health_score
from src.report_generator import generate_governance_report
from src.governance_assistant import answer_governance_question
from src.database import save_analysis
from src.prediction_engine import predict_repository_risk
from src.explainability_engine import explain_prediction
from src.shap_engine import get_shap_explanation
from src.trend_engine import get_trend_data
from src.trend_visualization import create_trend_chart


def render_dashboard():
    st.title("A³G-PMO Governance Dashboard")
    st.write("Real-time Agile AI Governance analysis using GitHub repository data.")

    owner = st.text_input("GitHub Owner", "octocat")
    repo = st.text_input("Repository", "Hello-World")

    if st.button("Analyze Repository"):
        data = analyze_github_repo(owner, repo)
        st.write("Auth Status:", data.get("auth_status"))

        if data["error"]:
            st.error(data["error"])
            return

        risk_score, risk_level, recommendation = calculate_risk(data)

        actions = generate_governance_actions(
            data["open_issues"],
            data["bugs"],
            data["security_issues"],
            risk_level
        )

        compliance_score, compliance_status = calculate_compliance_score(
            data["open_issues"],
            data["bugs"],
            data["security_issues"]
        )

        health_score, health_status = calculate_health_score(
            risk_score,
            compliance_score,
            data["recent_commits"]
        )

        predicted_risk, prediction_confidence = predict_repository_risk(data)

        save_analysis(
            owner,
            repo,
            data,
            risk_score,
            risk_level,
            compliance_score,
            compliance_status,
            health_score,
            health_status
        )

        st.session_state["analysis"] = {
            "owner": owner,
            "repo": repo,
            "data": data,
            "risk_score": risk_score,
            "risk_level": risk_level,
            "recommendation": recommendation,
            "actions": actions,
            "compliance_score": compliance_score,
            "compliance_status": compliance_status,
            "health_score": health_score,
            "health_status": health_status,
            "predicted_risk": predicted_risk,
            "prediction_confidence": prediction_confidence
        }

    if "analysis" not in st.session_state:
        st.info("Enter a GitHub repository and click Analyze Repository.")
        return

    result = st.session_state["analysis"]

    data = result["data"]
    risk_score = result["risk_score"]
    risk_level = result["risk_level"]
    recommendation = result["recommendation"]
    actions = result["actions"]
    compliance_score = result["compliance_score"]
    compliance_status = result["compliance_status"]
    health_score = result["health_score"]
    health_status = result["health_status"]
    predicted_risk = result["predicted_risk"]
    prediction_confidence = result["prediction_confidence"]

    st.success("GitHub connection successful!")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Open Issues", data["open_issues"])
    col2.metric("Bug Issues", data["bugs"])
    col3.metric("Security Issues", data["security_issues"])
    col4.metric("Open Pull Requests", data["open_prs"])

    col5, col6, col7, col8 = st.columns(4)
    col5.metric("Recent Commits", data["recent_commits"])
    col6.metric("Risk Score", risk_score)
    col7.metric("Compliance Score", compliance_score)
    col8.metric("Health Score", health_score)

    st.subheader("🤖 AI Risk Prediction")
    pred_col1, pred_col2 = st.columns(2)
    pred_col1.metric("Predicted Risk", predicted_risk)
    pred_col2.metric("Prediction Confidence", f"{prediction_confidence:.2f}%")

    st.subheader("🔍 Explainable AI Insights")
    explanations = explain_prediction(data)
    for explanation in explanations:
        st.write("•", explanation)

    st.subheader("SHAP-Based Repository Explanation")
    shap_df = get_shap_explanation(data)
    st.dataframe(shap_df, use_container_width=True)

    st.write("### Top Risk-Increasing Factors")
    for _, row in shap_df.head(5).iterrows():
        st.write(f"• **{row['feature']}** : {row['shap_value']:.4f}")

    st.write("### Top Risk-Reducing Factors")
    for _, row in shap_df.tail(3).iterrows():
        st.write(f"• **{row['feature']}** : {row['shap_value']:.4f}")

    fig = create_risk_chart(
        data["open_issues"],
        data["bugs"],
        data["security_issues"],
        data["open_prs"],
        data["recent_commits"]
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Governance Risk Level")
    if risk_level == "Low":
        st.success(risk_level)
    elif risk_level == "Medium":
        st.warning(risk_level)
    else:
        st.error(risk_level)

    st.subheader("Compliance Status")
    if compliance_status == "Compliant":
        st.success(compliance_status)
    elif compliance_status == "Partially Compliant":
        st.warning(compliance_status)
    else:
        st.error(compliance_status)

    st.subheader("Project Health Status")
    if health_status == "Healthy":
        st.success(health_status)
    elif health_status == "Needs Attention":
        st.warning(health_status)
    else:
        st.error(health_status)

    st.subheader("PMO Recommendation")
    st.info(recommendation)

    st.subheader("AI Governance Action Plan")
    for action in actions:
        st.write("✅", action)

    report_path = generate_governance_report(
        result["owner"],
        result["repo"],
        data,
        risk_score,
        risk_level,
        compliance_score,
        compliance_status,
        health_score,
        health_status,
        recommendation,
        actions
    )

    with open(report_path, "rb") as pdf_file:
        st.download_button(
            label="Download Governance Report",
            data=pdf_file,
            file_name="A3G_PMO_Governance_Report.pdf",
            mime="application/pdf"
        )

    st.subheader("AI Governance Assistant")
    user_question = st.text_area(
        "Ask a governance question",
        "Why is the project risk high?"
    )

    if st.button("Get Assistant Answer"):
        assistant_answer = answer_governance_question(
            user_question,
            data,
            risk_score,
            risk_level,
            compliance_score,
            compliance_status,
            health_score,
            health_status,
            recommendation,
            actions
        )
        st.write(assistant_answer)

    st.subheader("📈 Governance Trend Analytics")
    trend_df = get_trend_data()

    if not trend_df.empty:
        trend_chart = create_trend_chart(trend_df)
        st.plotly_chart(trend_chart, use_container_width=True)