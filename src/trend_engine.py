import pandas as pd
import sqlite3

DB_PATH = "data/a3g_pmo_history.db"


def get_trend_data():
    conn = sqlite3.connect(DB_PATH)

    query = """
    SELECT
        timestamp,
        repo,
        risk_score,
        compliance_score,
        health_score
    FROM analysis_history
    ORDER BY timestamp
    """

    df = pd.read_sql_query(query, conn)
    conn.close()

    return df