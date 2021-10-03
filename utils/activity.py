'''
Created on Jan 2, 2021

@author: rcurtis
'''

from utils.reddit_util import reddit

def activity_check(submission_id, players):
    submission = reddit.submission(id=submission_id)
    top_counts = {}
    child_counts = {}
    totals = []
    
    submission.comments.replace_more(limit=None)
    for comment in submission.comments.list():
        commentor = ''
        try:
            commentor = comment.author.name.upper()
        except:
            continue
            
        if comment.parent_id == comment.link_id:
            # This is a top-level comment
            if commentor in top_counts:
                top_counts[commentor] = top_counts[commentor] + 1
            else:
                top_counts[commentor] = 1
        else:
            if commentor in child_counts:
                child_counts[commentor] = child_counts[commentor] + 1
            else:
                child_counts[commentor] = 1
            
    for player in players:
        top_count = 0
        if player.upper() in top_counts:
            top_count = top_counts[player.upper()]
        child_count = 0
        if player.upper() in child_counts:
            child_count = child_counts[player.upper()]
        total_count = top_count + child_count
        
        totals.append((player, total_count, top_count, child_count))
    
    return totals

def reddit_table(post_id, players):
    counts = activity_check(post_id, players)
    sorted_counts = sorted(counts, key = lambda x : x[0].lower(), reverse = False)
    print('##Comment counts for [Phase](http://redd.it/%s)\n' % post_id)
    # Header row
    print('**Player** | **Total** | **Top-level** | **Child**')
    print(':-|:-|:-|:-')
    for count_data in sorted_counts:
        print('u/%s | %d | %d | %d' % count_data)

def screen_dump(post_id, players):
    counts = activity_check(post_id, players)
    # sorted_counts = sorted(counts, key = lambda x : x[1], reverse = True)
    
    print('For post https://redd.it/%s' % post_id)
    for count_data in counts:
        print('u/%s had %d comments (%d top-level and %d child)' % count_data)

if __name__ == '__main__':
    reddit_table('ol3ui0', ['-Tessa-', 'dawnphoenix', 'DealeyLama', 'Diggsydiggett', 'Disnerding', 'elbowsss', 'HedwigMalfoy', 'KB_black', 'MartinGG99', 'Mathy16', 'Mrrrrh', 'oomps62', 'redpoemage', 'TheLadyMistborn', 'VioletVirtuoso', 'WizKvothe', '-Team-Hufflepuff', 'bigjoe6172', 'birdmanofbombay', 'ElPapo131', 'forsidious', 'kemistreekat', 'Sameri278'])
    