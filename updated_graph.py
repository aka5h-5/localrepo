builder = StateGraph(AgentState)

builder.add_node("get_pr_details", fetch_pr_data)
builder.add_node("get_diff", getDiff)
builder.add_node("load_repo_contents", loadRepoContents)

builder.add_edge(START, "get_pr_details")
builder.add_edge("get_pr_details", "get_diff")  # ✅ fixed
builder.add_edge("get_diff", "load_repo_contents")  # ✅ fixed
builder.add_edge("load_repo_contents", END)

graph = builder.compile()
