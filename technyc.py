#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  8 15:08:10 2019

@author: michaelcantow
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import gspread#spreadsheet library
from oauth2client.service_account import ServiceAccountCredentials #spreadsheet library
import random

#chrome_path = r'/Users/michaelcantow/Documents/Michael-Jerrick-Code/chromedriver' # this is the path to chromedriver executible which selenium is built on
#chrome_options = webdriver.ChromeOptions()
#chrome_options.add_argument("--incognito")
#chrome_options.add_argument("--headless") #throws error in headless rn
#driver = webdriver.Chrome(chrome_path, options=chrome_options) 
#        
#
#driver.get('https://nytech.org/made?page=1')
#time.sleep(1)
#
#res = []
#for i in range(28):
#    linksHTML = driver.find_elements(By.XPATH,'//*[@target="_blank"]') #in the href
#    for item in linksHTML:
#        href = item.get_attribute('href')
#        if href not in res:
#            res.append(href)
#    actions = webdriver.ActionChains(driver) 
#    actions.send_keys(Keys.SPACE)
#    for i in range(3):
#        actions.perform()
#        time.sleep(0.5)
#    driver.find_element(By.XPATH,'//*[@class="next_page"]').click()
#
#driver.close()


#with open('investorHunt.txt', 'a') as fi:
#    for el in res:
#        fi.write("%s\n" % el)
##
scope = ['https://www.googleapis.com/auth/drive']
name = 'Test-Export-Data-829118260f20.json'#string of name of json file with Google API credentials
credentials = ServiceAccountCredentials.from_json_keyfile_name(name, scope)
client = gspread.authorize(credentials)
#
def export2dArray(spreadsheet_name, twoDArray):
    '''
    input: name of spreadsheet in google drive to export to
    outpt: none, edits existing spreadsheet in google drive
    '''
    sheet = client.open(spreadsheet_name).sheet1
    for row in twoDArray:
        sheet.append_row(row)
        time.sleep(1)

spreadsheet_name = 'madeinNYC'
#twoDArray = res
#export2dArray(spreadsheet_name, twoDArray)

twoDArray = []
with open('investorHunt.txt', 'r') as fdata:
    lines = fdata.read().splitlines()
for line in lines:
    twoDArray.append([line])
export2dArray(spreadsheet_name, twoDArray)
    




