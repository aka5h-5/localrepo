from github import Github
from dotenv import load_dotenv
import os
import logging
from state import AgentState

load_dotenv()
logger = logging.getLogger(__name__)


def get_diff(state: AgentState) -> AgentState:
    try:
        logger.info("Extracting PR diff...")

        github_token = os.getenv("GITHUB_TOKEN")
        if not github_token:
            raise ValueError("Missing GITHUB_TOKEN")

        g = Github(github_token)
        repo = g.get_repo(f"{state.repo_owner}/{state.repo_name}")
        pr = repo.get_pull(state.pr_number)

        files = pr.get_files()

        # ✅ Initialize safely
        git_diff = {}

        for file in files:
            # ✅ Skip files without patch (e.g., binary files)
            if not file.patch:
                continue

            git_diff[file.filename] = {
                "status": file.status,
                "patch": file.patch,
                "additions": file.additions,
                "deletions": file.deletions,
                "changes": file.changes,
                "previous_filename": getattr(file, "previous_filename", None)
            }

        # ✅ DO NOT modify changed_files structure here
        state.git_diff = git_diff

        logger.info(f"Processed diff for {len(git_diff)} files")

        return state

    except Exception as e:
        logger.error(f"Error in get_diff: {str(e)}")
        state.error = str(e)
        return state
