'''
Created on Dec 21, 2020

@author: rcurtis
'''

import logging

def handle_submission(submission):
    if (submission.locked):
        logging.info('Submssion [%s] is locked.  Skipping', submission.id)
    else:
        logging.info('Handling submission [%s]', submission.id)