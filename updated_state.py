class AgentState(BaseModel):

    # Input
    repo_owner: str
    repo_name: str
    pr_number: int

    # Node 1
    pr_data: Dict = Field(default_factory=dict)

    # Node 3
    changed_files: List[Dict] = Field(default_factory=list)

    git_diff: Dict[str, Dict] = Field(default_factory=dict)

    # Node 2
    repository_contents: Dict[str, str] = Field(default_factory=dict)

    # Node 4
    analysis: Optional[DiffAnalysis] = Field(default=None)

    # Errors
    error: Optional[str] = None
