import streamlit as st
import pandas as pd
import sqlite3


DB_PATH = "data/a3g_pmo_history.db"


def render_history():
    st.title("Repository Analysis History")

    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM analysis_history ORDER BY id DESC", conn)
    conn.close()

    if df.empty:
        st.info("No repository history available yet.")
        return

    if "id" in df.columns:
        df = df.drop(columns=["id"])

    st.subheader("Repository Statistics")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Analyses", len(df))
    col2.metric("Average Risk", round(df["risk_score"].mean(), 2))
    col3.metric("Average Compliance", round(df["compliance_score"].mean(), 2))

    st.subheader("Analysis History")
    st.dataframe(df, use_container_width=True)