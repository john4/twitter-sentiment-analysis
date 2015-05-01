#!/usr/local/bin/python3.4
# -*- coding: utf-8 -*-

# Author: John Martin

import json
import os
import copy

# -------------------- IMPORTING --------------------

# Returns python object of import tweets, consumes a path to a dir of .json files
def importDirOfTweets(PATH):
    pythonObject = []
    listing = os.listdir(PATH)
    for file in listing:
        if file[-5:] == ".json":
            pythonObject.extend(importJsonOfTweets(PATH + file))
    return pythonObject


def importJsonOfTweets(filePath):
    tweetsImported = 0
    pythonObject = []
    pythonString = open(filePath).read()
    pythonString = pythonString.split('\n\n')
    for line in pythonString:
        tweetsImported+= 1
        try:
            pythonObject.append(json.loads(line))
        except Exception as e:
            print("Issue in file: " + str(filePath) + " at tweet # " + str(tweetsImported) + " : " + str(e))
            tweetsImported-= 1
            continue
    return pythonObject

# Returns python object of imported tweets, consumes a path to .json
def importTweets(PATH):
    tweetsImported = 0
    pythonObject = []
    pythonString = open(PATH).read()
    pythonString = pythonString.split('\n\n')
    for line in pythonString:
        tweetsImported+= 1
        try:
            pythonObject.append(json.loads(line))
        except Exception as e:
            print("Issue at tweet # " + str(tweetsImported) + " : " + str(e))
            tweetsImported-= 1
            continue
    return pythonObject

#---------------------Good Words And Bad Words ------------------

def importWordList(PATH):
    results = []
    with open(PATH) as inputfile:
        for line in inputfile:
            results.append(line.strip('\n'))
    return results


# -------------------- MASSAGING & FILTERING --------------------

# Prepares tweets for analysis by converting to lower case, removing trivial words, etc.
def massageAndFilter(pythonObject, topic):
    arrayifyText(pythonObject)
    relivantTweets = filterForTopics(pythonObject, topic)
    return relivantTweets

# Turns all of the text fields on tweets into arrays of strings (words), replacing
# the single string that is there originally. Also lowercases everything, and
# removes symbols/numbers/etc.
def arrayifyText(pythonObject):
    for item in pythonObject:
        s = item.get("text").lower()
        textArray = ''.join(c for c in s if c not in '!@#$%^&*()-_=+[]{|};:<>,./?1234567890').split()
        item["arrayText"] = textArray

# Return an object of tweets that necessarily contains at least one of the give topics.
def filterForTopics(pythonObject, topic):
    relivantTweets = []
    for item in pythonObject:
        for word in item.get("arrayText"):
            if topic == word:
                relivantTweets.append(item)
                break
    return relivantTweets


# -------------------- ANALYZE --------------------

#  for every good/bad word1 in ever word2 in tweet.text
overallTopicSentiment = 0
numWords = 0
numGoodWords = 0
numBadWords = 0
scoreOfBestTweet = 0
scoreOfWorstTweet = 0

def analyzeGoodnessAndBadness(pythonObject, goodWords, badWords):
    global overallTopicSentiment, numWords, numGoodWords, numBadWords, scoreOfBestTweet, scoreOfWorstTweet

    for item in pythonObject:
        scoreOfThisTweet = 0
        print(item.get("arrayText"))

        for questionableWord in item.get("arrayText"):
            numWords += 1

            for goodWord in goodWords:
                if questionableWord == goodWord:
                    numGoodWords += 1
                    scoreOfThisTweet += 1

            for badWord in badWords:
                if questionableWord == badWord:
                    numBadWords += 1
                    scoreOfThisTweet += -1

        if scoreOfThisTweet > scoreOfBestTweet:
            scoreOfBestTweet = scoreOfThisTweet
        if scoreOfThisTweet < scoreOfWorstTweet:
            scoreOfWorstTweet = scoreOfThisTweet

    overallTopicSentiment = (numGoodWords - numBadWords) / (numGoodWords + numBadWords)


# Returns the number of tweets in the given object that were favorited at least once.
def countLikedTweets(pythonObject):
    likedTweets = 0
    for tweet in pythonObject:
        if "retweet_status" in tweet:
            print("was retweeted or something")
            favCount = tweet.get("retweet_status").get("favorite_count")
            if favCount > 0:
                likedTweets += 1
    print(str(likedTweets) + " of " + str(len(pythonObject)) + " were liked.")
    return likedTweets



# Return a list of strings that are equal to the desired topic string, but with
# optimized formatting for search. ie: "cat" -> [" cat", "cat ", " cat "]
def optimizeTopic(topic):
    return [" " + topic, topic + " ", " " + topic + " "]

def printRelivantTweets(pythonObject):
    for item in pythonObject:
        print (item.get("text"))


def main():
    PATH = "./Twitter/tweets/"
    PATHDICGOOD = "./good-words.txt"
    PATHDICBAD = "./bad-words.txt"
    topicOfInterest = "halo"
    # topicsOfInterest = optimizeTopic(topicOfInterest)

    inputTopicOfInterest = input("Hi there! What single-word topic would you like to analyze for? ")
    if " " in inputTopicOfInterest:
        print("Hmm... seems you've entered something invalid. Using default topic instead.")
    else:
        topicOfInterest = inputTopicOfInterest

    # Import all tweets from .json within the given folder
    print("Importing tweets within " + PATH + " . . .")
    allTweets = importDirOfTweets(PATH)

    # Import word dictionaries
    print("Importing goodword dictionary at " + PATHDICGOOD + " . . .")
    goodWords = importWordList(PATHDICGOOD)

    print("Importing badword dictionary at " + PATHDICBAD + " . . .")
    badWords = importWordList(PATHDICBAD)

    # Manipulate tweets and pull out only relivant ones based on topicOfInterest
    print("Sniffing out tweets about " + topicOfInterest + " . . .")
    relivantTweets = massageAndFilter(allTweets, topicOfInterest)
    print(str(len(relivantTweets)) + " of " + str(len(allTweets)) + " are relivent to the topic: " + topicOfInterest)


    # Analyze
    print("Analyzing all relivant tweets for sentiment . . .")
    analyzeGoodnessAndBadness(relivantTweets, goodWords, badWords)
    print("Analyzed " + str(numWords) + " words, finding " + str(numGoodWords) + " to be good, and " + str(numBadWords) + " to be bad.")
    print("Making for an overall sentiment score of " + str(overallTopicSentiment))

    return 0

main()

# axiom: tweetSet is a set of tweets that certainly pertain to a topic X
#
# for tweet in tweetSet:
#     filter out nonessential words
#     compare remaining words to catalog of known words
#     report on words not cataloged
#     calculate overal sentiment score of -1 to 1
#
# combine scores to calculate a overal sentiment value of the tweets, and consequentially of the topic X
