#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 15:39:31 2019

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

class vsco():
    '''
    class to scrape vsco
    '''
    def __init__(self, username, password):
        self.username = username
        self.password = password
        chrome_path = r'/Users/michaelcantow/Documents/Michael-Jerrick-Code/chromedriver'
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--incognito")
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(chrome_path, options=chrome_options) 
        self.driver.get('https://vsco.co/user/login')
        time.sleep(1)
        try:
            login = self.driver.find_element(By.XPATH,'//*[@id="login"]')
            password = self.driver.find_element(By.XPATH,'//*[@id="password"]')
            login.send_keys(self.username)
            password.send_keys(self.password)
            time.sleep(0.5)
            password.send_keys(Keys.ENTER)
        except: #already logged ind
            pass
        
    def scrapeUser(self, user):
        '''
        TFrom vsco gets [Name, Bio, link]
        '''
        self.driver.get(user)
        time.sleep(1)
        
        Name = ''
        try:
            nombre = self.driver.find_element(By.XPATH,'//*[@id="root"]/div/main/div/div/div/h2')
            llamo = nombre.text
            Name += llamo
        except:
            pass
        
        Link = ''
        try:
            oth = self.driver.find_element(By.XPATH,'//*[@target="_blank"]')
            hre = oth.get_attribute('href')
            Link += hre
        except:
            pass
        
        Bio = ''
        try:
            bi = self.driver.find_element(By.XPATH,'//*[@id="root"]/div/main/div/div/p')
            biotext = bi.text
            Bio += biotext
        except:
             pass
         
        toReturn = [Name, Bio, Link]
        return toReturn
    
    def getUsers(self, numUsers):
        '''
        scrapes vsco feed for int numUsers user URLs to scrape later
        '''
        print('scraping feed....')
        self.driver.get('https://vsco.co/feed')
        time.sleep(1)
        toScrape = []
        loadedMore = False #popup
        while len(toScrape) < numUsers:
            users = self.driver.find_elements(By.XPATH,'//*[@id="root"]/div/main/div/div/section/figure/figcaption/h6/a')
            for user in users:
                href = user.get_attribute('href')
                if href not in toScrape:
                    toScrape.append(href)
                    print(str(len(toScrape)/numUsers*100)[:4] + ' % complete') #update percentage
            actions = webdriver.ActionChains(self.driver)
            for v in range(15):
                actions.send_keys(Keys.ARROW_DOWN)
            actions.perform()
            if not loadedMore:
                try:
                    loadMore = self.driver.find_element(By.XPATH,'//*[@id="root"]/div/main/div/div/div/button')
                    loadMore.click()
                    loadedMore = True
                except: #not clickable yet and hasn't been clicked
                    pass 
            
        print('finished scraping feed, begin vist profiles...')
        return(toScrape)
        
    def getInstaData(self, target):
        '''
        returns list of user data in the form [instaPosts, instaFollowers, instaFollowing]
        '''
        
        self.driver.get(target)
        time.sleep(1)
        
        mainData = self.driver.find_elements_by_class_name("g47SY")
        numPosts = convertSAstringToFloat(mainData[0].text)
        numFollowers = convertSAstringToFloat(mainData[1].text)
        numFollowing = convertSAstringToFloat(mainData[2].text)
        return([numPosts, numFollowers, numFollowing])

        
    def runFullScrape(self, numUsers):
        '''
        Gets link to profile, Name, Link, and Bio if applicable
        '''
        counter = 0
        toReturn = [['name', 'vscoLink', 'bio', 'instaLink', 'instaPosts', 'instaFollowers', 'instaFollowing']]
        toScrape = self.getUsers(numUsers)
        for el in toScrape:
            data = self.scrapeUser(el)
            try:
                lin = str(data[2])
                if 'instagram' in lin:
                    instaData = self.getInstaData(lin)
                    temp = [data[0], el, data[1], data[2]] + instaData 
                    toReturn.append(temp)
                else:
                    pass #link to personal site
            except:
                pass #no link
            counter += 1
            print(str(counter/len(toScrape)*100)[:4] + ' % complete')
        return toReturn
            
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
        
vsco = vsco('blakeoconnor12345', 'vscopassword')
#print(vsco.scrapeUser('https://vsco.co/jasnoorkhalsa'))      
#print(vsco.getUsers(20))   
twoDArray = vsco.runFullScrape(2000) 
        
scope = ['https://www.googleapis.com/auth/drive']
name = r'/Users/michaelcantow/Documents/Michael-Jerrick-Code/Test-Export-Data-829118260f20.json'#path of json file with Google API credentials
credentials = ServiceAccountCredentials.from_json_keyfile_name(name, scope)
client = gspread.authorize(credentials)

def export2dArray(spreadsheet_name, twoDArray):
    '''
    input: name of spreadsheet in google drive to export to
    outpt: none, edits existing spreadsheet in google drive
    '''
    print('exporting to sheets..')
    sheet = client.open(spreadsheet_name).sheet1
    for row in twoDArray:
        sheet.append_row(row)
        time.sleep(1)
spreadsheet_name = 'vsco'
export2dArray(spreadsheet_name, twoDArray)
print('scrape complete')
            