'''
Created on Dec 21, 2020

@author: rcurtis
'''

import logging

def handle_comment(comment):
    logging.info('Handling comment [%s] on submission [%s]', comment.id, comment.submission.id)