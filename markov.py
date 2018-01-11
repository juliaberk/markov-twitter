"""Generate Markov text from text files."""

import os
from random import choice
import sys
import string
import twitter

api = twitter.Api(
    consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
    consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
    access_token_key=os.environ['TWITTER_ACCESS_TOKEN_KEY'],
    access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET'])


def open_and_read_files(file_paths):
    """Take file path as string; return text as string.

    Takes a string that is a file path, opens the file, and turns
    the file's contents as one string of text.
    """
    # mashup = []

    with open(file_paths) as f:
        return f.read()

    # with open(file_paths) as f:
    #     mashup.append(f.read())
    # print mashup


def make_chains(text_string):
    """Take input text as string; return dictionary of Markov chains.

    A chain will be a key that consists of a tuple of (word1, word2)
    and the value would be a list of the word(s) that follow those two
    words in the input text.

    For example:

        >>> chains = make_chains("hi there mary hi there juanita")

    Each bigram (except the last) will be a key in chains:

        >>> sorted(chains.keys())
        [('hi', 'there'), ('mary', 'hi'), ('there', 'mary')]

    Each item in chains is a list of all possible following words:

        >>> chains[('hi', 'there')]
        ['mary', 'juanita']

        >>> chains[('there','juanita')]
        [None]
    """
    # code for bi-gram
    # chains = {}

    # words = text_string.split()
    # words.append(None)

    # for i in range(len(words)-2):
    #     key = (words[i], words[i+1])

    #     if chains.get(key):
    #         chains[key].append(words[i+2])
    #     else:
    #         chains[key] = [words[i+2]]

    # return chains

    # code for tri-gram
    chains = {}

    words = text_string.split()
    words.append(None)

    ngram = 3

    for i in range(len(words)-ngram):
        key = []

        for j in range(ngram):
            key.append(words[i+j])
        key = tuple(key)

        if chains.get(key):
            chains[key].append(words[i+ngram])
        else:
            chains[key] = [words[i + ngram]]

    return chains


def make_text(chains):
    """Return text from chains."""

    punct = string.punctuation

    while True:
        ngram = choice(chains.keys())

        if ngram[0][0].isupper():
            break

    words = list(ngram)

    while choice(chains[ngram]):
        # words.extend([ngram[0], ngram[1]])
        new_word = choice(chains[ngram])

        if new_word is None:
            break

        words.append(new_word)

        if new_word[-1] in punct:
            break

        # resetting for bi-gram
        # ngram = (ngram[1], new_word)

        # resetting for tri-gram
        ngram = (ngram[1], ngram[2], new_word)

    # The whole story in a long string
    word_string = " ".join(words)

    # Just the first 140 characters of the story, for our tweet
    tweet_string = word_string[:141]

    # This line is for tweeting Henry:
    # tweet_string = "@SoylentBleen " + word_string[:127]

    return tweet_string


def tweet(chain):
    """Take in chain, output 140 characters and tweet them until user quits"""

    while True:
        status = api.PostUpdate(chain)
        print(status.text)

        user_input = raw_input("Enter to tweet again [q to quit] > ")

        if user_input.lower() == "q":
            break


# input_path = "green-eggs.txt"
input_paths = sys.argv[1]

# Open the file and turn it into one long string
input_text = open_and_read_files(input_paths)

# Get a Markov chain
chains = make_chains(input_text)

# Produce random text
random_text = make_text(chains)

# print random_text
# print(api.VerifyCredentials())

tweet(random_text)
