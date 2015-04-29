#!/usr/local/bin/python3.4
# -*- coding: utf-8 -*-

# Author: John Martin

import json
import os
import re

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
            results.append(line.split(', '))
    return results


# -------------------- MASSAGING & FILTERING --------------------

# Prepares tweets for analysis by converting to lower case, removing trivial words, etc.
def massageAndFilter(pythonObject, topic):
    arrayifyText(pythonObject)
    relivantTweets = filterForTopics(pythonObject, topic)
    return relivantTweets

# Turns all of the text fields on tweets into arrays of strings (words), replacing
# the single string that is there originally.
def arrayifyText(pythonObject):
    for item in pythonObject:
        s = item.get("text").lower()
        textArray = ''.join(c for c in s if c not in '!@#$%^&*()-_=+[]{|};:<>,./?1234567890').split()
        item["text"] = textArray


# Return an object of tweets that necessarily contains at least one of the give topics.
def filterForTopics(pythonObject, topic):
    relivantTweets = []
    for item in pythonObject:
        for word in item.get("text"):
            if topic == word:
                relivantTweets.append(item)
                break
    return relivantTweets


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


def main():
    PATH = "./Twitter/tweets/"
    PATHDICGOOD = "./goodwords.txt"
    topicOfInterest = "cat"
    # topicsOfInterest = optimizeTopic(topicOfInterest)

    allTweets = importDirOfTweets(PATH)
    relivantTweets = massageAndFilter(allTweets, topicOfInterest)

    # filteredTweets = filterForTopics(allTweets, topicsOfInterest)

    print(str(len(relivantTweets)) + " of " + str(len(allTweets)) + " are relivent to the topic: " + topicOfInterest)
    likeTweets = countLikedTweets(allTweets)

    print(importWordList(PATHDICGOOD))

    return "finished"


print(main())


# axiom: tweetSet is a set of tweets that certainly pertain to a topic X
#
# for tweet in tweetSet:
#     filter out nonessential words
#     compare remaining words to catalog of known words
#     report on words not cataloged
#     calculate overal sentiment score of -1 to 1
#
# combine scores to calculate a overal sentiment value of the tweets, and consequentially of the topic X
