'''
Created on Feb 22, 2021

@author: rcurtis
'''

import logging

def tabulate_votes(sheet, phase):
    logging.info('Tabulating vote for phase [%s]', phase)
    
    vote_records = sheet.get_votes()
    inactive_players = sheet.get_users()
    
    logging.debug('Processing individual votes_cast')
    votes_cast = dict()
    for vote_record in vote_records:
        if vote_record[1] == phase:
            voter = vote_record[2]
            if sheet.check_codeword(voter, vote_record[3]):
                logging.info('%s voted for %s', voter, vote_record[4])
                votes_cast[voter] = vote_record[4]
                if voter in inactive_players:
                    inactive_players.remove(voter)
            else:
                logging.warn('Invalid codeword for [%s]', voter)
        else:
            logging.debug('Skipping vote from wrong phase')
            
    logging.info('No votes_cast from %s in phase [%s]', inactive_players, phase)

    logging.debug('Compiling final votes_cast')
    votes_received = dict()
    for voter in votes_cast.keys():
        if votes_cast[voter] not in votes_received:
            votes_received[votes_cast[voter]] = []
            votes_received[votes_cast[voter]].append(voter)
        else:
            votes_received[votes_cast[voter]].append(voter)
    
    logging.info('Votes for phase [%s]:', phase)
    for target in votes_received.keys():
        logging.info('%s received %s votes: %s', target, len(votes_received[target]), votes_received[target])
    
    return votes_received, inactive_players