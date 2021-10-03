'''
Created on Jul 4, 2021

@author: rcurtis
'''

import sys

from utils.activity import activity_check
from utils.reddit_util import reddit

def parse_roster(roster_post):
    print('Parsing roster from post: {}'.format(roster_post.title))
    in_roster = False
    for line in roster_post.selftext.splitlines():
        if not in_roster:
            in_roster = '--- |' in line
            continue
        elif '' == line:
            in_roster = False
            continue
        else:
            player = line.split(' | ')[0].replace('/u/', '').replace('u/', '').replace('\\', '')
            players.append(player)
    print(players)
    
def handle_post(post):
    print('Processing player comment counts for phase {}'.format(post.title))
    comment_totals = activity_check(post.id, players)
    for player_comments in comment_totals:
        if player_comments[0] not in comment_counts:
            comment_counts[player_comments[0]] = []
        comment_counts[player_comments[0]].append(player_comments[1])
        
def export_to_csv(filename):
    csv = open(filename, 'w')
    for player in players:
        line = player
        for phase_total in comment_counts[player]:
            line += ',{}'.format(phase_total)
        line += '\n'
        csv.write(line)
    csv.close()
    
def export_to_markdown(filename):
    markdown = open(filename, 'w')
    header_line = '**Player**'
    second_line = ':-'
    
    for phase_num in range(0, len(comment_counts[players[0]])):
        header_line += '| Phase {} '.format(phase_num)
        second_line += '|-:'
    
    markdown.write(header_line + '\n')
    markdown.write(second_line + '\n')
    
    for player in players:
        line = player
        for phase_total in comment_counts[player]:
            line += "| {} ".format(phase_total)
        line += '\n'
        markdown.write(line)
    markdown.close()
    
players = []
comment_counts = {}

if __name__ == '__main__':
    subreddit = reddit.subreddit("HogwartsWerewolvesB+HogwartsWerewolvesA+HogwartsWerewolves")
    
    game_post_generator = subreddit.search(query=' '.join(sys.argv[1:]), sort="new", time_filter="all")
    game_posts = []
    
    for post in game_post_generator:
        game_posts.append(post)
    
    roster_found = False
    for post in reversed(game_posts):
        if not roster_found:
            if 'Roster' not in post.title:
                continue
            else:
                roster_found = True
                parse_roster(post)
        elif 'Phase' not in post.title:
            continue
        elif 'Roster' in post.title or 'Wrap' in post.title:
            break
        else:
            handle_post(post)
    
    export_to_csv('{}.csv'.format(' '.join(sys.argv[1:])))
    export_to_markdown('{}.md'.format(' '.join(sys.argv[1:])))