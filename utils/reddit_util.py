'''
Created on Dec 21, 2020

@author: rcurtis
'''

import logging
import praw

from praw.models import Comment, Submission

bot_name="WolfBot"
user_agent="script:WolfBot:0.1 (by u/BourbonInExile)"

# Create the connection to Reddit.
# This assumes a properly formatted praw.ini file exists:
#   https://praw.readthedocs.io/en/latest/getting_started/configuration/prawini.html
reddit = praw.Reddit(bot_name, user_agent=user_agent)

logging.debug('Logged on to Reddit as [%s]', reddit.user)

# Get a handle on our preferred subreddit
game_subreddit = reddit.subreddit("HogwartsWerewolvesA")
wolf_subreddit = reddit.subreddit("HogwartsWerewolvesB")

def get_submission(post_id):
    return Submission(reddit, post_id)

def get_comment(comment_id):
    return Comment(reddit, comment_id)
