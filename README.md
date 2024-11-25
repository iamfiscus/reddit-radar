# Reddit Radar 🎯

Reddit Radar is an AI agent that monitors subreddits for topics you care about, delivering curated insights with community context.

## Quickstart

1. Populate the `.env` file with you Reddit API credentials (see below) and model API key: 
```
$ cp .env.example .env
```

2. Load this folder in [LangGraph Studio](https://github.com/langchain-ai/langgraph-studio?tab=readme-ov-file#download) and run the graph. 

## Motivation 

Keeping up with specific topics across Reddit's vast landscape can be overwhelming. While the platform offers incredible depth of discussion, understanding the community's perspective requires reading through countless posts and comments to gather meaningful context. Reddit Radar eliminates this manual effort, automatically scanning subreddits to deliver the insights you care about.

## Overview

| Phase | Objective | Reddit Radar Implementation |
|-------|-----------|---------------------------|
| Structure | How is the report organized? | Uses LLM to convert user topics into structured Take objects with title, observation, source URLs, and reasoning |
| Research | What are the information sources? | Reddit API (PRAW) to fetch recent posts and top comments from specified subreddits |
| Orchestration | How is report generation managed? | Three-phase LangGraph workflow: 1) Loading Reddit context, 2) Topic analysis and mapping, 3) Parallel insight generation per topic |
| Reporting | How are insights presented? | Generates structured takes in a consistent format with source attribution |
| UX | What is the user interaction pattern? | Ambient (asynchronous) agent where Reddit Radar will run in the background, with insights often published (e.g., to Slack, email, etc.) |

1. `Inputs` - Reddit Radar requires only 2 inputs from users:
   - A set of topics of interest that a user wants to monitor in a given subreddit (this can simply be natural language topics)
   - A subreddit to monitor
   
2. `Topic parsing` - Reddit Radar first uses [tool calling](https://python.langchain.com/docs/concepts/tool_calling/) to convert the user's topics into a structured list of mutually exclusive topics. 

3. `Generation of "takes"` - 
   - Reddit Radar loads the context of the subreddit once
   - It then uses a multi-agent workflow 
   - Each agent is assigned a topic
   - It will generate generate takes, which follow a user-specified structure, for each topic 
   - All takes are published to the same output key in state 

## Setup Details

### Reddit API

Get credentials for Reddit API:

1. Go to [Reddit's App Preferences](https://www.reddit.com/prefs/apps)
2. Click "Create Application" or "Create Another Application"
3. Fill in the following:
   - Name: `reddit-radar` (or any name you prefer)
   - Select "script" as the application type
   - Description: Optional, but helpful for remembering the app's purpose
   - About URL: Can be left blank for personal use
   - Redirect URI: Use `http://localhost:8080`
4. Click "Create app"
5. Once created, you'll see your credentials:
   - Client ID: Found under your app name
   - Client Secret: Listed as "secret"

Add the following credentials to your environment:

* `REDDIT_CLIENT_ID`
* `REDDIT_CLIENT_SECRET`

### Optional: Publishing to Slack

Since ambient agents work best when integrated into existing workflows, we publish the agent's insights directly to Slack where our team already communicates. To set up a webhook to publish to Slack:

1. Go to https://api.slack.com/apps
2. Click "Create New App"
3. Choose "From scratch"
4. Name your app (e.g., "Take Bot") and select your workspace
5. Once created, go to "Incoming Webhooks" in the left sidebar
6. Toggle "Activate Incoming Webhooks" to On
7. Click "Add New Webhook to Workspace"
8. Choose the channel where you want the messages to appear
9. Copy the "Webhook URL" that's generated

Add add webhook URL credentials to your environment:

* `REDDIT_RADAR_SLACK_URL` 

Then, see our notebook for how to run the agent. 

## Testing with the notebook

Create your environment and run the notebook to test the graph and your Slack connection.
```
$ python3 -m venv take-bot-env
$ source take-bot-env/bin/activate
$ pip install -r requirements.txt
$ jupyter notebook
```

## Running Studio 

You can use the [LangGraph Studio](https://github.com/langchain-ai/langgraph-studio) desktop app to run the agent locally (on your own machine). 

To do this, first [download](https://github.com/langchain-ai/langgraph-studio?tab=readme-ov-file#download) the desktop app and have [Docker Desktop](https://docs.docker.com/engine/install/) running. 

Generate your `.env` file with the necessary credentials: 


Load this folder in the Studio app to launch it.