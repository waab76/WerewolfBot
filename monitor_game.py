'''
Created on Feb 5, 2022

@author: rhcurtis
'''

import datetime
import json
import logging
import socket
import sys
import threading
from logging.handlers import TimedRotatingFileHandler

handlers = set()
handlers.add(TimedRotatingFileHandler('HWWMonitor.log',
                                      when='W3',
                                      interval=1,
                                      backupCount=4))

logging.basicConfig(level=logging.INFO, handlers=handlers,
                    format='%(asctime)s %(levelname)s %(threadName)s %(module)s:%(funcName)s %(message)s ')
logging.Formatter.formatTime = (lambda self, record, datefmt=None: datetime.datetime.fromtimestamp(record.created, datetime.timezone.utc).astimezone().isoformat(sep="T",timespec="milliseconds"))

from prawcore import ServerError
from praw.models.reddit import comment
from praw.models.reddit import submission
from praw.models.util import stream_generator
from utils.reddit_util import reddit


logging.info('Connected to Reddit instance as %s', reddit.user.me())
subreddit = reddit.subreddit('HogwartsWerewolvesA+HogwartsWerewolvesB+HogwartsWerewolves')

def monitor_comments():
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

def monitor_edits():
    while True:
        logging.info('Monitoring r/%s edits', subreddit.display_name)
        edited_stream = stream_generator(subreddit.mod.edited, pause_after=0)
        try:
            for item in edited_stream:
                if isinstance(item, comment.Comment):
                    logging.info('Comment [%s] on submission "%s" was edited by %s', item.id, item.submission.title, item.author.name)
                    handle_comment(item, edit=True)
                elif isinstance(item, submission.Submission):
                    logging.info('Submission "%s" was edited by %s', item.title, item.author.name)
                    pass
                elif item is not None:
                    logging.error('Unknown edited item type: %s', type(item))
        except ServerError:
            logging.error('Reddit server is down: %s', sys.exc_info()[0], exc_info=True)
        except Exception:
            logging.error('Caught exception: %s', sys.exc_info()[0], exc_info=True)

def handle_comment(comment, edit=False):
    gelf_object = dict()
    gelf_object['version'] = '1.1'
    gelf_object['host'] = 'HWW'
    gelf_object['short_message'] = 'Comment from {} on {} in {}'.format(comment.author.name, comment.submission.title, comment.submission.subreddit.display_name)
    gelf_object['timestamp'] = comment.edited if comment.edited > 0 else comment.created_utc
    gelf_object['level'] = 1
    gelf_object['_hww_post_title'] = comment.submission.title
    gelf_object['_hww_player'] = comment.author.name
    gelf_object['_hww_comment'] = comment.body
    gelf_object['_hww_comment_id'] = comment.id
    gelf_object['_hww_comment_edited'] = comment.edited > 0
    gelf_object['_hww_subreddit'] = comment.submission.subreddit.display_name
    gelf_object['_hww_game_flair'] = comment.submission.link_flair_text
    gelf_text = '{}\n'.format(json.dumps(gelf_object))
    logging.debug('Submitting GELF message %s', json.dumps(gelf_object))

    host = '192.168.50.200'
    port = 12201
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.sendall(bytes(gelf_text, 'utf-8'))
    s.close()
    logging.debug('GELF message submitted')

logging.debug('Starting child threads')
threading.Thread(target=monitor_comments, name='comments').start()
threading.Thread(target=monitor_edits, name='edits').start()