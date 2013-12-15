#******************************************************************************
# Sean Liu
# sl3497
# 5/5/2013
# file: tweeter.py
#
# This program contains useful functions to manage tweet data, add geo data and
# sentiment data to each tweet, as well as filter the tweets.
#******************************************************************************

import datetime as dt
import string
import csv
import math

#******************************************************************************
# Phase 1

def make_tweet(tweet_line):
    """Return a tweet, represented as a python dictionary.
    tweet_line: a string corresponding to a line formatted as in all_tweets.txt

    Dictionary keys:
    text  -- A string; the text of the tweet, all in lowercase
    time  -- A datetime object; the time that the tweet was posted
    lat   -- A number; the latitude of the tweet's location
    lon   -- A number; the longitude of the tweet's location"""
    if tweet_line[0] != '[':
        return None
    tweet = {}
    # Save tweet information into a list.
    tweet_line = tweet_line.strip()
    info = tweet_line.split()
    # Extract location information.
    latitude = float(info[0].strip('[,'))
    longitude = float(info[1].strip(']'))
    # Extract date information.
    date = info[3]
    date = date.replace('-', ' ')
    date = date.split()
    date = [int(x) for x in date]
    tweet_date = dt.date(date[0], date[1], date[2])
    # Extract time information.
    time = info[4]
    time = time.replace(':', ' ')
    time = time.split()
    time = [int(x) for x in time]
    tweet_time = dt.time(time[0], time[1], time[2])
    # Combine date and time.
    when = dt.datetime.combine(tweet_date, tweet_time)
    # Extract tweet message.
    text = ' '.join(info[5:]).lower()
    # Save tweet information into dictionary.
    tweet['lat'] = latitude
    tweet['lon'] = longitude
    tweet['time'] = when
    tweet['text'] = text
    return tweet

def add_tweet(tweet, tweets):
    """Add a tweet to the list of tweets."""
    # Check tweet.
    if tweet != None:
        tweets = tweets.append(tweet)

def make_tweets(filename):
    """Return list of tweet dictionaries from a text file of tweets."""
    tweet_file = open(filename,'r')
    tweets = []
    tweet_line = tweet_file.readline()
    while tweet_line != '':
        tweet = make_tweet(tweet_line)
        add_tweet(tweet, tweets)
        tweet_line = tweet_file.readline()
    return tweets

def tweet_text(tweet):
    """Return the text of a tweet as a string."""
    return tweet['text']

def tweet_words(tweet):
    """Return a list of the words in the tweet's text excluding punctuation."""
    word_list = tweet_text(tweet).split()
    for i in range(len(word_list)):
        word_list[i] = word_list[i].strip(string.punctuation)
    return word_list

def tweet_time(tweet):
    """Return the datetime that represents when the tweet was posted."""
    return tweet['time']

def tweet_location(tweet):
    """Return an tuple that represents the tweet's location."""
    return (tweet['lat'], tweet['lon'])

def tweet_state(tweet):
    """Return the state of the tweet's location."""
    return tweet['state']

def tweet_zip(tweet):
    """Return the nearest zipcode of the tweet."""
    return tweet['zip']

def read_zip(filename):
    '''Return a list of all zip code data stored in csv file.'''
    zip_file = open(filename, 'r')    
    reader = csv.reader(zip_file)
    # Ignore first line, which contains only keys, not data values.
    reader.next()
    zip_list = []
    for line in reader:
        zip_list.append(line)
    return zip_list

def make_zip(zipcode):
    """Return a zip code, represented as a python dictionary.
    zipcode: a list containing a single zip codes data ordered as in zips.csv

    Dictionary keys:
    zip    -- A string; the zip code
    state   -- A string; Two-letter postal code for state
    lat    -- A number; latitude of zip code location
    lon    -- A number; longitude of zip code location
    city   -- A string; name of city assoicated with zip code"""
    for i in range(6):
        zipcode[i] = zipcode[i].strip('" ')
    new_zip = {}
    new_zip['zip'] = zipcode[0]
    new_zip['state'] = zipcode[1]
    new_zip['lat'] = float(zipcode[2])
    new_zip['lon'] = float(zipcode[3])
    # Check whether zip code is actually located in a city.
    if zipcode[4] == '':
        new_zip['city'] = None
    else:
        new_zip['city'] = zipcode[4]
    return new_zip

def add_zips(zipcode, zipcodes):
    """Add a zip code to the list of zip codes."""
    zipcodes = zipcodes.append(zipcode)

def make_zips(filename):
    """Return list of zip code dictionaries from a text file of zip codes."""
    zip_list = read_zip(filename)
    new_ziplist = []
    for zipcode in zip_list:
        new_zip = make_zip(zipcode)
        add_zips(new_zip, new_ziplist)
    return new_ziplist

def zipcode_zip(zipcode):
    """Return the 5-character zip of the zip code."""
    return zipcode['zip']

def zipcode_state(zipcode):
    """Return the state of the zip code."""
    return zipcode['state']

def zipcode_city(zipcode):
    """Return the city of the zip code."""
    return zipcode['city']

def zipcode_location(zipcode):
    """Return an tuple that represents the tweet's location."""
    return (zipcode['lat'], zipcode['lon'])

def geo_distance(loc1,loc2):
    """Return the great circle distance (in miles) between two tuples of
    (latitude, longitude)
    Uses the "haversine" formula.
    http://en.wikipedia.org/wiki/Haversine_formula"""
    # Convert degrees to radians
    lat1 = math.radians(loc1[0])
    lon1 = math.radians(loc1[1])
    lat2 = math.radians(loc2[0])
    lon2 = math.radians(loc2[1])
    # Calculate spherical distance in miles
    radius = 3959   # From http://en.wikipedia.org/wiki/Earth_radius.
    a = math.sin((lat2 - lat1) / 2) ** 2
    b = math.cos(lat1) * math.cos(lat2) * math.sin((lon2 - lon1) / 2) ** 2
    return 2 * radius * math.asin(math.sqrt(a + b))

def find_zip(tweet, zip_list):
    """Return zipcode associated with a tweets location data
    zip_list is a list of zip_cides represented as dictionaries"""
    tweet_loc = tweet_location(tweet)
    zip_loc = zipcode_location(zip_list[0])
    zipcode = zip_list[0]
    min_dist = geo_distance(tweet_loc, zip_loc)
    for x in zip_list:
        zip_loc = zipcode_location(x)
        new_dist = geo_distance(tweet_loc, zip_loc)
        if new_dist < min_dist:
            min_dist = new_dist
            zipcode = x
    return zipcode

def add_geo(tweets):
    """Add the new keys state and zip to each tweet dictionary"""
    zip_list = make_zips('zips.csv')
    for tweet in tweets:
        zipcode = find_zip(tweet, zip_list)
        tweet['zip'] = zipcode_zip(zipcode)
        tweet['state'] = zipcode_state(zipcode)
        
def write_tweets(tweets, filename):
    """Write the list of tweets to a text file with the input filename"""
    outfile = open(filename, 'w')
    header = 'Date, Time, (Location), State, ZIP, "Text" \n'
    outfile.write(header)
    for tweet in tweets:
        # Save all tweet data as strings.
        when = tweet_time(tweet)
        date = str(when.date())
        time = str(when.time())
        loc = str(tweet_location(tweet))
        state = tweet_state(tweet)
        zipcode = tweet_zip(tweet)
        text = '"' + tweet_text(tweet) + '"'
        # Add tweet data strings together and write into text file.
        tweetline = date + ', ' + time + ', ' + loc + ', ' + state + ', ' + \
                    zipcode + ', ' + text + '\n'
        outfile.write(tweetline)
    outfile.close()

#******************************************************************************
# Phase 2

def make_sentiments(filename):
    '''Return a dictionary of words and their sentiments from a csv file.'''
    sents_file = open(filename, 'r')
    reader = csv.reader(sents_file)
    sents = {}
    for sent_line in reader:
        word = sent_line[0]
        sent = float(sent_line[1])
        sents[word] = sent
    return sents

def remove_Nones(values):
    '''Create and return a new list identical to input list without Nones.'''
    new_values = []
    for value in values:
        if value != None:
            new_values.append(value)
    return new_values

def average(values):
    '''Return the average value of a list.'''
    new_values = remove_Nones(values)
    length = len(new_values)
    if length > 0:
        avg = sum(new_values)/float(length)
    else:
        avg = None
    return avg

def calc_sentiment(tweet, sents):
    '''Calculate and return a tweet's sentiment using sentiments dictionary.'''
    word_list = tweet_words(tweet)
    sent_list = []
    # Append each word's sentiment into sent_list.
    for word in word_list:
        if word in sents:
            sent_list.append(sents[word])
    sent = average(sent_list)
    return sent

def add_sentiments(tweets):
    '''Add the sentiments to each tweet in the list of tweets.'''
    sents = make_sentiments('sentiments.csv')
    for tweet in tweets:
        sent = calc_sentiment(tweet, sents)
        tweet['sentiment'] = sent

def tweet_sentiment(tweet):
    '''Return the sentiment of the tweet.'''
    return tweet['sentiment']

def write_newtweets(tweets, filename):
    '''Write the list of tweets to a text file with the input filename'''
    outfile = open(filename, 'w')
    header = 'Date, Time, (Location), State, ZIP, "Text", Sentiment \n'
    outfile.write(header)
    for tweet in tweets:
        # Save all tweet data as strings.
        when = tweet_time(tweet)
        date = str(when.date())
        time = str(when.time())
        loc = str(tweet_location(tweet))
        state = tweet_state(tweet)
        zipcode = tweet_zip(tweet)
        text = '"' + tweet_text(tweet) + '"'
        sent = str(tweet_sentiment(tweet))
        # Add tweet data strings together and write into text file.
        tweetline = date + ', ' + time + ', ' + loc + ', ' + state + ', ' + \
                    zipcode + ', ' + text + ', ' + sent + '\n'
        outfile.write(tweetline)
    outfile.close()
    
def tweet_filter(tweets, **kwargs):
    '''Create and return the list of tweets filtered by the keywords in kwargs.
    word: a single word in the text
    state: the state that the tweet is in
    zip: the zip code of the tweet location'''   
    tweet_list = list(tweets)
    for key in kwargs:
        if kwargs[key] == '':
            kwargs[key] = None
    if 'word' in kwargs and kwargs['word'] != None:
        target_word = kwargs['word'].lower()
        new_list = []
        for tweet in tweet_list:
            word_list = tweet_words(tweet)
            if target_word in word_list:
                new_list.append(tweet)
        tweet_list = new_list
    if 'state' in kwargs and kwargs['state'] != None:
        target_state = kwargs['state'].upper()
        new_list = []
        for tweet in tweet_list:
            state = tweet_state(tweet)
            if target_state == state:
                new_list.append(tweet)
        tweet_list = new_list
    if 'zip' in kwargs and kwargs['zip'] != None:
        target_zip = kwargs['zip']
        new_list = []
        for tweet in tweet_list:
            zip = tweet_zip(tweet)
            if target_zip == zip:
                new_list.append(tweet)
        tweet_list = new_list
    # Check whether filtered list has any tweets remaining.
    length = len(tweet_list)
    if length == 0:
        print 'Sorry, no tweets matched your search.'
        # Empty tweet_list will be returned.
    return tweet_list
    
def avg_sentiment(tweets):
    '''Return the average sentiment of a list of tweets.'''
    sent_list = []
    for tweet in tweets:
        sent = tweet_sentiment(tweet)
        sent_list.append(sent)
    avg_sent = average(sent_list)
    return avg_sent

#******************************************************************************
# Functions written for extra credit

def make_state_sentiments(tweets):
    '''Return a dictionary with state names as keys and a list of sentiments
    of each tweet in that state as the values of those keys.'''
    state_sents = {}
    for tweet in tweets:
        sent = tweet_sentiment(tweet)
        state = tweet_state(tweet)
        if state in state_sents:
            state_sents[state].append(sent)
        else:
            state_sents[state] = [sent]
    return state_sents

def most_positive(tweets, word):
    '''Return a string that is the two-letter postal code for the state
    with the highest average sentiment for tweets containing word.'''
    tweet_list = tweet_filter(tweets, word = word)
    state_sents = make_state_sentiments(tweet_list)
    states = state_sents.keys()
    high_sent = None
    for state in states:
        sent = average(state_sents[state])
        if sent > high_sent:
            high_sent = sent
            pos_state = state
    if high_sent == None:
        pos_state = None
    return pos_state

def most_negative(tweets, word):
    '''Return a string that is the two-letter postal code for the state
    with the lowest average sentiment for tweets containing word.'''
    tweet_list = tweet_filter(tweets, word = word)
    state_sents = make_state_sentiments(tweet_list)
    states = state_sents.keys()
    # Use 2 as ititial value, all floats are greater than None.
    low_sent = 2
    for state in states:
        sent = average(state_sents[state])
        if sent != None and sent < low_sent:
            low_sent = sent
            neg_state = state
    if low_sent == 2:
        neg_state = None
    return neg_state      
