import pandas as pd
import sqlite3


DB_PATH = "data/a3g_pmo_history.db"


def export_dataset():
    connection = sqlite3.connect(DB_PATH)

    df = pd.read_sql_query(
        "SELECT * FROM analysis_history ORDER BY id DESC",
        connection
    )

    connection.close()

    if "id" in df.columns:
        df = df.drop(columns=["id"])

    df.to_csv("data/governance_real_dataset.csv", index=False)

    print(df.head())
    print("\nDataset Shape:", df.shape)
    print("\nDataset exported successfully.")