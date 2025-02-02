import os
import praw

# Reddit credentials
reddit_client_id = os.getenv("REDDIT_CLIENT_ID")
reddit_client_secret = os.getenv("REDDIT_CLIENT_SECRET")

# Initialize the Reddit instance
reddit = praw.Reddit(
    client_id=reddit_client_id,
    client_secret=reddit_client_secret,
    user_agent="Reddit Agent Loader",
)


# Get reddit posts
def get_recent_reddit_posts(
    subreddit_name,
    filter_to_use,
    number_of_posts,
    number_of_comments,
):
    """
    Retrieve top posts and their comments from a specified subreddit.

    Args:
    subreddit_name (str): Name of the subreddit to fetch posts from.
    filter_to_use (str): Time filter for top posts (e.g., 'day', 'week', 'month', 'year', 'all').
    number_of_posts (int): Number of top posts to retrieve.
    number_of_comments (int): Number of top comments to fetch for each post.

    Returns:
    str: A formatted string containing information about the top posts and their comments.
         Each post entry includes:
         - Post ID
         - Post subreddit
         - Post title
         - Post URL
         - Post score
         - Top comments (up to the specified number) with their scores and ID
         Posts are separated by a line of '=' characters.

    Note:
    This function requires a properly initialized 'reddit' object with necessary permissions.
    """

    # Access the subreddit
    subreddit = reddit.subreddit(subreddit_name)

    # Get top posts based on the specified filter
    top_posts = subreddit.top(time_filter=filter_to_use, limit=number_of_posts)

    # Initialize an empty string to store the output
    reddit_expert_context = ""

    # Process each post
    for post in top_posts:
        reddit_expert_context += f"ID: {post.id}\n"
        reddit_expert_context += f"Subreddit: {subreddit_name}\n"
        reddit_expert_context += f"Title: {post.title}\n"
        reddit_expert_context += f"Source Data URL: {post.url}\n"
        reddit_expert_context += f"Reddit Post URL: {post.shortlink}\n"
        reddit_expert_context += f"Score: {post.score}\n"

        post.comments.replace_more(limit=0)  # Flatten the comment tree

        # Get the specified number of top comments
        for i, comment in enumerate(post.comments[:number_of_comments]):
            reddit_expert_context += f"Top Comment {i+1}: {comment.body}\n"
            reddit_expert_context += f"Comment Score: {comment.score}\n\n"
            reddit_expert_context += f"Comment ID: {comment.id}\n\n"

        reddit_expert_context += "=" * 50 + "\n\n"

    return reddit_expert_context
