import logging
import sys

from services.sheets import MySheet
from utils.votes import tabulate_votes

logging.basicConfig(filename='PhaseTurnover.log', level=logging.INFO, 
                    format='%(asctime)s %(levelname)s %(threadName)s %(module)s:%(funcName)s :: %(message)s ', 
                    datefmt='%m/%d/%Y %I:%M:%S %p')


def handle_turnover(phase):
    illuminatus_sheet = MySheet('Illuminatus! Test Sheet')
    
    do_actions(illuminatus_sheet, phase)
    
    do_items(illuminatus_sheet, phase)
    
    do_votes(illuminatus_sheet, phase)

def do_votes(sheet, phase):
    votes_received, inactive = tabulate_votes(sheet, phase)
    for target in votes_received.keys():
        print('%s received %s votes: %s' % (target, len(votes_received[target]), votes_received[target]))
    print('Non-voting players: %s' % inactive)
    
def do_actions(sheet, phase):
    print('No actions for phase [%s]' % phase)

def do_items(sheet, phase):
    print('No items for phase [%s]' % phase)

    
if __name__ == "__main__":
    phase = sys.argv[1]
    handle_turnover(phase)