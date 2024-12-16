import os
from dataclasses import dataclass, field, fields
from typing import Any, Optional

from langchain_core.runnables import RunnableConfig
from typing_extensions import Annotated
from dataclasses import dataclass

@dataclass(kw_only=True)
class Configuration:
    """The configurable fields for the Reddit Radar."""
    user: str = "@rlm"
    subreddit_name: str = "LocalLLaMA" 
    topics: str = "New models, local LLM use-cases" 
    reddit_timeframe: str = "day" # Time filter for top posts
    number_of_posts: int = 20 # Number of top posts to retrieve
    number_of_comments: int = 3 # Number of top comments to fetch for each post

    @classmethod
    def from_runnable_config(
        cls, config: Optional[RunnableConfig] = None
    ) -> "Configuration":
        """Create a Configuration instance from a RunnableConfig."""
        configurable = (
            config["configurable"] if config and "configurable" in config else {}
        )
        values: dict[str, Any] = {
            f.name: os.environ.get(f.name.upper(), configurable.get(f.name))
            for f in fields(cls)
            if f.init
        }
        return cls(**{k: v for k, v in values.items() if v})