'''
Created on Dec 21, 2020

@author: rcurtis
'''

import logging
import sys
import threading
import time

logging.basicConfig(filename='WolfBot.log', level=logging.INFO, 
                    format='%(asctime)s %(levelname)s %(threadName)s %(module)s:%(funcName)s :: %(message)s ', 
                    datefmt='%m/%d/%Y %I:%M:%S %p')

from prawcore import ServerError
from praw.models.reddit import comment
from praw.models.reddit import submission
from praw.models.util import stream_generator

from handlers.comment_handler import handle_comment
from handlers.message_handler import handle_message
from handlers.submission_handler import handle_submission
from utils.reddit_util import reddit, game_subreddit, wolf_subreddit

logging.info('Connected to Reddit instance as %s', reddit.user.me())

def monitor_submissions(subreddit):
    logging.info('Monitoring submissions for r/%s', subreddit.display_name)
    while True:
        submission_stream = subreddit.stream.submissions()
        try:
            for submission in submission_stream:
                handle_submission(submission)
        except ServerError:
            logging.error('Reddit server is down: %s', sys.exc_info()[0], exc_info=True)
        except Exception:
            logging.error('Error processing submission: %s', sys.exc_info()[0], exc_info=True)

def game_submissions():
    monitor_submissions(game_subreddit)
    
def wolf_submissions():
    monitor_submissions(wolf_subreddit)

def monitor_comments(subreddit):
    while True:
        logging.info('Monitoring comments for r/%s', subreddit.display_name)
        comment_stream = subreddit.stream.comments()
        try:
            for comment in comment_stream:
                handle_comment(comment)
        except ServerError:
            logging.error('Reddit server is down: %s', sys.exc_info()[0], exc_info=True)
        except Exception:
            logging.error('Error processing comment: %s', sys.exc_info()[0], exc_info=True)

def game_comments():
    monitor_comments(game_subreddit)
    
def wolf_comments():
    monitor_comments(wolf_subreddit)
        
def monitor_edits(subreddit):
    while True:
        logging.info('Monitoring r/%s submission and comment edits', subreddit.display_name)
        edited_stream = stream_generator(subreddit.mod.edited, pause_after=0)
        try:
            for item in edited_stream:
                if isinstance(item, comment.Comment):
                    logging.info('Comment [%s] on submission [%s] was edited', item.id, item.submission.id)
                    handle_comment(item)
                elif isinstance(item, submission.Submission):
                    logging.info('Submission [%s] was edited', item.id)
                    handle_submission(item)
                elif item is not None:
                    logging.warn('Unknown edited item type: [%s]', type(item))
        except ServerError:
            logging.error('Reddit server is down: %s', sys.exc_info()[0], exc_info=True)
        except Exception:
            logging.error('Caught exception: %s', sys.exc_info()[0], exc_info=True)

def game_edits():
    monitor_edits(game_subreddit)

def wolf_edits():
    monitor_edits(wolf_subreddit)

def monitor_private_messages():
    while True:
        logging.info('Monitoring inbox of user %s', reddit.user.me())
        inbox_stream = reddit.inbox.stream(pause_after = 0)
        try:
            for inbox_item in reddit.inbox.stream():
                handle_message(inbox_item)
        except ServerError:
            logging.error('Reddit server is down: %s', sys.exc_info()[0], exc_info=True)
        except Exception:
            logging.error('Caught exception: %s', sys.exc_info()[0], exc_info=True)

def periodic_updates(subreddit):
    while True:
        logging.info('Beginning periodic update thread for r/%s', subreddit.display_name)
        try:
            while True:
                time.sleep(60)
                logging.info('Periodic Update thread awake for r/%s', subreddit.display_name)
        except Exception:
            logging.error('Caught exception: %s', sys.exc_info()[0], exc_info=True)

def game_updates():
    periodic_updates(game_subreddit)
    
def wolf_updates():
    periodic_updates(wolf_subreddit)
    

logging.debug('Starting child threads')
threading.Thread(target=game_updates, name='updater:game').start()
threading.Thread(target=game_submissions, name='posts:game').start()
threading.Thread(target=game_comments, name='comments:game').start()
# threading.Thread(target=game_edits, name='edits:game').start()
threading.Thread(target=wolf_updates, name='updater:wolf').start()
threading.Thread(target=wolf_submissions, name='posts:wolf').start()
threading.Thread(target=wolf_comments, name='comments:wolf').start()
# threading.Thread(target=wolf_edits, name='edits:wolf').start()
threading.Thread(target=monitor_private_messages, name='inbox').start()