import plotly.express as px


def create_trend_chart(df):

    fig = px.line(
        df,
        x="timestamp",
        y="risk_score",
        color="repo",
        markers=True,
        title="Governance Risk Trend"
    )

    return fig