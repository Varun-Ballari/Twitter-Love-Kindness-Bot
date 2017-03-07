#!/usr/bin/env python

import os
import tweepy
from random import randint

# from our keys module (keys.py), import the keys dictionary
from keys import keys

CONSUMER_KEY = os.environ.get('consumer_key')
CONSUMER_SECRET = os.environ.get('consumer_secret')
ACCESS_TOKEN = os.environ.get('access_token')
ACCESS_TOKEN_SECRET = os.environ.get('access_token_secret')

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

search_strings = [
                  ['"@VarunDevAccount"', 'Thanks for tweeting me.'],
                  ['"be kind"', "Thanks for being awesome! I hope you have a great day!"],
                  ['"love each other"', 'You are an awesome person!'],
                  ['"I am sad"', 'You are beautiful and bring joy to so many people. I hope you are ok.']
                 ]
pics = ["1.jpg", "2.jpg", "3.jpg", "4.jpg", "5.jpg"]

for string in search_strings:
    tweet_list = api.search (
        q = string[0],
        count = 5,
        lang = "en"
    )

    # tweet 5 times a cycle
    num_tweets_answered = 0

    for tweet in tweet_list:
        screen_name = tweet.user.screen_name

        # ignore retweets
        if (hasattr(tweet, 'retweeted_status') or 'RT @' in tweet.text or api.me().screen_name == screen_name):
            print "This is a retweet."

        else:
            message = "@{username} {message}".format (
                username = screen_name,
                message = string[1]
            )

            image_path = "media/{image_name}".format(image_name = pics[randint(0, 4)])

            try:
                # following users
                api.create_friendship(screen_name)

                # send messages
                api.update_with_media (filename = image_path, status = message, in_reply_to_status_id = tweet.id)

                num_tweets_answered += 1
                print '{num_tweets_answered} {query}'.format (
                    num_tweets_answered = num_tweets_answered,
                    query = string[0]
                )

                print message

                if num_tweets_answered >= 5:
                    break

            except tweepy.TweepError as e:
                print e
