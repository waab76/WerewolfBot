'''
Created on Dec 21, 2020

@author: rcurtis
'''

import logging

def handle_message(inbox_item):
    if inbox_item.name.startswith("t4"):
        logging.info('Got a private message from %s', inbox_item.author.name)
    else:
        logging.warn('Got an inbox item that is not a message, maybe mention?')