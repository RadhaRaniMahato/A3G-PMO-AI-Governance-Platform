```python
import sqlite3
from datetime import datetime
import os


DB_PATH = "data/a3g_pmo_history.db"


def create_database():
    os.makedirs("data", exist_ok=True)

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS analysis_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            owner TEXT,
            repo TEXT,

            stars INTEGER,
            forks INTEGER,
            watchers INTEGER,
            repo_open_issues INTEGER,

            open_issues INTEGER,
            bugs INTEGER,
            security_issues INTEGER,
            open_prs INTEGER,
            recent_commits INTEGER,
            releases INTEGER,
            contributors INTEGER,
            repo_age_days INTEGER,
            days_since_last_push INTEGER,

            risk_score REAL,
            risk_level TEXT,
            compliance_score REAL,
            compliance_status TEXT,
            health_score REAL,
            health_status TEXT
        )
    """)

    connection.commit()
    connection.close()


def migrate_database():
    """
    Adds missing columns to existing SQLite database.
    Useful when old database exists with previous schema.
    """

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("PRAGMA table_info(analysis_history)")
    existing_columns = [
        column[1] for column in cursor.fetchall()
    ]

    required_columns = {
        "stars": "INTEGER",
        "forks": "INTEGER",
        "watchers": "INTEGER",
        "repo_open_issues": "INTEGER",
        "open_issues": "INTEGER",
        "bugs": "INTEGER",
        "security_issues": "INTEGER",
        "open_prs": "INTEGER",
        "recent_commits": "INTEGER",
        "releases": "INTEGER",
        "contributors": "INTEGER",
        "repo_age_days": "INTEGER",
        "days_since_last_push": "INTEGER",
        "risk_score": "REAL",
        "risk_level": "TEXT",
        "compliance_score": "REAL",
        "compliance_status": "TEXT",
        "health_score": "REAL",
        "health_status": "TEXT"
    }

    for column, datatype in required_columns.items():
        if column not in existing_columns:
            cursor.execute(
                f"ALTER TABLE analysis_history ADD COLUMN {column} {datatype}"
            )

    connection.commit()
    connection.close()


def save_analysis(
    owner,
    repo,
    data,
    risk_score,
    risk_level,
    compliance_score,
    compliance_status,
    health_score,
    health_status
):

    create_database()
    migrate_database()

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO analysis_history (
            timestamp,
            owner,
            repo,
            stars,
            forks,
            watchers,
            repo_open_issues,
            open_issues,
            bugs,
            security_issues,
            open_prs,
            recent_commits,
            releases,
            contributors,
            repo_age_days,
            days_since_last_push,
            risk_score,
            risk_level,
            compliance_score,
            compliance_status,
            health_score,
            health_status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        owner,
        repo,
        data.get("stars", 0),
        data.get("forks", 0),
        data.get("watchers", 0),
        data.get("repo_open_issues", 0),
        data.get("open_issues", 0),
        data.get("bugs", 0),
        data.get("security_issues", 0),
        data.get("open_prs", 0),
        data.get("recent_commits", 0),
        data.get("releases", 0),
        data.get("contributors", 0),
        data.get("repo_age_days", 0),
        data.get("days_since_last_push", 0),
        risk_score,
        risk_level,
        compliance_score,
        compliance_status,
        health_score,
        health_status
    ))

    connection.commit()
    connection.close()


def get_analysis_history():

    create_database()
    migrate_database()

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            timestamp,
            owner,
            repo,
            stars,
            forks,
            watchers,
            repo_open_issues,
            open_issues,
            bugs,
            security_issues,
            open_prs,
            recent_commits,
            releases,
            contributors,
            repo_age_days,
            days_since_last_push,
            risk_score,
            risk_level,
            compliance_score,
            compliance_status,
            health_score,
            health_status
        FROM analysis_history
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    connection.close()

    return rows
```
