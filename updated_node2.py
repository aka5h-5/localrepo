from github import Github
from dotenv import load_dotenv
import os
import logging
from state import AgentState

load_dotenv()

logger = logging.getLogger(__name__)

# ✅ Allowed file types
VALID_EXTENSIONS = (".py", ".js", ".ts", ".json", ".yaml", ".yml")

# ✅ Max file size (in bytes)
MAX_FILE_SIZE = 200_000  # ~200 KB


def load_repo_contents(state: AgentState) -> AgentState:
    try:
        logger.info("Loading repository contents...")

        github_token = os.getenv("GITHUB_TOKEN")
        if not github_token:
            raise ValueError("Missing GITHUB_TOKEN")

        g = Github(github_token)
        repo = g.get_repo(f"{state.repo_owner}/{state.repo_name}")

        repo_contents = {}

        # ✅ Only load changed files (BEST PRACTICE)
        if not state.changed_files:
            logger.warning("No changed files found, skipping repo load")
            state.repository_contents = {}
            return state

        for file_info in state.changed_files:
            path = file_info["filename"]

            # ✅ Skip unwanted files
            if not path.endswith(VALID_EXTENSIONS):
                continue

            try:
                file = repo.get_contents(path)

                # ✅ Skip large files
                if file.size and file.size > MAX_FILE_SIZE:
                    logger.warning(f"Skipping large file: {path}")
                    continue

                content = file.decoded_content.decode("utf-8", errors="ignore")
                repo_contents[path] = content

            except Exception as e:
                logger.warning(f"Failed to load {path}: {str(e)}")

        state.repository_contents = repo_contents

        logger.info(f"Loaded {len(repo_contents)} files")

        return state

    except Exception as e:
        logger.error(f"Error in load_repo_contents: {str(e)}")
        state.error = str(e)
        return state
