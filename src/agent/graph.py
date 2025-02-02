import os
import operator

import requests

from langchain_anthropic import ChatAnthropic

from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.runnables import RunnableConfig

from langgraph.constants import Send
from langgraph.graph import END, StateGraph, START


import agent.configuration as configuration
from agent.utils import get_recent_reddit_posts
from agent.prompt import take_instructions, take_format_instructions, topic_instructions
from agent.state import (
    Topics,
    Takes,
    TakeGeneratorState,
    TakeGeneratorOutputState,
    OverallState,
    OverallInputState,
)

# ------------------------------------------------------------
# LLMs

# Anthropic
llm = ChatAnthropic(model="claude-3-5-sonnet-20240620", temperature=0)

# ------------------------------------------------------------
# Graph


def load_context(state: OverallState, config: RunnableConfig):
    """Generate context from Reddit"""

    # Get configuration
    configurable = configuration.Configuration.from_runnable_config(config)
    subreddit_name = configurable.subreddit_name
    reddit_timeframe = configurable.reddit_timeframe
    number_of_posts = configurable.number_of_posts
    number_of_comments = configurable.number_of_comments

    # Pull recent posts
    reddit_recent_posts = get_recent_reddit_posts(
        subreddit_name, reddit_timeframe, number_of_posts, number_of_comments
    )

    return {"context": reddit_recent_posts}


def generate_takes(
    state: TakeGeneratorState, config: RunnableConfig
) -> TakeGeneratorOutputState:
    """Generate takes, format them, and perform a second check on relevance to topic"""

    # Get team
    topic = state.topic
    context = state.context

    # Get configuration
    configurable = configuration.Configuration.from_runnable_config(config)
    user = configurable.user
    subreddit_name = configurable.subreddit_name

    # Instructions
    take_system_promot = take_instructions.format(
        context=context, topic=topic, subreddit_name=subreddit_name, user=user
    )
    take_human_message = (
        "Only generate takes if the news is related to: {topic}".format(topic=topic)
    )

    # Generate takes as an unstructured output
    takes = llm.invoke(
        [SystemMessage(content=take_system_promot)]
        + [HumanMessage(content=take_human_message)]
    )

    # Enforce structured output and perform a second check on relevant to topic
    structured_llm = llm.with_structured_output(Takes)
    take_formatting_system_promot = take_format_instructions.format(
        topic=topic, user=user, context=takes.content, subreddit_name=subreddit_name
    )
    take_formatting_human_message = "Only generate your final, formatted takes if they are relevant to {topic}".format(
        topic=topic
    )

    # Generate takes
    formatted_takes = structured_llm.invoke(
        [SystemMessage(content=take_formatting_system_promot)]
        + [HumanMessage(content=take_formatting_human_message)]
    )

    # Write to state
    return {"takes": [formatted_takes]}


def initiate_all_takes(state: OverallState, config: RunnableConfig):
    """This is the "map" step to initiate takes per topic"""

    # Generate search query
    structured_llm = llm.with_structured_output(Topics)

    # Get topics
    configurable = configuration.Configuration.from_runnable_config(config)

    # Default topics in the configuration file
    default_topics = configurable.topics

    # Any additional topics provided by the user
    topics = state.user_provided_topics

    # Combine default topics with user-provided topics
    all_topics = default_topics + ", " + topics

    # Generate topics to scan the news for
    generated_topics = structured_llm.invoke(
        [SystemMessage(content=topic_instructions)]
        + [HumanMessage(content=f"Here are the user interests: {all_topics}")]
    )

    # Scan the news for each topic
    return [
        Send("generate_takes", TakeGeneratorState(topic=topic, context=state.context))
        for topic in generated_topics.user_topics
    ]


def write_to_slack(state: OverallState):
    """Write takes to Slack"""

    # Full set of interview reports
    takes = state.takes

    # Write to your Slack Channel via webhook
    true = True
    headers = {
        "Content-Type": "application/json",
    }

    # Write to slack
    for t in takes:
        for take in t.takes:

            # Blocks
            blocks = []

            # Block 1: Title section
            blocks.append(
                {
                    "type": "section",
                    "text": {"type": "mrkdwn", "text": f"*{take.title}*"},
                }
            )

            # Block 2: Divider
            blocks.append({"type": "divider"})

            # Block 3: Content section
            blocks.append(
                {"type": "section", "text": {"type": "mrkdwn", "text": f"{take.take}"}}
            )

            # Block 4: Divider
            blocks.append({"type": "divider"})

            # Block 5: Source
            blocks.append(
                {
                    "type": "section",
                    "text": {"type": "mrkdwn", "text": f"Source: {take.source_url}"},
                }
            )

            # Block 6: Divider
            blocks.append({"type": "divider"})

            # Block 7: Reddit post
            blocks.append(
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"Reddit post: {take.reddit_url}",
                    },
                }
            )

            # Block 8: Reddit subreddit
            blocks.append(
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"{take.reddit_subreddit}",
                    },
                }
            )

            # Block 9: Reddit subreddit
            blocks.append(
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"{take.reddit_id}",
                    },
                }
            )

            blocks.insert(
                0,
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": ":fire: :robot_face: Reddit-Radar is heating up ...",
                        "emoji": true,
                    },
                },
            )

            data = {
                "blocks": blocks,
                "unfurl_links": True,
                "unfurl_media": True,
            }

            response = requests.post(
                os.getenv("SLACK_WEBHOOK"), headers=headers, json=data
            )


# Add nodes and edges
overall_builder = StateGraph(
    OverallState, input=OverallInputState, config_schema=configuration.Configuration
)
overall_builder.add_node("load_context", load_context)
overall_builder.add_node("generate_takes", generate_takes)
overall_builder.add_node("write_to_slack", write_to_slack)
# Flow
overall_builder.add_edge(START, "load_context")
overall_builder.add_conditional_edges(
    "load_context", initiate_all_takes, ["generate_takes"]
)
overall_builder.add_edge("generate_takes", "write_to_slack")
overall_builder.add_edge("write_to_slack", END)

# Compile
graph = overall_builder.compile()
