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
    sorted_counts = sorted(counts, key = lambda x : x[1], reverse = True)
    print('##Comment counts for [Phase 4](http://redd.it/%s)\n' % post_id)
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
    reddit_table('kraq3q', ['-Tessa-', 'AmericaJohnLine', 'billiefish', 
                              'blxckfire', 'dawnphoenix', 'DealeyLama', 'Dirtymarteeny', 
                              'Epolur77', 'ICantReachTheOctave', 
                              'Infinite_Zone_0868', 'Keight07', 
                              'KeiratheUnicorn', 'Larixon', 'laughterislouder', 'meddleofmycause', 
                              'OiHaveABiscuit', 'saraberry12', 
                              'swqmb2', 'Tacochel', 'TalkNerdyToMe20', 
                              'Tipsytippett'])
    print('\n\n## Previous Phase Data')
    print('* [Phase 4](https://www.reddit.com/r/hogwartswerewolvesA/comments/kspjhu/devoctrices_of_destiny_phase_5_dinna_fash_yersel/gihjz5w?utm_source=share&utm_medium=web2x&context=3)')
    print('* [Phase 3](https://www.reddit.com/r/hogwartswerewolvesA/comments/kraq3q/devoctrices_of_destiny_phase_4_its_hedwog_tyvm/gic39d7/?context=3)')
    print('* [Phase 2](https://www.reddit.com/r/hogwartswerewolvesA/comments/kqktf3/devoctrices_of_destiny_phase_3_k9s_cards_giveth/gi4e9bm?utm_source=share&utm_medium=web2x&context=3)')
    print('* [Phase 1](https://www.reddit.com/r/hogwartswerewolvesA/comments/kpvnmy/devoctrices_of_destiny_phase_2_i_am_9999_certain/gi2g60z?utm_source=share&utm_medium=web2x&context=3)')
    print('* [Phase 0](https://www.reddit.com/r/hogwartswerewolvesA/comments/kp8fuq/devoctrices_of_destiny_phase_1_sleep_is_always/ghya8hp?utm_source=share&utm_medium=web2x&context=3)')
    