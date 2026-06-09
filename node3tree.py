from langgraph.graph import StateGraph, START, END

from state import AgentState
from node1 import get_pr_details
from node2 import load_repo_contents
from node3 import get_diff

builder = StateGraph(AgentState)

builder.add_node("get_pr_details", get_pr_details)
builder.add_node("load_repo_contents", load_repo_contents)
builder.add_node("get_diff", get_diff)

builder.add_edge(START, "get_pr_details")
builder.add_edge("get_pr_details", "load_repo_contents")
builder.add_edge("load_repo_contents", "get_diff")
builder.add_edge("get_diff", END)

graph = builder.compile()


if __name__ == "__main__":

    state = AgentState(
        owner="TS-KAAG",
        repository="visual-test-frontend",
        pr_id=31
    )

    result = graph.invoke(state)

    print("\n=== PR DETAILS ===")
    print(result.pr_details)

    print("\n=== REPOSITORY FILES ===")
    print(len(result.repository_contents))

    print("\n=== CHANGED FILES ===")
    print(result.changed_files)

    print("\n=== GIT DIFF ===")
    print(result.git_diff)
