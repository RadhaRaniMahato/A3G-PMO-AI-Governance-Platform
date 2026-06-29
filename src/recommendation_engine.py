def generate_governance_actions(open_issues, bugs, security_issues, risk_level):
    actions = []
    if open_issues > 50:
        actions.append("Schedule backlog refinement to reduce open issue load.")
    if bugs > 5:
        actions.append("Prioritize bug fixing in the next sprint.")
    if security_issues > 0:
        actions.append("Perform immediate security review before release.")
    if risk_level == "Medium":
        actions.append("Conduct PMO-level sprint governance review.")
    if risk_level == "High":
        actions.append("Escalate to governance board and freeze release until risks are reviewed.")
    if not actions:
        actions.append("Continue normal Agile governance monitoring.")
    return actions
