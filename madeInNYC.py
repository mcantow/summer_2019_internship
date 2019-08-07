#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  6 10:31:47 2019

@author: michaelcantow

writing a note to myself

may have utf-8 error when exporting due to non ascii characters in bio
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import gspread#spreadsheet library
from oauth2client.service_account import ServiceAccountCredentials #spreadsheet library
import random 


## setup class
class madeInNYC(): #standard python line for creating a class. 
    def __init__(self, profile): #this is another standard piece of class syntax. __init__ is used to initialize
                        # variables that will be used by methods in the class
        chrome_path = r'/Users/michaelcantow/Documents/Michael-Jerrick-Code/chromedriver' #this is the path where chromedriver.exe lives. The selenium package works by using this executible file. 
        chrome_options = webdriver.ChromeOptions() # we can use this to set some options
#        chrome_options.add_argument("--incognito")
        chrome_options.add_argument("--headless") #headless means that we wont see a chrome browser instance. This is useful since it doesn't load graphics which makes it faster, but it is easier to code this scrape if we leave it commented for now so we can see what the code is actually doing
        self.driver = webdriver.Chrome(chrome_path, options=chrome_options) #create the driver which runs the code. This is an object and has many useful methods as will be demonstrated. 
                # self is a hard concept to understand about classes
                # when something is self and when something isn't self pertains to if you want it to be a general variable which can be called by other methods
        self.profile = profile
        
    def getProfile(self):
        '''
        gets profile for inputed profile
        '''
        self.driver.get(self.profile)
        time.sleep(2)
        
    def scrapeMedia(self):
        '''
        scrapes a the social handles for a user
        
        input: profile, a string for the profile you wish to scrape
        
        returns a list of links [instagram, facebook, twitter, linkedin, pinterest]
        if a social handle is missing sets it to an empty string (neccessary for exporting to sheets)
        '''
        path = '//*[@class="social-link"]'
        try:
            links = self.driver.find_elements(By.XPATH,path) #elements returns a list, path can be any valid path
        except:
            links = []
        socialHandles = [] #empty list to append results to
        for link in links:
            href = link.get_attribute('href') #standard sytax for getting a link saved as href
            socialHandles.append(href)
        #the list socialHandles has all the links for the profile we scraped. 
        #we need to format them according to the description of the function so we 
        #export to sheets correctly
        #ill do this by making variables initialized as empty strings, then modifying these if 
        #there is a matching href in socialHandles
        insta = ''
        twitter = ''
        facebook = ''
        linkedin = ''
        pinterest = ''
        site = ''
        for handle in socialHandles:
            if 'instagram' in handle and insta == '':
                insta += handle
            elif 'twitter' in handle and twitter == '':
                twitter += handle
            elif 'linkedin' in handle and linkedin == '':
                linkedin += handle
            elif 'pinterest' in handle and pinterest == '':
                pinterest += handle
            elif 'facebook' in handle and facebook == '':
                facebook += handle
        try:      
            temp = self.driver.find_element(By.XPATH,'//*[@name="website_visit"]').text #gets text which is where the link lives
            site += temp
        except:
            pass 
        #try and except is for error handling. If there is not link then temp will be none and there will be an error. In this case we just pass.
        
       
        # when you return something never make it a function, will remove a lot of wierd erros
        #ex. dont return [insta, facebook, twitter, linkedin, pinterest]
        toReturn = [insta, facebook, twitter, linkedin, pinterest, site]
        return toReturn
    
    def getNameBio(self):
        '''
        lets implement a method to get the name and bio
        
        returns list [name, bio]
        '''
        namePath = '/html/body/div/article/div/section/div/header/h2' #in text #worth noting which part of html the desired info lives in
        bioPath = '/html/body/div/article/div/section/div/div/div/p' #in text
        name = ''
        bio = ''
        
        nameText = self.driver.find_element(By.XPATH,namePath).text
        try:
            name += nameText
        except: #no name
            pass
    
        bioText = self.driver.find_element(By.XPATH,bioPath).text
        try:
            bio += bioText
        except: #no bio
            pass
        
        res = [name, bio]
        return res
    
    def getEmail(self):
        '''
        gets email for desired user
        
        returns str email
        '''
        email = ''
        emailHref = self.driver.find_element(By.XPATH,'/html/body/div/article/div/section/div/p/a').get_attribute('href')[10:]
        try:
            email += emailHref
        except:
            pass
        
        return email
    
    def scrapeProfile(self):
        '''
        scrapes the given profile for desired attributes
        
        currently does not but will also scrape follower data
        
        returns [name, bio, email, instagramLink, facebookLink, twitterLink, linkedinLink, pinterestLink, instaFollowers, instaFollowing, twitterFollowers, twitterFollowing]
        '''
        self.getProfile()
        media = self.scrapeMedia()
        namebio = self.getNameBio()
        email = self.getEmail()
        ###### code to get twitter and instagram follower data ########
        insta = media[0]
        twitter = media[2]
        
        #get insta data
        instaFollowers = ''
        instaFollowing = ''
        
        if insta != '': #got a result
            try: #incase of bad link
                self.driver.get(insta)
                time.sleep(1)
                mainData = self.driver.find_elements_by_class_name("g47SY")
                numFollowers = convertSAstringToFloat(mainData[1].text)
                numFollowing = convertSAstringToFloat(mainData[2].text)
                instaFollowers = numFollowers
                instaFollowing = numFollowing
            except:
                pass
            
        # get twitter data
        twitterFollowers = ''
        twitterFollowing = ''
        
        if twitter != '':
            try:
                self.driver.get(twitter)
                time.sleep(1)
                twitFollow = convertTwitterstringToFloat(self.driver.find_element(By.XPATH,'//*[@id="page-container"]/div/div/div/div/div/div/div/div/ul/li[3]/a/span[3]').text) 
                twitFollowing = convertTwitterstringToFloat(self.driver.find_element(By.XPATH,'//*[@id="page-container"]/div/div/div/div/div/div/div/div/ul/li[2]/a/span[3]').text) 
                twitterFollowers = twitFollow
                twitterFollowing = twitFollowing
            except:
                pass

        ##### end get follower data #############3
       

        
        res = namebio + [email] + media + [instaFollowers, instaFollowing] + [twitterFollowers, twitterFollowing]
        return res
        
    def closeBrowser(self):
        '''
        closes the self.driver instance initialez in __init__
        '''
        self.driver.close()
        
        
def convertTwitterstringToFloat(SAstr): #plop this function after the class and it can be called within the class
    '''
    seeking alpha for users with following 1k-10k returns this as x,xxx (python doesnt use commas)
    and for users with following 10K plus uses xx.xk to display
    
    this functon convers the seeking alpha string notation to python float so 
    in sheets we can sort nuerically
    
    input: seeking alpha string type
    returns: float of desired number
    '''
    if ',' in SAstr:
        pyFloat = ''
        for i in SAstr:
            if i != ',':
                pyFloat += i
        return float(pyFloat)
    elif 'K' in SAstr: #looks the same as instagram except uses capital, lets see
        temp = ''
        pyFloat = ''
        temp += SAstr[:-1]
        temp += '00'
        if '.' in SAstr:
            for i in temp:
                if i != '.':
                    pyFloat += i
        else:
            for i in temp:
                pyFloat += i
            pyFloat += '0'
        return float(pyFloat)
    else:
        return(float(SAstr))
        
        
def convertSAstringToFloat(SAstr): #plop this function after the class and it can be called within the class
    '''
    seeking alpha for users with following 1k-10k returns this as x,xxx (python doesnt use commas)
    and for users with following 10K plus uses xx.xk to display
    
    this functon convers the seeking alpha string notation to python float so 
    in sheets we can sort nuerically
    
    input: seeking alpha string type
    returns: float of desired number
    '''
    if ',' in SAstr:
        pyFloat = ''
        for i in SAstr:
            if i != ',':
                pyFloat += i
        return float(pyFloat)
    elif 'k' in SAstr:
        temp = ''
        pyFloat = ''
        temp += SAstr[:-1]
        temp += '00'
        if '.' in SAstr:
            for i in temp:
                if i != '.':
                    pyFloat += i
        else:
            for i in temp:
                pyFloat += i
            pyFloat += '0'
        return float(pyFloat)
    else:
        return(float(SAstr))
        
        
def getProfiles(numPerCat):
    '''
    gets a list of profile to scrape
    stores them as a full url
    
    input: int numPerCat, and integer of the number of profiles to scrape per category
                note there are 7 categories so this scrape will return 7 * numPerCat results
                
    returns list of profile to be scraped by madeInNYC class
    '''
    profiles = [] #make empty list to append profiles to
    origins = ['food-beverage/', 'fashion/', 'home-interiors/', 'jewelry/', 'babies-children/', 'print-media/', 'other-cool-stuff/']
    
    for o in origins:
        chrome_path = r'/Users/michaelcantow/Documents/Michael-Jerrick-Code/chromedriver'  
        chrome_options = webdriver.ChromeOptions() 
#        chrome_options.add_argument("--incognito")
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(chrome_path, options=chrome_options) #make a new driver object for each origin, helps prevent some errors
        origin = 'https://madeinnyc.org/consumer-shopping/' + o
        driver.get(origin)
        time.sleep(1)
        mag = driver.find_element(By.XPATH,'//*[@id="search-start"]')
        mag.click()
        time.sleep(0.5)
        x = driver.find_element(By.XPATH,'//*[@id="search-close"]')
        x.click()
        time.sleep(0.5) 
    
    
        localLinks = []
#        while len(localLinks) < numPerCat:
        for i in range(30):
            links = driver.find_elements(By.XPATH,'//*[@id="companies"]/article/a') 
            # check if link has been scraped already then add it 
            for link in links:
                href = link.get_attribute('href')
                if href not in localLinks:
                    localLinks.append(href)
            actions = webdriver.ActionChains(driver) 
            actions.send_keys(Keys.SPACE)
            for i in range(3):
                actions.perform()
                time.sleep(0.5) #need this or it wont work
            
            print (   str((len(localLinks) / numPerCat) * 100)[:4] + ' percent complete')
        driver.close() 
        profiles += localLinks 
    print('Initializing scrape of ' + str(len(profiles)) + ' profiles')
    return (profiles)


def export2dArray(spreadsheet_name, twoDArray):
    '''
    input: name of spreadsheet in google drive to export to
    outpt: none, edits existing spreadsheet in google drive
    '''
    
    scope = ['https://www.googleapis.com/auth/drive']
    name = 'Test-Export-Data-829118260f20.json'#string of name of json file with Google API credentials
    credentials = ServiceAccountCredentials.from_json_keyfile_name(name, scope)
    client = gspread.authorize(credentials)
    sheet = client.open(spreadsheet_name).sheet1
    for row in twoDArray:
        sheet.append_row(row)
        time.sleep(1) 

spreadsheet_name = 'madeInNYC'
#twoDArray = [['Name', 'Email', 'password'], ['John', 'john@gmail.com', 'password1!'], ['hPPY', 'hp@gmail.com', 'password2!']]

#useful to put in some print statements and see where the code is at
print('getting profiles to scrape...')
toScrape = getProfiles(100)
print('scraping profiles....')
twoDArray = [['name', 'bio', 'email', 'instagramLink', 'facebookLink', 'twitterLink', 'linkedinLink', 'pinterestLink', 'site', 'instaFollowers', 'instaFollowing', 'twitterFollowers', 'twitterFollowing', 'profileLink']]#starte this with a row which has the title for each column
for profile in toScrape:
    try:
        bot = madeInNYC(profile) #takes in no variables, initialize a madeInNYC instance 
        bot.getProfile()
        res = bot.scrapeProfile()
        res.append(profile)
        twoDArray.append(res)
        print(str(len(twoDArray)/len(toScrape)*100)[:4] + ' percent complete')
        bot.closeBrowser()
    except:
        pass

try:
    export2dArray(spreadsheet_name, twoDArray)
except:
    with open('investorHunt.txt', 'a') as fi:
        for el in twoDArray:
            fi.write("%s\n" % el)


      
#profile = 'https://madeinnyc.org/company/miakoda/'
#bot = madeInNYC(profile) #takes in no variables, initialize a madeInNYC instance 
#bot.getProfile()

#media = bot.scrapeMedia() #how you call class methods #working   
#print(media) 

#data = bot.getNameBio()
#print(data)

#email = bot.getEmail()
#print(email)
#print(bot.scrapeProfile())

#bot.closeBrowser()   

            
        
        