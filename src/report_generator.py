from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime
import os


def generate_governance_report(owner, repo, data, risk_score, risk_level, compliance_score, compliance_status, health_score, health_status, recommendation, actions):
    os.makedirs("reports", exist_ok=True)
    file_path = "reports/governance_report.pdf"
    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4
    y = height - 50

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "A3G-PMO Governance Report")
    y -= 30
    c.setFont("Helvetica", 10)
    c.drawString(50, y, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    y -= 30
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Repository Details")
    y -= 20
    c.setFont("Helvetica", 10)
    c.drawString(50, y, f"GitHub Owner: {owner}")
    y -= 18
    c.drawString(50, y, f"Repository: {repo}")

    y -= 30
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Governance Metrics")
    metrics = [
        ("Open Issues", data["open_issues"]),
        ("Bug Issues", data["bugs"]),
        ("Security Issues", data["security_issues"]),
        ("Open Pull Requests", data["open_prs"]),
        ("Recent Commits", data["recent_commits"]),
        ("Risk Score", risk_score),
        ("Risk Level", risk_level),
        ("Compliance Score", compliance_score),
        ("Compliance Status", compliance_status),
        ("Health Score", health_score),
        ("Health Status", health_status),
    ]
    y -= 20
    c.setFont("Helvetica", 10)
    for label, value in metrics:
        c.drawString(50, y, f"{label}: {value}")
        y -= 18

    y -= 15
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "PMO Recommendation")
    y -= 20
    c.setFont("Helvetica", 10)
    c.drawString(50, y, recommendation[:100])

    y -= 30
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "AI Governance Action Plan")
    y -= 20
    c.setFont("Helvetica", 10)
    for action in actions:
        c.drawString(50, y, f"- {action[:100]}")
        y -= 18

    c.save()
    return file_path
