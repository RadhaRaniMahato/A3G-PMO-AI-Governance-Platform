# A³G-PMO Governance Dashboard

A³G-PMO is an Adaptive Agile AI Governance Dashboard for AI-enabled PMOs in regulated industries. It analyzes live GitHub repository data and generates governance insights for project managers and PMO teams.

## Features

- Live GitHub repository analysis
- Open issue, bug, security issue, pull request, and commit analysis
- Governance risk score
- Compliance score
- Project health score
- AI-based governance action plan
- Downloadable PDF governance report
- SQLite-based repository analysis history
- Historical trend analytics
- Interactive dashboard using Streamlit and Plotly

## Tech Stack

- Python
- Streamlit
- GitHub REST API
- SQLite
- Plotly
- ReportLab
- python-dotenv

## How to Run

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## Environment Variables

Create a `.env` file in the project root:

```text
GITHUB_TOKEN=your_github_token_here
```

Do not upload `.env` to GitHub.
