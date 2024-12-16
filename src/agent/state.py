import operator
from dataclasses import dataclass, field
from pydantic import BaseModel, Field
from typing_extensions import TypedDict, List, Annotated

class Take(BaseModel):
    title: str = Field(
        description="Punchy summary title for the take",
    )
    take: str = Field(
        description="Fun, punchy observation about the newsworthy topic",
    )
    source_url: str = Field(
        description="Source data URL for information in the take (if applicable)",
    )
    reddit_url: str = Field(
        description="Reddit post URL for the post",
    )
    reasoning: str = Field(
        description="Provide your reasoning for the take, which confirms that the take is relevant to the newsworthy topic",
    )

class Takes(BaseModel):
    takes: List[Take] = Field(
        description="A list of takes, each containing a title and a take observation."
    )

@dataclass(kw_only=True)
class TakeGeneratorOutputState:
    takes: List[Take] = field(default_factory=list)

@dataclass(kw_only=True)
class TakeGeneratorState:
    topic: str = field(default=None) # Topic 
    context: str = field(default=None) # Context 
    takes: List[Take] = field(default_factory=list)

@dataclass(kw_only=True)
class OverallInputState:
    user_provided_topics: str = field(default="AI") # User-provided topics     

@dataclass(kw_only=True)
class OverallState:
    context: str = field(default=None) # Context    
    user_provided_topics: str = field(default=None) # User-provided topics   
    takes: Annotated[List[Take], operator.add] = field(default_factory=list)

class Topics(BaseModel):
    user_topics: list = Field(None, description="List of user-supplied topics of interest.")
