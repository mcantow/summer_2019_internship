#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 12:17:14 2019

@author: michaelcantow
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
#from selenium.webdriver.common.keys import Keys
import time
#from bs4 import BeautifulSoup #parse html code
#import requests #get html code
import gspread#spreadsheet library
from oauth2client.service_account import ServiceAccountCredentials #spreadsheet library
#from lxml import etree



def firstScrape(topLinks):
    '''
    inputs:
        topLinks, list of grapheon pages to scrpae
    returns:
        [[authorLoacation, origin]]
        
    '''
    print("getting list of authors to scrape...")
    hrefs = []
    chrome_path = r'/Users/michaelcantow/Documents/Michael-Jerrick-Code/chromedriver'
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")
#    chrome_options.add_argument("--headless")
    prefs={"profile.managed_default_content_settings.images": 2, 'disk-cache-size': 4096 }
    prefs = {'profile.managed_default_content_settings.images':2}
    chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(chrome_path, options=chrome_options)  
#    for page in topLinks:
#        driver.get(page)
#        time.sleep(1)
###### this block of code is to scrape multiple pages of the same toplink, page 2 and 3 to be precise####
#        for z in range(30):
#            for i in range(1,101):
#                xpath = '//*[@id="allCreatorsTable"]/tbody/tr[%s]/td/a' % str(i)
#                block = driver.find_element(By.XPATH,xpath)
#                href = block.get_attribute('href')
#                hrefs.append([href[31:], page[40:]])
#            button = driver.find_element(By.XPATH,'//*[@id="allCreatorsTable_next"]')
#            button.click()
#            time.sleep(1)
    for page in topLinks:
        driver.get(page)
        time.sleep(1)
        for v in range(5):
            button = driver.find_element(By.XPATH,'//*[@id="allCreatorsTable_next"]')
            button.click()
            time.sleep(1)
        for i in range(1,101):
            xpath = '//*[@id="allCreatorsTable"]/tbody/tr[%s]/td/a' % str(i)
            block = driver.find_element(By.XPATH,xpath)
            href = block.get_attribute('href')
            hrefs.append([href[31:], page[40:]])
        
        
    driver.close()
    print("finished getting author list. Beggining full scrape")
    return (hrefs)


def convert(STR):
    '''
    converts special STR to int
    '''
    
    if '$' in STR:
        STR = STR[1:]
        
    if STR == '':
        return ''
        
    try:
        return(float(STR))
    except ValueError:
        pyFloat = ''
        
        if 'k' not in STR: #x,xxx
            for char in STR:
                if char == ',':
                    pass
                else:
                    pyFloat += char
                    
        else:
            if '.' not in STR:
                pyFloat += STR[:-1]
                pyFloat += '000'
            else:
                temp = ''
                temp += STR[:-1]
                temp += '00'
                for char in temp: 
                    if char != '.':
                        pyFloat += char
        pyFloat =float(pyFloat)
        return pyFloat

def secondScrape(locations):
    '''
    '''
    counter = 0      
    chrome_path = r'/Users/michaelcantow/Documents/Michael-Jerrick-Code/chromedriver'
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(chrome_path, options=chrome_options) 
    twoDArray = [['name', 'origin', 'profileURL', 'Patrons', 'Cash', 'Twitter', 'Facebook', 'Instagram', 'OtherLinks']]
    for loc in locations:
        origin = loc[1]
        url = 'https://www.patreon.com/' + loc[0]
        driver.get(url) 
        time.sleep(0.5)
        
        try: #am 18
            butt = driver.find_element(By.XPATH,'//*[@id="reactTarget"]/div/div[2]/div[3]/div/div[2]/div/div/div/div/div[3]/div/button')
            butt.click()
        except:
            pass
        
        time.sleep(0.5)
        try:
            name = driver.find_element(By.XPATH, '//*[@id="renderPageContentWrapper"]/div/div[3]/div/div/div/div[3]/div/h1')
            name = name.text
        except:
            name = ''
        
        Patrons = ''
        Cash = ''
        redBox = driver.find_elements(By.XPATH,'//*[@class="sc-bZQynM izRyKA"]')
        for el in redBox:
            txt = el.text
            if '$' in txt:
                Cash = convert(txt)
            else:
                Patrons = convert(txt)
        
        twitter = ''
        facebook = ''
        instagram = ''
        other = ''
        flag = False
        links = driver.find_elements(By.XPATH, '//*[@id="renderPageContentWrapper"]/div/div/div/div/div/div/div/div/span/a')
        for link in links:
            href = link.get_attribute('href')
            if 'twitter' in href:
                twitter += href
                flag = True
            elif 'facebook' in href:
                facebook += href
                flag = True
            elif 'instagram' in href:
                instagram += href
                flag = True
            else:
                other += href
                other += ' '
                flag = True
        if not flag:
            pass
        else:
            data = [name, origin, url, Patrons, Cash, twitter, facebook, instagram, other]
            twoDArray.append(data)
        counter += 1
        print('Scraped ' + str(counter * 100 / len(locations))[:4] + ' % of users')
        if counter % 10 == 0 and counter < len(locations):
            driver.close()
            chrome_path = r'/Users/michaelcantow/Documents/Michael-Jerrick-Code/chromedriver'
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument("--incognito")
            chrome_options.add_argument("--headless")
            driver = webdriver.Chrome(chrome_path, options=chrome_options)
            
#    print(twoDArray)
    print("finished webscrape. Exporting to google sheets")
    return twoDArray



topLinks = ['https://graphtreon.com/patreon-creators/games']#['https://graphtreon.com/patreon-creators/podcasts', 'https://graphtreon.com/patreon-creators/cosplay', 'https://graphtreon.com/patreon-creators/writing','https://graphtreon.com/patreon-creators/photography','https://graphtreon.com/patreon-creators/crafts-diy','https://graphtreon.com/patreon-creators/adult-podcasts']
locations = firstScrape(topLinks)[10:20]
#locations = [['SecretDinosaurCult', '40']]
twoDArray = secondScrape(locations)
#  
#    
scope = ['https://www.googleapis.com/auth/drive']
name = r'/Users/michaelcantow/Documents/Michael-Jerrick-Code/Test-Export-Data-829118260f20.json'#string of name of json file with Google API credentials
credentials = ServiceAccountCredentials.from_json_keyfile_name(name, scope)
client = gspread.authorize(credentials)
  
def export2dArray(spreadsheet_name, twoDArray):
    '''
    input: name of spreadsheet in google drive to export to
    outpt: none, edits existing spreadsheet in google drive
    '''
    sheet = client.open(spreadsheet_name).sheet1
    for row in twoDArray:
        sheet.append_row(row)
        time.sleep(1)
    
    
 
##### call export2dArray #########    
spreadsheet_name = 'Games'
export2dArray(spreadsheet_name, twoDArray)
     


    
    
    
#chrome_path = r'/Users/michaelcantow/Documents/Michael Jerrick Code/chromedriver'
#chrome_options = webdriver.ChromeOptions()
#chrome_options.add_argument("--incognito")
#driver = webdriver.Chrome(chrome_path, options=chrome_options) 
#driver.get('https://www.patreon.com/GuyNewYork') 
#links = driver.find_elements(By.XPATH, '//*[@id="renderPageContentWrapper"]/div/div[3]/div/div/div/div[3]/div/div[3]/span/a')
#for link in links:
#    href = link.get_attribute('href')
#    print(href)


           
#url = 'https://www.patreon.com/GuyNewYork'
#result = requests.get(url)
#soup = BeautifulSoup(result.content, features = "lxml")
#z = soup.find_all('a', {"target" : "_blank"})
#for t in z:
#    href = t.get('href')
#    if href:
#        print(href)
        
        
    