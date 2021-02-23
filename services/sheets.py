'''
Created on Feb 22, 2021

@author: rcurtis
'''

import gspread
import logging
from oauth2client.service_account import ServiceAccountCredentials

class MySheet(object):
    
    sheet = None
    vote_sheet = None
    action_sheet = None
    role_sheet = None
    codewords = None
    
    def __init__(self, sheet_name):
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
        client = gspread.authorize(creds)

        logging.info('Opening Google Sheet [%s]', sheet_name)
        self.sheet = client.open(sheet_name)
     
    def load_codewords(self):
        logging.debug('Loading codewords')
        if None == self.role_sheet:
            logging.info('Loading data from worksheet [Role List]')
            self.role_sheet = self.sheet.worksheet('Role List')
        role_records = self.role_sheet.get_all_values()
        codewords = {}
        for role in role_records:
            codewords[role[0]] = role[2].upper()
        self.codewords = codewords
        logging.debug('Codewords map populated')

    def get_codewords(self):
        logging.debug('Fetching codewords')
        if None == self.codewords:
            self.load_codewords()
        return self.codewords

    def check_codeword(self, user, codeword):
        logging.debug('Codeword check for player [%s]', user)
        if None == self.codewords:
            self.load_codewords()
        return codeword.upper() == self.codewords[user].upper()
    
    def get_users(self):
        logging.debug('Fetching player list')
        if None == self.codewords:
            self.load_codewords()
        users = []
        for user in self.codewords.keys():
            users.append(user)
        return users
            
    def get_votes(self):
        logging.debug('Fetching votes')
        if None == self.vote_sheet:
            logging.info('Loading votes from worksheet [Voting]')
            self.vote_sheet = self.sheet.worksheet('Voting')
        return self.vote_sheet.get_all_values()
    
    def get_actions(self):
        logging.debug('Fetching actions')
        if None == self.action_sheet:
            logging.info('Loading actions from worksheet [Actions]')
            self.action_sheet = self.sheet.worksheet('Actions')
        return self.action_sheet.get_all_values()
