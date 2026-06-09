from pydantic import BaseModel, Field
from typing import Dict, List, Optional


class DiffAnalysis(BaseModel):
    change_summary: str = ""
    risk_level: str = ""
    business_impact: str = ""
    testing_areas: List[str] = Field(default_factory=list)


class AgentState(BaseModel):

    # Input
    owner: str
    repository: str
    pr_id: int

    # Node 1
    pr_data: Dict = Field(default_factory=dict)

    # Node 2
    repository_contents: Dict[str, str] = Field(
        default_factory=dict
    )

    # Node 3
    changed_files: List[str] = Field(
        default_factory=list
    )

    git_diff: Dict = Field(
        default_factory=dict
    )

    # Node 4
    analysis: Optional[DiffAnalysis] = None
