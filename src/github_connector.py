import os
import requests
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()


def get_headers():
    token = os.getenv("GITHUB_TOKEN")

    if not token:
        return None

    return {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json"
    }


def github_get(url):
    headers = get_headers()

    if not headers:
        return None, "GitHub token not found"

    try:
        response = requests.get(url, headers=headers, timeout=30)

        if response.status_code != 200:
            return None, f"GitHub API Error {response.status_code}: {response.text}"

        return response.json(), None

    except requests.exceptions.RequestException as e:
        return None, f"Request failed: {str(e)}"


def analyze_github_repo(owner, repo):
    repo_url = f"https://api.github.com/repos/{owner}/{repo}"
    issues_url = f"https://api.github.com/repos/{owner}/{repo}/issues?state=open&per_page=100"
    prs_url = f"https://api.github.com/repos/{owner}/{repo}/pulls?state=open&per_page=100"
    commits_url = f"https://api.github.com/repos/{owner}/{repo}/commits?per_page=100"
    releases_url = f"https://api.github.com/repos/{owner}/{repo}/releases?per_page=100"
    contributors_url = f"https://api.github.com/repos/{owner}/{repo}/contributors?per_page=100"

    repo_data, error = github_get(repo_url)
    if error:
        return {"auth_status": "Token loaded", "error": error}

    issues, error = github_get(issues_url)
    if error:
        issues = []

    prs, error = github_get(prs_url)
    if error:
        prs = []

    commits, error = github_get(commits_url)
    if error:
        commits = []

    releases, error = github_get(releases_url)
    if error:
        releases = []

    contributors, error = github_get(contributors_url)
    if error:
        contributors = []

    bugs = 0
    security_issues = 0

    for issue in issues:
        if "pull_request" in issue:
            continue

        labels = [label["name"].lower() for label in issue.get("labels", [])]

        if "bug" in labels:
            bugs += 1

        if "security" in labels or "vulnerability" in labels:
            security_issues += 1

    created_at = repo_data.get("created_at")
    pushed_at = repo_data.get("pushed_at")

    repo_age_days = 0
    days_since_last_push = 0

    if created_at:
        created_date = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
        repo_age_days = (datetime.now(timezone.utc) - created_date).days

    if pushed_at:
        pushed_date = datetime.fromisoformat(pushed_at.replace("Z", "+00:00"))
        days_since_last_push = (datetime.now(timezone.utc) - pushed_date).days

    return {
        "auth_status": "Token loaded",
        "error": None,
        "stars": repo_data.get("stargazers_count", 0),
        "forks": repo_data.get("forks_count", 0),
        "watchers": repo_data.get("watchers_count", 0),
        "repo_open_issues": repo_data.get("open_issues_count", 0),
        "open_issues": len([issue for issue in issues if "pull_request" not in issue]),
        "bugs": bugs,
        "security_issues": security_issues,
        "open_prs": len(prs),
        "recent_commits": len(commits),
        "releases": len(releases),
        "contributors": len(contributors),
        "repo_age_days": repo_age_days,
        "days_since_last_push": days_since_last_push
    }