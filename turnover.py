import logging
import sys

from services.sheets import MySheet
from utils.votes import tabulate_votes

logging.basicConfig(filename='Turnover.log', level=logging.INFO, 
                    format='%(asctime)s %(levelname)s %(threadName)s %(module)s:%(funcName)s :: %(message)s ', 
                    datefmt='%m/%d/%Y %I:%M:%S %p')


def handle_turnover(phase):
    illuminatus_sheet = MySheet('Illuminatus! Test Sheet')
    votes = tabulate_votes(illuminatus_sheet, phase)
    for votee in votes.keys():
        print('%s received %s votes: %s' %(votee, len(votes[votee]), votes[votee]))
    
if __name__ == "__main__":
    phase = sys.argv[1]
    handle_turnover(phase)