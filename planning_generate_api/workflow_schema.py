from typing import Optional, List
from pydantic import BaseModel, Field

class InputSchema(BaseModel):
    """Input schema for a planning step."""
    type: str = Field(description="The type of input")
    description: Optional[str] = Field(default=None, description="Description of the input")

class OutputSchema(BaseModel):
    """Output schema for a planning step."""
    type: Optional[str] = Field(default=None, description="The type of output")
    description: Optional[str] = Field(default=None, description="Description of the output")

class PlanningStep(BaseModel):
    """A single step in the planning process."""
    step: int = Field(description="The step number")
    previous_step: int = Field(description="The previous step number that this step depends on")
    name: str = Field(description="The name of the step")
    oid: str = Field(description="The unique identifier of the step")
    description: str = Field(description="Description of the step")
    input: InputSchema = Field(description="Input requirements for the step")
    output: OutputSchema = Field(description="Output specifications for the step")
    title: str = Field(description="The title of the step")

class WorkflowPlan(BaseModel):
    """Complete workflow planning structure."""
    planning_steps: List[PlanningStep] = Field(description="List of planning steps in the workflow")

# Example usage:
# structured_llm = llm.with_structured_output(WorkflowPlan)
# result = structured_llm.invoke("Generate a workflow plan for...") 