# Reddit Radar 🎯

Reddit Radar is an AI assistant that keeps you informed about topics that matter to you across Reddit. It intelligently monitors your chosen subreddits, scanning top post content and comments, then distills this information into concise, actionable summaries. These insights are automatically delivered to your Slack workspace, helping you stay on top of relevant conversations without getting lost in the noise.

## 🚀 Quickstart

One option for publishing highlights from Reddit Radar is Slack. Follow the below instructions to set up the Slack webhook for a channel in your workspace. Set the Slack webhook along with other API keys after you clone the repository. Then, launch the assistant [with the LangGraph server](https://langchain-ai.github.io/langgraph/cloud/reference/cli/#dev):
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
git clone https://github.com/langchain-ai/reddit_radar.git
cd reddit_radar
cp .env.example .env
uvx --refresh --from "langgraph-cli[inmem]" --with-editable . --python 3.11 langgraph dev
```

You should see the following output and Studio will open in your browser:

- 🚀 API: http://127.0.0.1:2024
- 🎨 Studio UI: https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024
- 📚 API Docs: http://127.0.0.1:2024/docs

In the `configuration` tab, add the subreddit and, optionally, default topics of interest.  

## Motivation 

Reddit Radar is an AI agent that helps you stay informed about specific topics across Reddit's vast ecosystem. While Reddit organizes discussions into subreddits, the volume of posts and comments can be overwhelming. This tool automatically monitors your chosen subreddits, analyzes discussions for topics you care about, and delivers relevant insights through your preferred channel (Slack, email, etc.). It's like having a personal assistant that reads Reddit for you, focusing only on what matters to you.

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

### Publishing to Slack

Since ambient newfeed agents like Reddit Radar work best when integrated into existing workflows, we publish takes insights directly to Slack. To set up a webhook to publish to Slack:

1. Go to https://api.slack.com/apps
2. Click "Create New App"
3. Choose "From scratch"
4. Name your app (e.g., "Reddit Radar") and select your workspace
5. Once created, go to "Incoming Webhooks" in the left sidebar
6. Toggle "Activate Incoming Webhooks" to On
7. Click "Add New Webhook to Workspace"
8. Choose the channel where you want the messages to appear
9. Copy the "Webhook URL" that's generated

Add add webhook URL credentials to your environment variable `SLACK_WEBHOOK`. 
