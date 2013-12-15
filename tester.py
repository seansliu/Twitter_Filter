#******************************************************************************
# Sean Liu
# sl3497
# 5/5/2013
# file: tester.py
#
# This program tests the functions in the module tweeter.
#******************************************************************************

import tweeter as t

def main():
    # Phase 1 functions.
    print 'Making tweets...'
    tweets = t.make_tweets('some_tweets.txt')
    print '  Tweets made. \nAdding states and ZIPs...'
    t.add_geo(tweets)
    print '  States and ZIPs added. \nAdding sentiments...'

    # Phase 2 functions.
    t.add_sentiments(tweets)
    print '  Sentiments added. \nWriting to new file...'
    t.write_newtweets(tweets, 'new_tweets.txt')
    print '  File created. \n'
    print 'Filtering tweets. If filter unwanted, do not enter anything.'
    word = raw_input('Word filter: ')
    state = raw_input('State filter: ')
    zip = raw_input('ZIP filter: ')
    ftweets = t.tweet_filter(tweets, word = word, state = state, zip = zip)
    print 'Average sentiment of filtered tweets: ', t.avg_sentiment(ftweets)
    print ''

    # Extra credit below.
    word = raw_input('Most positive state filter word: ')                     
    print t.most_positive(tweets, word = word), '\n'
    word = raw_input('Most negative state filter word: ')                      
    print t.most_negative(tweets, word = word), '\n'

    print 'Testing complete. Thanks!'

main()
