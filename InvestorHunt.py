#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 12:48:02 2019

@author: michaelcantow
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
#from bs4 import BeautifulSoup #parse html code
#import requests #get html code
import gspread#spreadsheet library
from oauth2client.service_account import ServiceAccountCredentials #spreadsheet library
#from lxml import etree
import random 
import codecs
import ast

class InvestorHunt():
    def __init__(self, username, password):
        self.username = username
        self.password a= password
        chrome_path = r'/Users/michaelcantow/Documents/Michael-Jerrick-Code/chromedriver'
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--incognito")
#        chrome_options.add_argument("--headless") #throws error in headless rn
        self.driver = webdriver.Chrome(chrome_path, options=chrome_options) 
        
    def login(self):
        self.driver.get('https://investorhunt.co/users/sign_in')
        time.sleep(1)
        usernameInput = self.driver.find_element(By.XPATH,'//*[@id="user_email"]')
        passwordInput = self.driver.find_element(By.XPATH,'//*[@id="user_password"]')
        usernameInput.send_keys(self.username)
        passwordInput.send_keys(self.password)
        passwordInput.send_keys(Keys.ENTER)
        
    def setScrapeParameters(self, focus, location):
        '''
        Sets Scrape parameters since the data base only posts 2000 results and we want all 40,000(must conduct multiple scrapes)
        Should be controlled by a caller function iterating through all the investments focus and location combinations(one at a time)
        
        Input: str focus. The investment focus to set for the scrape. Possible options:
                                    Mobile 
                                    Consumer Internet
                                    Enterprise Software
                                    SaaS
                                    ECommerce
                                    Social Media
                                    Marketplaces
                                    Digital Media
              str location. The location for a given focus to scrape. Possible options:
                                    San Francisco
                                    New York City
                                    Los Angeles
                                    London
                                    Silicon Valley
                                    New York
                                    Boston
                                    California
                                    United States
                                    Palo Alto
        '''
        #### set focus for scrape### 
        self.driver.get('https://investorhunt.co/dashboard')
        time.sleep(1)
        focpath = '//*[@value="%s"]' %focus
        foc = self.driver.find_element(By.XPATH,focpath)
        foc.click()
        time.sleep(1)
        
        ### set locations ###
        actions = webdriver.ActionChains(self.driver) #need to get buttons into display for them to be clickable
        actions.send_keys(Keys.ARROW_DOWN)
        for i in range(7):
            actions.perform()
            time.sleep(0.5)
            
        path = '//*[@value="%s"]' %location
        loc = self.driver.find_element(By.XPATH,path)
        loc.click()
        time.sleep(2)
        
        ### set email; only want investors with an email### 
        email = self.driver.find_element(By.XPATH,'//*[@value="Has email"]')
        email.click()
        time.sleep(2)
        
    def runScrape(self):
        '''
        once parameters are set, this function runs a full scrape of the results
        returns LOL
        '''
        queryResult = [['name', 'location', 'company', 'focuses', 'investments', 'email', 'twitter', 'linkedin']]
        #### get bound ####
        actions = webdriver.ActionChains(self.driver) #prevents unclickable button error
        actions.send_keys(Keys.SPACE)
        for z in range(4):
            actions.perform()   #navigate display to next page button 
            time.sleep(1)
        end = self.driver.find_element(By.XPATH,'//*[@id="pagination"]/div/ul/li[11]/a')
        end.click()
        time.sleep(1)
        for z in range(4):
            actions.perform()   #navigate display to next page button 
            time.sleep(1)
        bound = self.driver.find_elements(By.XPATH,'//*[@id="pagination"]/div/ul/li/a')[-1].text
        back = self.driver.find_element(By.XPATH,'//*[@id="pagination"]/div/ul/li[1]')
        back.click()
        time.sleep(1)
        for it in range(int(bound) - 1):
            for i in range(1,6):
                try:
                    namePath = '//*[@id="hits"]/div/div[%s]/div/div/div/h1' %str(i) #in text
                    emailPath = '//*[@id="hits"]/div/div[%s]/div/div/div[2]/a' %str(i) #in href
                    locationPath = '//*[@id="hits"]/div/div[%s]/div/div/div[2]/h3[1]/span' %str(i) #in text
                    companyPath = '//*[@id="hits"]/div/div[%s]/div/div/div[2]/h3[2]/span'%str(i)#in text
                    focusPath = '//*[@id="hits"]/div/div[%s]/div/div/div/p[1]/span/span' %str(i)#general path will yield multiple results, in text
                    investmentsPath = '//*[@id="hits"]/div/div[%s]/div/div/div[2]/p[3]/span/span'%str(i) #name in text link in href
                    twitterPath = '//*[@id="hits"]/div/div[%s]/div/div/div[1]/a[1]' %str(i) # in href
                    linkedinPath = '//*[@id="hits"]/div/div[%s]/div/div/div[1]/a[2]' %str(i) #in href
                    
                    name = self.driver.find_element(By.XPATH,namePath).text
                    email = self.driver.find_element(By.XPATH,emailPath).get_attribute('href')[7:]
                    location = self.driver.find_element(By.XPATH,locationPath).text
                    company = self.driver.find_element(By.XPATH,companyPath).text
                    
                    focuses = ''
                    foci = self.driver.find_elements(By.XPATH,focusPath)
                    for res in foci:
                        focuses += res.text
                        focuses += ' '
                        
                    investments = ''
                    investi = self.driver.find_elements(By.XPATH,investmentsPath)
                    for re in investi:
                        investments += re.text
                        investments += ' '
                        
                    ### get links, XPAth changes when one is missing #####    
                    try:
                        link1 = self.driver.find_element(By.XPATH,twitterPath).get_attribute('href')
                    except:
                        link1 = ''
                    try:
                        link2 = self.driver.find_element(By.XPATH,linkedinPath).get_attribute('href')
                    except:
                        link2 = ''
                    links = [link1, link2]
                    twitter = ''
                    linkedin = ''  
                    for link in links:
                        if 'twitter' in link:
                            twitter += link
                        elif 'linkedin' in link:
                            linkedin += link
                    ########################################################## 
                    resu = [name, location, company, focuses, investments, email, twitter, linkedin]
                    queryResult.append(resu)
                except: #missing data fields so dont worry about it
                    pass
                
            actions = webdriver.ActionChains(self.driver) #prevents unclickable button error
            actions.send_keys(Keys.SPACE)
            for z in range(4):
                actions.perform()   #navigate display to next page button 
                time.sleep(1)
            time.sleep(1)
            nextPage = self.driver.find_element(By.XPATH,'//*[@aria-label="Next"]')
            nextPage.click()
            time.sleep(1)
        self.driver.close()
        return queryResult
    
    


def export2dArray(twoDArray):
    '''
    input: name of spreadsheet in google drive to export to
    outpt: none, edits existing spreadsheet in google drive
    '''
    scope = ['https://www.googleapis.com/auth/drive']
    name = r'/Users/michaelcantow/Documents/Michael-Jerrick-Code/Test-Export-Data-829118260f20.json'#path of json file with Google API credentials
    credentials = ServiceAccountCredentials.from_json_keyfile_name(name, scope)
    client = gspread.authorize(credentials)
    spreadsheet_name = 'InvestorHunt'
    sheet = client.open(spreadsheet_name).sheet1
    for row in twoDArray:
        sheet.append_row(row)
        time.sleep(1)                
                
        
#        
#foci = ['Mobile', 'Consumer Internet', 'Enterprise Software', 'SaaS', 'ECommerce', 'Social Media', 'Marketplaces', 'Digital Media']
        
foci = ['ECommerce']
#foci = ['Enterprise Software', 'SaaS', 'ECommerce', 'Social Media', 'Marketplaces', 'Digital Media']
locations = ['Palo Alto', 'San Francisco', 'New York City', 'Los Angeles', 'London', 'Silicon Valley', 'New York', 'Boston', 'California', 'United States']    
counter = 0           
for foc in foci:
    for loc in locations:
        counter += 1
        bot = InvestorHunt('blake.oconnor@jerrick.media', 'InvestorHuntPassword1')
        bot.login()
        try:
            bot.setScrapeParameters(foc, loc)
            print('Scraping investors specializing in ' + foc + ' located in ' + loc + '(' + str(counter) +' of 80)')
            twoDArray = bot.runScrape()
        except:
            print('Failed to set parameters for: ' + foc + ' and ' loc)
        for el in twoDArray:
            for e in el:
                try:
                    e = e.encode(encoding='UTF-8',errors='strict')
                except:
                    e = 'Non utf-8, encoding not supported'
#        try:
#            export2dArray(twoDArray)  #dealing with an api error which erratically occurs, can be solved by exporting to txt then importing the txt and exporting to sheets. 
#                                       # #idk why this error is occuring or why this solves it
#        except:
        with open('investorHunt.txt', 'a') as fi:
            for el in twoDArray:
                fi.write("%s\n" % el)



### read txt and export to sheets ####

with open('investorHunt.txt', 'r') as fdata:
    lines = fdata.read().splitlines()
    for line in lines:
        scope = ['https://www.googleapis.com/auth/drive']
        name = r'/Users/michaelcantow/Documents/Michael-Jerrick-Code/Test-Export-Data-829118260f20.json'#path of json file with Google API credentials
        credentials = ServiceAccountCredentials.from_json_keyfile_name(name, scope)
        client = gspread.authorize(credentials)
        spreadsheet_name = 'InvestorHunt'
        sheet = client.open(spreadsheet_name).sheet1
        row = ast.literal_eval(line)
        sheet.append_row(row)
        time.sleep(1)   


    



#twoDArray = []
#with open('investorHunt.txt', 'r') as fdata:
#    lines = fdata.read().splitlines()
#for line in lines:
#    twoDArray.append(ast.literal_eval(line))
#export2dArray(twoDArray)






#print(ast.literal_eval("['name', 'location', 'company', 'focuses', 'investments', 'email', 'twitter', 'linkedin']"))
        
        
#twoDArray = [['1','2','3'], ['4','5','6'], ['7','8','9']]
#with open('exportHere', 'w') as f:
#    for item in twoDArray:
#            f.write("%s\n" % item)
#foo = InvestorHunt('blake.oconnor@jerrick.media', 'InvestorHuntPassword1')
#foo.login()
#foo.setScrapeParameters('Marketplaces', 'Palo Alto')
#twoDArray = foo.runScrape()

#scope = ['https://www.googleapis.com/auth/drive']
#name = r'/Users/michaelcantow/Documents/Michael-Jerrick-Code/Test-Export-Data-829118260f20.json'#path of json file with Google API credentials
#credentials = ServiceAccountCredentials.from_json_keyfile_name(name, scope)
#client = gspread.authorize(credentials)
#
#def export2dArray(spreadsheet_name, twoDArray):
#    '''
#    input: name of spreadsheet in google drive to export to
#    outpt: none, edits existing spreadsheet in google drive
#    '''
#    print('exporting to sheets..')
#    sheet = client.open(spreadsheet_name).sheet1
#    for row in twoDArray:
#        sheet.append_row(row)
#        time.sleep(1)
#spreadsheet_name = 'InvestorHunt'
#export2dArray(spreadsheet_name, twoDArray)
#print('scrape complete')

        
        