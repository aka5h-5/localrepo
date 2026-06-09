from github import Github
from state import AgentState
import os
import logging

logger = logging.getLogger(__name__)


def fetch_pr_data(state: AgentState) -> AgentState:
    try:
        logger.info(f"Fetching PR #{state.pr_number} from {state.repo_owner}/{state.repo_name}")

        github_token = os.getenv("GITHUB_TOKEN")
        if not github_token:
            raise ValueError("GITHUB_TOKEN not found in environment")

        g = Github(github_token)

        repo = g.get_repo(f"{state.repo_owner}/{state.repo_name}")
        pr = repo.get_pull(state.pr_number)

        # ✅ PR Metadata
        pr_data = {
            "title": pr.title,
            "description": pr.body,
            "author": pr.user.login,
            "source_branch": pr.head.ref,
            "target_branch": pr.base.ref,
            "state": pr.state,
            "created_at": str(pr.created_at),
            "merged": pr.is_merged(),
            "mergeable": pr.mergeable
        }

        #Changed Files (CRITICAL)
        files = pr.get_files()
        changed_files = []

        for f in files:
            changed_files.append({
                "filename": f.filename,
                "status": f.status,
                "additions": f.additions,
                "deletions": f.deletions,
                "changes": f.changes,
                "patch": f.patch
            })

        #Commits (helps AI understand intent)
        commits = pr.get_commits()
        commit_messages = [c.commit.message for c in commits]

        #Update state
        state.pr_data = pr_data
        state.changed_files = changed_files
        state.commit_messages = commit_messages

        logger.info(f"PR #{state.pr_number} fetched successfully with {len(changed_files)} files")

        return state

    except Exception as e:
        logger.error(f"Error fetching PR data: {str(e)}")
        state.error = str(e)
        return state
