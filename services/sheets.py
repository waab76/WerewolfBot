'''
Created on Feb 22, 2021

@author: rcurtis
'''

import gspread
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

        self.sheet = client.open(sheet_name)
     
    def load_codewords(self):
        if None == self.role_sheet:
            self.role_sheet = self.sheet.worksheet('Role List')
        role_records = self.role_sheet.get_all_values()
        codewords = {}
        for role in role_records:
            codewords[role[0]] = role[2].upper()
        return codewords

    def check_codeword(self, user, codeword):
        if None == self.codewords:
            self.codewords = self.load_codewords()
        return codeword.upper() == self.codewords[user].upper()
    
    def get_users(self):
        if None = self.codewords:
            self.codewords = self.load_codewords()
        return self.codewords.keys()
            
    
    def get_votes(self):  
        if None == self.vote_sheet:
            self.vote_sheet = self.sheet.worksheet('Voting')
        return self.vote_sheet.get_all_values()
    
    def get_actions(self):
        if None == self.action_sheet:
            self.action_sheet = self.sheet.worksheet('Actions')
        return self.action_sheet.get_all_values()
