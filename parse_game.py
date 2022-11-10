'''
Created on Jul 4, 2021

@author: rcurtis
'''

import argparse

from utils.activity import activity_check
from utils.reddit_util import reddit

players = []
comment_counts = {}
chat_matrix = {}
chat_totals = {}

def parse_roster(roster_post):
    print('Parsing roster from post: {}'.format(roster_post.title))
    in_roster = False
    for line in roster_post.selftext.splitlines():
        if not in_roster:
            in_roster = ('--- |' in line) or (':-' in line) or ('-:' in line)
            continue
        elif '' == line:
            in_roster = False
            continue
        else:
            if line.strip().startswith('|'):
                line = line.strip()[1:]
            player = line.split('|')[0].replace('/u/', '').replace('u/', '').replace('\\', '').replace('/', '').strip()
            players.append(player)
    print(players)

def init_chat_matrix():
    for respondee in players:
        chat_matrix[respondee.upper()] = {}
        chat_totals[respondee.upper()] = {}
        for responder in players:
            chat_matrix[respondee.upper()][responder.upper()] = 0
            chat_totals[respondee.upper()][responder.upper()] = 0

def process_chat_totals():
    for respondee in players:
        for responder in players:
            chat_totals[respondee.upper()][responder.upper()] = chat_matrix[respondee.upper()][responder.upper()] + chat_matrix[responder.upper()][respondee.upper()]

def handle_post(post):
    print('Processing player comment counts for phase {}'.format(post.title))
    comment_totals = activity_check(post.id, players, chat_matrix)
    for player_comments in comment_totals:
        if player_comments[0] not in comment_counts:
            comment_counts[player_comments[0]] = []
        comment_counts[player_comments[0]].append(player_comments[1])

def export_to_csv(filename):
    csv = open(filename, 'w')
    header_line = 'Player, Total'

    for phase_num in range(0, len(comment_counts[players[0]])):
        header_line += ', Phase {} '.format(phase_num)
    header_line += '\n'
    csv.write(header_line)

    for player in players:
        line = player
        line += ', {}'.format(sum(comment_counts[player]))
        for phase_total in comment_counts[player]:
            line += ',{}'.format(phase_total)
        line += '\n'
        csv.write(line)
    csv.close()

def export_to_markdown(filename):
    markdown = open(filename, 'w')
    header_line = '**Player** | **Total**'
    second_line = ':- | -:'

    for phase_num in range(0, len(comment_counts[players[0]])):
        header_line += '| **Phase {}** '.format(phase_num)
        second_line += '|-:'

    markdown.write(header_line + '\n')
    markdown.write(second_line + '\n')

    for player in players:
        line = 'u/{}'.format(player)
        line += ' | {} '.format(sum(comment_counts[player]))
        for phase_total in comment_counts[player]:
            line += '| {} '.format(phase_total)
        line += '\n'
        markdown.write(line)
    markdown.close()

def dump_chat_matrix_to_csv(filename):
    csv = open(filename, 'w')
    header_line = 'FOO'
    for player in players:
        header_line += ', {}'.format(player)
    csv.write(header_line + '\n')

    for responder in players:
        line = responder
        for respondee in players:
            line += ',{}'.format(chat_totals[respondee.upper()][responder.upper()])
        csv.write(line + '\n')
    csv.close()

def dump_chat_matrix_to_markdown(filename):
    markdown = open(filename, 'w')
    header_line = '**FOO**'
    second_line = ':-'
    for player in players:
        header_line += ' | ' + player
        second_line += ' | -:'

    markdown.write(header_line + '\n')
    markdown.write(second_line + '\n')

    for responder in players:
        line = '**u/{}**'.format(responder)
        for respondee in players:
            line += ' | {} '.format(chat_totals[respondee.upper()][responder.upper()])
        markdown.write(line + '\n')
    markdown.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get the comment counts for a HWW game')
    parser.add_argument('-f', '--flair', help='The flair for the game (e.g.: "Game X.A - 2021")')
    parser.add_argument('-k', '--keyword', help='Title keywords to search for')
    parser.add_argument('-a', '--author', help='Author (game host account) to search for')

    parsed_args = parser.parse_args()
    flair = parsed_args.flair
    keyword = parsed_args.keyword
    author = parsed_args.author
    title = "Output"

    subreddit = reddit.subreddit('hiddenwerewolves')

    game_post_generator = None

    if flair:
        print(flair)
        game_post_generator = subreddit.search(query='flair:"{}"'.format(flair), sort='new', time_filter='month')
        title = flair
    elif keyword:
        game_post_generator = subreddit.search(query='{}'.format(keyword), sort='new', time_filter='month')
        title = keyword
    elif author:
        game_post_generator = subreddit.search(query='author:"{}"'.format(author), sort='new', time_filter='month')
        title = author

    game_posts = []

    for post in game_post_generator:
        print('Found post "{}"'.format(post.title))
        game_posts.append(post)

    # First, find and parse the roster
    roster_found = False
    for post in reversed(game_posts):
        print('Handling "{}"'.format(post.title))
        if not roster_found:
            if 'roster' not in post.title.lower():
                continue
            else:
                roster_found = True
                parse_roster(post)
                break

    if not roster_found:
        print('Could not find roster, quitting')
        quit()

    init_chat_matrix()

    for post in reversed(game_posts):
        if 'Phase' not in post.title and 'Prologue' not in post.title and 'Chapter' not in post.title and 'Dedication' not in post.title:
            continue
        elif 'Wrap' in post.title:
            quit()
        else:
            handle_post(post)

    process_chat_totals()

    export_to_csv('{}.csv'.format(title))
    export_to_markdown('{}.md'.format(title))
    dump_chat_matrix_to_markdown('{}_responses.md'.format(title))
    dump_chat_matrix_to_csv('{}_responses.csv'.format(title))
