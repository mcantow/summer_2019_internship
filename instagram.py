#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 09:18:04 2019


@author: michaelcantow


"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.proxy import Proxy, ProxyType
import time
import requests #get html code
from bs4 import BeautifulSoup #parse html code
import random

#driver = webdriver.Chrome('/Users/michaelcantow/Documents/Michael Jerrick Code/chromedriver')

class InstaBot():
    def __init__(self, username, password, targetUserUrl):

        chrome_path = r'/Users/michaelcantow/Documents/Michael Jerrick Code/chromedriver'
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--incognito")

        self.driver = webdriver.Chrome(chrome_path, options=chrome_options)
        self.usernameLOGIN = username
        self.passwordLOGIN = password
        self.targetUsername = targetUserUrl[26:-1]
        self.targetUserUrl = targetUserUrl
#        self.targetUserUrl = 'https://www.instagram.com/' + self.targetUsername + '/'
        
        
    def signIn(self):
        '''
        logs into instagram account. 
        has provision for a pop up and responds by pressing 'not now'
        '''
        self.driver.get('https://www.instagram.com/accounts/login/')
        time.sleep(1) #IMPORTNANT! need to wait for page to load before you do anything
        usernameInput = self.driver.find_element(By.XPATH,'//*[@name="username"]')
        passwordInput = self.driver.find_element(By.XPATH,'//*[@name="password"]')
#        passwordInput = self.driver.find_elements_by_css_selector('form input')[1]
        usernameInput.send_keys(self.usernameLOGIN)
        passwordInput.send_keys(self.passwordLOGIN)
        passwordInput.send_keys(Keys.ENTER)
        time.sleep(2) 
        try:
            notnow = self.driver.find_element(By.XPATH,'//html/body/div[3]/div/div/div[3]/button[2]')
            notnow.click()
        except:
            pass #not now button didn't pop up so ignore error
            
            
        time.sleep(1)
    
            
    def followWithUsername(self):
        '''
        follows user with given username
        '''
        try:
            self.driver.get(self.targetUserUrl)
            time.sleep(1)
            followButton = self.driver.find_element(By.XPATH,'//*[@type="button"]')
            followButton.click()
        except:
            print('Already Following user: ' + username)
        
        
    def getUserData(self):
        '''
        returns list of user data in the form [name, link to profile, numPosts, numFollowers, numFollowing, bio]
        
        '''
        self.driver.get(self.targetUserUrl)
        time.sleep(1)
        
#        name = self.driver.find_element_by_class_name("rhpdm")
#        name = name.text
        
        nameAndBio = self.driver.find_element_by_class_name("-vDIg")
        nameAndBio = nameAndBio.text
        fe = nameAndBio.split('\n')
        try:
            name = fe[0]
        except: 
            name = 'No Name'
        try:
            bio = fe[1]
        except:
            bio = 'No Bio'
#        return nameAndBio
#        bio = bio.text
        
        mainData = self.driver.find_elements_by_class_name("g47SY")
        numPosts = convertSAstringToFloat(mainData[0].text)
        numFollowers = convertSAstringToFloat(mainData[1].text)
        numFollowing = convertSAstringToFloat(mainData[2].text)
#        return([numPosts, numFollowers, numFollowing])
        
        return[name, bio, self.targetUserUrl, numPosts, numFollowers, numFollowing]
        
        
        
#        followData = self.driver.find_elements(By.XPATH,'//*[@class="g47SY lOXF2"]')
#        print(followData)
#    def unfollowWithUsername:
#    def getUserFollowers:
    def closeBrowser(self):
        '''
        closes browser opened when initialized. REMEMBER TO CALL THIS METHOD
        '''
        self.driver.close()
#    def __exit__:

def generateProxy():
    '''
    returns a list of proxy IP address
    '''
    toReturn = []
    
    browser = webdriver.Chrome('/Users/michaelcantow/Documents/Michael Jerrick Code/chromedriver')
    browser.get('https://hidemyna.me/en/proxy-list/')
    time.sleep(10)
    pages = ['https://hidemyna.me/en/proxy-list/']
    for i in range (10) :
        nextPage = 'https://hidemyna.me/en/proxy-list/?start=' + str(64*i)
        pages.append(nextPage)
    for page in pages:
        browser.get(page)
        time.sleep(1)
        adresses = browser.find_elements(By.XPATH,'//*[@id="content-section"]/section[1]/div/table/tbody/tr/td[1]')
        for adress in adresses:
            txt = adress.text
            toReturn.append(txt)
    browser.close()
    
    return toReturn
        
def getFollowersList(user):
    '''
    input: user, a string, full url for desired user
    return: list of follower's full url to their profile
    '''
    print('Getting Followers List...')
    ## open driver
    chrome_path = r'/Users/michaelcantow/Documents/Michael Jerrick Code/chromedriver'
    chrome_options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(chrome_path, options=chrome_options)
    driver.get('https://www.instagram.com/accounts/login/')
    time.sleep(1) #IMPORTNANT! need to wait for page to load before you do anything
    usernameInput = driver.find_element(By.XPATH,'//*[@name="username"]')
    passwordInput = driver.find_element(By.XPATH,'//*[@name="password"]')
    usernameInput.send_keys('owen.kelly__')
    passwordInput.send_keys('Debbie123!')
    passwordInput.send_keys(Keys.ENTER)
    time.sleep(3) 
    try:
        notnow = driver.find_element(By.XPATH,'//html/body/div[3]/div/div/div[3]/button[2]')
        notnow.click()
    except:
        pass #not now button didn't pop up so ignore error
    try: 
        x = driver.find_element(By.XPATH,'/html/body/div/div/div/div/div/button')
        x.click()
    except:
        pass # no followers pop up

    #get data
    driver.get(user)
    mainData = driver.find_elements_by_class_name("g47SY")
    temper = mainData[1].text
    numFollowers = convertSAstringToFloat(temper)
    followersLink = driver.find_element_by_css_selector('ul li a')
    followersLink.click()
    time.sleep(2)
    followersList = driver.find_element_by_css_selector('div[role=\'dialog\'] ul')
    numberOfFollowersInList = len(followersList.find_elements_by_css_selector('li'))
    
    followersList.click()
#    actionChain = webdriver.ActionChains(driver)
    prev = 0
    while (numberOfFollowersInList < numFollowers): #put in num followers for user
#        time.sleep(1)
#        actionChain.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
        actionChain = webdriver.ActionChains(driver)
        actionChain.send_keys(Keys.ARROW_DOWN)
        actionChain.send_keys(Keys.ARROW_DOWN)
        actionChain.send_keys(Keys.ARROW_DOWN)
        actionChain.send_keys(Keys.ARROW_DOWN)
        actionChain.perform()
#        time.sleep(1)
#        time.sleep(2)
        numberOfFollowersInList = len(followersList.find_elements_by_css_selector('li'))
#        print('Scraped ' + str(numberOfFollowersInList/numFollowers*100)[:4] + '% of users')
#        cur =numberOfFollowersInList
#        if cur == prev:
#            time.sleep(10)
#        else:
#            prev = cur
        if numberOfFollowersInList % 100 == 0:
            time.sleep(10)
        print(numberOfFollowersInList)
    
    followers = []
    for user in followersList.find_elements_by_css_selector('li'):
        userLink = user.find_element_by_css_selector('a').get_attribute('href')
        followers.append(userLink)
        if (len(followers) == numFollowers): #put in num followers for user
            break
    print('Finished getting followers list')
    return( followers)
    
def convertSAstringToFloat(SAstr):
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
                
   
    
#bot = InstaBot('owen.kelly__', 'hidingpassword!', 'carolinee08')
#bot.signIn()
#print(bot.getUserData())

#bot.closeBrowser()
#bot.followWithUsername()
    
    
    
    
#### get follower list and export to txt file
followersList = getFollowersList('https://www.instagram.com/Vocal_Creators/')  
with open('test.txt', 'w') as f:
    for item in followersList:
        f.write("%s\n" % item)
    
    
#### read txt file and get user data
with open('test.txt') as f:
    lines = f.read().splitlines()
toScrape = lines

###### Run Scrape #######
scraped_data = []
#InstaBot('owen.kelly__', 'hidepassword,donttry to use my account!', 'https://www.instagram.com/owen.kelly__/').signIn()
counter = 0
prev_perc = 0
for follower in toScrape:
    bot = InstaBot('owen.kelly__', 'Debbie123!', follower)
    data = bot.getUserData()
    scraped_data.append(data)
    bot.closeBrowser()
    counter += 1
    perc_comp = 'Scraping ' + str(counter/len(toScrape) * 100)[0:4] + ' % complete.'
    print('Scraping ' + str(counter/len(toScrape) * 100)[0:4] + ' % complete.' )

with open('exportHere.txt', 'w') as fi:
    for el in scraped_data:
        fi.write("%s\n" % el)


    
#print(convertSAstringToFloat('75.4K'))


#https://www.youtube.com/watch?v=PqSXxrVNpLA here is youtube link for xpath, explained well
