#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 15:38:06 2019

@author: michaelcantow

A brief introduction to webscraping in selenium




first scrape is a couple of lines to familiarze youself with how selenium works




second scrape is a class to scrape twitter profiles and a function to scrape profile links
this gives an idea of how selenium scrapes can be neatly structured in Python

"""



#### Lets start by importing the libraries we will need. This can be copied and pasted for each scrape ####

from selenium import webdriver
from selenium.webdriver.common.by import By
#from selenium.webdriver.common.keys import Keys #wont use in this document but this allows you to automate the keyboard.
import time





################################################
################# first scrape #################
################################################

## shows how to find elements by XPath and pull data from text or href attributes of resulting HTML blocks ##
##  for instagram home page ##




###     make webdriver object, needs to be done to use webdriver  #####

#chrome_path = r'/Users/michaelcantow/Documents/Michael-Jerrick-Code/chromedriver' # this is the path to chromedriver executible which selenium is built on
#driver = webdriver.Chrome(chrome_path) #make driver object
#driver.get('http://instagram.com')# navigate to instagram
#time.sleep(1) #allow page to load, VERY IMPORTANT





##### pull "Sign up to see photos and videos from your friends."  ####

#targetXPath = '//*[@class="vvzhL "]'
#targetHTML = driver.find_element(By.XPATH,targetXPath) #gets HTML block for targetXPath
#target = targetHTML.text #pulls text from HTML block
#print(target) #prints the text in the console on the right






#### pull the link to the sign in page, in less code. Notice this is in the href attribute, not text ###

#print(driver.find_element(By.XPATH,'//*[@class="izU2O"]/a').get_attribute('href'))





###########################################################
################## end first scrape #######################
###########################################################













################## second scrape ####################

#now we will construct a simple profile scraper class for a twitter profile
class twitter():
    def __init__(self, profile):
        '''
        good coding practice: writng a description under a method or function makes code much more readable and helps your future self
        
        __init__ is a reserved method in python used to initialize variables
        '''
        
        chrome_path = r'/Users/michaelcantow/Documents/Michael-Jerrick-Code/chromedriver'
        
        ############## for headless scraping #########################3
#        chrome_options = webdriver.ChromeOptions()
#        chrome_options.add_argument("--incognito")
#        chrome_options.add_argument("--headless")
#        self.driver = webdriver.Chrome(chrome_path, options= chrome_options) 
        #############################################################
        
        ## for demo ##
        self.driver = webdriver.Chrome(chrome_path)
        self.url = 'http://twitter.com/' + profile
        self.driver.get(self.url)
        time.sleep(2)
        
    def getMetaData(self):
        '''
        returns list of [profileLink, tweets, following, followers]
        
        tried to write this method as readable as possible
        '''
        
        ### start by inspecting element and getting XPaths for attributes we want to scrape ###
        ### I like this style since it clusters similar tasks, ie you get all the XPaths you need in one step##
        ### then use those XPaths to extract desired data in one step, then return result#####
        
        
        tweetsPath = '//*[@data-nav="tweets"]/span[3]' #its helpful when writing a lot of XPaths to write a note of if the ultimate data you want is in text or href. this is in text
        followingPath = '//*[@id="page-container"]/div/div/div/div/div/div/div/div/ul/li[2]/a/span[3]' #in text
        followersPath = '//*[@id="page-container"]/div/div/div/div/div/div/div/div/ul/li[3]/a/span[3]' #in text
        ## side note: in XPath /text() or /@href is a valid extention, but doing this will make selenium unable to find the element ##
        ## this is because selenium was built for testing webpages, not neccesarily scraping. ###
        
        
        ### gets the HTML for the elements we are interested in and pulls the text ###
        tweets = self.driver.find_element(By.XPATH,tweetsPath).text
        following = self.driver.find_element(By.XPATH,followingPath).text
        followers = self.driver.find_element(By.XPATH,followersPath).text
        
        # build the list we want to return
        res = [self.url, tweets, following, followers] #note that twitter formats numbers differently than python (in twitter 23000 is 23k and 2300 is 2,300), so we cant just divide to get ratio
                                            #this is a good example of why coding experience is important, this is hard if you don't know what you are doing but very easy for a programmer
        #return the result
        return res
    
    def getBio(self):
        '''
        returns the bio for profile as a str  
        this method is less readable, but shows how to combine lines
        '''
        return self.driver.find_element(By.XPATH,'//*[@id="page-container"]/div/div/div/div/div/div/div/div/p').text
    
    def scrapeProfile(self):
        '''
        call to scrape a profile
        
        returns list of [profileLink, tweets, following, followers, bio]
        '''
        ## standard syntax for calling methods within a class ##
        data = self.getMetaData()
        bio = self.getBio()
        
        ## getBio method returns a str and getMetaData returns a list, so this line combines them ##
        temp = data + [bio]
        
        ## close driver at the end to prevent an absurd amount of open chrome windows ##
        self.driver.close()
        
        return temp
    



################ test calls on twitter class methods ##################
    
#### This is the advantage of structuring your code in a class, it is easy to test components and debug ##
        
    
#data = twitter('realDonaldTrump').getMetaData()
#print(data)

#bio = twitter('realDonaldTrump').getBio()
#print(bio)

#scrape = twitter('realDonaldTrump').scrapeProfile()
#print(scrape)
        
################# end test calls ######################################








        
############ now lets write a function to get some profiles to scrape ##################
        
## https://en.wikipedia.org/wiki/List_of_most-followed_Twitter_accounts is a list of the 50 most followed twitter accounts       
## This function will pull profile names from that page ##
        
def scrapePorfiles():
    '''
    goes to 
    https://en.wikipedia.org/wiki/List_of_most-followed_Twitter_accounts 
    
    returns a list of the 50 most followed twitter accounts
    '''   
    ## create driver object ##
    chrome_path = r'/Users/michaelcantow/Documents/Michael-Jerrick-Code/chromedriver'
    driver = webdriver.Chrome(chrome_path) 
    driver.get('https://en.wikipedia.org/wiki/List_of_most-followed_Twitter_accounts')
    time.sleep(2)
    ###########################
    
    profiles = [] #empty list to append profiles to
    
    names = driver.find_elements(By.XPATH,'//*[@id="mw-content-text"]/div/table/tbody/tr/td[3]') #genearl XPath for all usernames, makes name variable which is a list of HTML blocks
    for name in names:
#        profiles.append(name.text)  # pull text from blocks of HTML
        profiles.append(name.text[1:]) #profiles are returned as @username, so we need to slice the string to remove that symbol
        
    return profiles

#print(scrapePorfiles()) #test function
    









####### now we have a twitter class that scrapes individual profiles ########3
####### and a scrapeProfiles function to get profiles to scrape    #########3#

######## the function below, runScrape, puts these components together and completes the scrape ######

def runScrape():
    '''
    function to control the entire scrape. Returns 2DArray(list of lists) with results of scrape
    '''
    profiles = scrapePorfiles() #calls function that gets a list of profiles
    twoDArray = [['profileLink', 'tweets', 'following', 'followers', 'bio']] #make 2D array to append results to, initialize it with the heading for each attribut so the columns have titles in the spreadhseet
    for profile in profiles:
        try: 
            bot = twitter(profile)
            res = bot.scrapeProfile()
            twoDArray.append(res)
        except:
            pass
    return twoDArray




'''
for the purposes of this demo, we will just print the results in console
The result is a 2D Array, which can easily be exported to Google Sheets
    


in spreadsheetsGoogleDrive.py  i wrote notes to myself on how to set up the google drive API
that file also has the code to import/export data                 


                   
If that file doesn't explain it well i'm pretty sure I used this video  :   
            https://www.youtube.com/watch?v=vISRn5qFrkM 
'''    






####### this is how to call the scrape and print the result in console ##########3
    
#print(runScrape())

names  = ['michael','kyle']
print(random.choice(names))
        
        
        
        
        
        
        
        
