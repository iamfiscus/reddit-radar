
take_instructions="""Your job is to generate fun, punchy takes on a topic of interest for this subreddit: {subreddit_name}

For each news item, systematically cross-reference it against the topic of interest, topic: {topic}

IMPORTANT: Only generate takes for news that is DIRECTLY related to the topic of interest.

Do not include speculation or information from outside the given news items.

Create a numbered list of takes and format each take as follows:

Include a concise and fun subject line
Start with "Hey {user}:" and then provide a brief summary of the news
Include the exact Source URL of the news item, if provided
Include the exact Reddit post URL of the news item
Provide your reasoning for the take, which confirms that it is relevant to the topic

After generating each take, double-check that it is relevant to the topic.

If no news items are directly related to the topic, explicitly state that no relevant news was found for the topic.

Here are the recent news from the subreddit to base your takes on: 

{context}"""

take_format_instructions="""Your job is to review and then format a final list of fun, punchy takes for a user about a topic of interest from a subreddit: {subreddit_name}.

Review Phase:
1. First, check if any takes are provided in the list of takes. If the list of takes is empty or contains no takes, provide no output and end the process.

2. For each take in the list of takes, verify that:
   a) It is DIRECTLY related to the topic of interest: {topic}
   b) The take is based solely on the information provided within the list of takes.

3. Discard any takes that do not meet ALL of the above criteria.

Here is the list of takes to review:

{context}

---

Formatting Phase:
If any takes remain after the review phase, format each take as follows:

1. Include a concise and fun subject line
2. Start the summary with "Hey {user}:" and then provide a brief summary of the news, focusing only on what is directly stated about the player
3. Include the exact Source URL of the news item, if provided
4. Include the exact Reddit post URL of the news item
5. End with your reasoning for the take, which confirms that the specific player is on the roster of the Fantasy Manager

Final Check:

Before finalizing your response, review ALL formatted takes once more to ensure they meet all criteria.

Ensure that the summary of EACH formatted take starts with "Hey {user}:".

If no takes remain after the review process, provide no output."""

topic_instructions="""Generate a list of topics based upon a user's input."""