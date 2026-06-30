import streamlit as st
from src.model_analytics import render_model_analytics
from src.dashboard import render_dashboard
from src.history import render_history
from src.xai_dashboard import render_xai_dashboard

st.set_page_config(page_title="A3G-PMO", layout="wide")

st.sidebar.title("A³G-PMO")
page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "History", "Model Analytics", "Explainable AI"]
)
if page == "Dashboard":
    render_dashboard()
elif page == "History":
    render_history()
elif page == "Model Analytics":
    render_model_analytics()
elif page == "Explainable AI":
    render_xai_dashboard()