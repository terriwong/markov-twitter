import os
import sys
from random import choice
import twitter

api = twitter.Api(
        consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
        consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
        access_token_key=os.environ['TWITTER_ACCESS_TOKEN_KEY'],
        access_token_secret=os.environ["TWITTER_ACCESS_TOKEN_SECRET"])

print api.VerifyCredentials()



def open_and_read_file(filenames):
    """Given a list of files, open them, read the text, and return one long
        string."""

    body = ""

    for filename in filenames:
        text_file = open(filename)
        body = body + text_file.read()
        text_file.close()

    return body


def make_chains(text_string):
    """Takes input text as string; returns dictionary of markov chains."""

    chains = {}

    words = text_string.split()

    for i in range(len(words) - 2):
        key = (words[i], words[i + 1])
        value = words[i + 2]

        if key not in chains:
            chains[key] = []

        chains[key].append(value)

        # or we could replace the last three lines with:
        #    chains.setdefault(key, []).append(value)

    return chains


def make_text(chains):
    """Takes dictionary of markov chains; returns random text."""

    key = choice(chains.keys())
    # words = [key[0], key[1]]
    sentence = key[0] + " " + key[1]

    while key in chains and len(sentence) <= 140: #the other way to limit the 140 char, is to slice the text before tweeting out.
        # Keep looping until we have a key that isn't in the chains
        # (which would mean it was the end of our original text)
        #
        # Note that for long texts (like a full book), this might mean
        # it would run for a very long time.

        word = choice(chains[key])
        sentence = sentence + " " + word
        # words.append(word)
        key = (key[1], word)

    if len(sentence) > 140:
        sentence = sentence[:140]

    return sentence


def tweet(chains):
   
    status = api.PostUpdate(chains)
    print status.text
    
    # Use Python os.environ to get at environmental variables
    # Note: you must run `source secrets.sh` before running this file
    # to make sure these environmental variables are set.
    # pass

def read_most_recent_tweet(user_id):

    statuses = api.GetUserTimeline(user_id)
    print "The most recent tweet: ", statuses[0].text

# return ()

# Get the filenames from the user through a command line prompt, ex:
# python markov.py green-eggs.txt shakespeare.txt
filenames = sys.argv[1:]

# Open the files and turn them into one long string
text = open_and_read_file(filenames)

# Get a Markov chain
chains = make_chains(text)

# Generate text as tweet
new_tweet = make_text(chains)

# Print the most recent tweet
read_most_recent_tweet("Pat")

# Your task is to write a new function tweet, that will take chains as input
tweet(new_tweet)