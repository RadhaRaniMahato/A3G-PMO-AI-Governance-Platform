import streamlit as st
from src.dashboard import render_dashboard
from src.history import render_history

st.set_page_config(page_title="A3G-PMO", layout="wide")

st.sidebar.title("A³G-PMO")
page = st.sidebar.radio("Navigation", ["Dashboard", "History"])

if page == "Dashboard":
    render_dashboard()
elif page == "History":
    render_history()
