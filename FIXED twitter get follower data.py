#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 20 16:42:36 2019

@author: michaelcantow
"""

# -*- coding: utf-8 -*-
"""
this code will activate twitter's api, test to see if it is activated, and retrieve a
2d matrix of the desired data
"""
import time
import tweepy

access_token = "1141426405097578497-8kvMU9pVFZN8u2ffInSjyr0S9mIJJA"
access_token_secret = "4f5v71SWzKAqPR0g5WauMTPtfZeSUOkLovDDnTs5A7OuB"
consumer_key = "visgHX5hhzCAFY3nCmcYEtHvC"
consumer_secret = "NG8w5hwpW2Mz9biH4pmgJqCSIjsH8Cz512oMqnI7LcgYgpGeYx"

def connect_to_twitter_OAuth():
    '''
    creates and returns twitter api object
    '''
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)# Creating the authentication object
    auth.set_access_token(access_token, access_token_secret)# Setting your access token and secret
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)# Creating the API object while passing in auth information
    return api

def printTweets():
    '''
    tester function for access token, run to see if api object was succesfully created
    this function is not useful beyond testing
    '''
    public_tweets = api.home_timeline()
    for tweet in public_tweets:
        print (tweet.text)

def getFollowers(username):
    '''
    input: username for user you are trying to retrieve followers for
    returns: LOL with [name, handle, follwoers, following] heading and 
    cooresponidng data after
    '''
    followersData = [['Users Name', 'Twitter Handle', 'Followers Count', 'Following Count', 'Number of Tweets', 'Bio']]
    followersIDS = api.followers_ids(username) #works for 5000 followers
    totalFollowers = len(followersIDS)
    numIterations = 0
    for follower in followersIDS:
        try:
            followerObject = api.get_user(follower)
            numIterations += 1
            name = str(followerObject.name)
            screenName = str(followerObject.screen_name)
            followers = str(followerObject.followers_count)
            following = str(followerObject.friends_count)
            numTweets = str(followerObject.statuses_count)
            bio = str(followerObject.description)
            followersData.append([name, screenName, followers, following, numTweets, bio])
            
            ##### Following is not neccessary for the function to run,
            ##### it displays user data currently being retrieved and percent complete
#            sanity = ['Name:' + name, 'Handle:' + screenName, 'Followers:' + followers, 'Following:' + following, 'NumTweets:' + numTweets, 'Bio:' + bio]
#            print(sanity)#### line 66 and 67 are to debug
            print('progress:  ' + str((numIterations/ totalFollowers)*100)[0:4] + '%') #display percent complete cuz this runs for so long
            #################################################################
        except:
            pass
    return followersData




        
#### CREATE API OBJECT BEFORE CALLING ANY FUNCTIONS, DO NOT COMMENT OUT#####
api = connect_to_twitter_OAuth()



#####tester functions call to check if api initialized correctly####
#printTweets()



#####GET FOLLOWER DATA FOR USER########
user = 'Vocal_Creators'
#user = 'mcantowmitedu1'
followData2dMatrix= getFollowers(user) ###will yield 2d matrix with heading and data below

print(followData2dMatrix)







#########this code works for get followers function but limited to 20 followers. May be able to get around that######
#########Try new approach and revisit this if it doesnt work#########
#    followerData = []
#    followers = api.followers(username)
#    for follower in followers:
#        name = str(follower.name)
#        screenName = str(follower.screen_name)
#        followers = str(follower.followers_count)
#        following = str(follower.friends_count)
#        followerData.append(['Name:' + name, 'Handle:' + screenName, 'Followers:' + followers, 'Following:' + following])
#    return followerData
    #################################################