Shih-Chun Liu sl3497

1. How to use this program.
With your tweets text file, 'zips.csv', and 'sentiments.csv' in the same 
folder as 'tweeter.py', run the 'tweeter.py' module, or import it in another 
program to run in the Python Shell and use the functions written in the 
code. To test the module, you may run 'tester.py' in the Python Shell and
follow the instructions.

2. Design decisions.
This section of the module continues to operate on the tweets list of tweet
dictionaries from assignment 6A.
I split the assignment into the following functions:
-make_sentiments
	This iterates through every line of 'sentiments.csv', saving into the 
	sentiments dictionary the word as a key and the float as the 
	sentiment value for that key.
-remove_Nones
	This function comes in useful for calculating the average value in a 
	list, since sum(list) will not work if None is in the list.
-average
	I wrote this because a lot of these sentiment functions need to 
	calculate the average of a list of sentiments.
-calc_sentiment
	This uses tweets_words from 6A to create a list of the words in a
	tweet, then appends each word's sentiment into a separate list of
	sentiments, and plugs this list into the average function to find 
	and return the tweet sentiment.
-add_sentiments
	This performs make_sentiments, then iterates through the tweets list
	and adds the sentiment to each tweet after using calc_sentiment.
-tweet_sentiment
	Like the one-liner functions from 6A, this returns the sentiment of
	a tweet input.
-write_newtweets
	Same as write_tweets from 6A, with sentiments added.
-tweet_filter
	If any of the keys' value in kwargs is an empty string, this function
	replaces that value with None.
	This first creates a copy of the tweets list. Then it checks whether 
	each key is in kwargs and whether the value associated with that key 
	is None, then creates a new list and appends the appropriate tweets 
	to that list, leaving out the tweets that are filtered out. It 
	continues to filter the new list until finished, and then returns the 
	new filtered list. For word and state, I made sure to lowercase the
	word and uppercase the state before filtering, just in case the user
	is not consistent with the expected input. 
-avg_sentiment
	This saves the sentiment of each tweet into a new list, then plugs
	that new list into average and returns that average tweets sentiment.
-make_state_sentiments
	This function comes in useful for the extra credit functions. It 
	iterates through tweets, adding each state as a dictionary key and 
	the sentiments of tweets from that state into a list whose key is 
	the state. Then it returns the state:[sentiments] dictionary.
-most_positive
	This first filters tweets for the given word, then uses 
	make_state_sentiments to create a state:[sentiments] dictionary for
	that filtered list. Then it sets an initial sentiment of None and
	iterates through each list in that dictionary, calculating and saving 
	the highest average sentiment and state of that highest average 
	sentiment. If there are only sentiment values of None, then it sets
	the most positive state to None. Then it returns that state.
-most_negative
       	This works the same as most_positive; however, I used an initial value
	of 2 instead of None because all floats have greater values than None.

3. Conclusions.
While operations with word sentiments are practical, what I have done is
limited to the 'sentiments.csv' file. This program would be more useful if I
could also add and update the 'sentiments.csv' file to account for words that
do not have sentiments saved in that file. Also, another limitation is 
singular vs plural words--they show up as different words in the way I have
coded. Furthermore, **kwargs opens up many more creative ways to write 
functions.