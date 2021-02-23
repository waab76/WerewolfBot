'''
Created on Feb 22, 2021

@author: rcurtis
'''

def tabulate_votes(sheet, phase):
    vote_records = sheet.get_votes()
    votes = dict()
    for vote_record in vote_records:
        if vote_record[1] == phase:
            voter = vote_record[2]
            if sheet.check_codeword(voter, vote_record[3]):
                votes[voter] = vote_record[4]
            else:
                print('Invalid codeword for [%s]' % voter)
        else:
            pass

    votes_for = dict()
    for voter in votes.keys():
        if votes[voter] not in votes_for:
            votes_for[votes[voter]] = []
            votes_for[votes[voter]].append(voter)
        else:
            votes_for[votes[voter]].append(voter)
    
    return votes_for