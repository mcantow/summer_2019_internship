#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  3 15:44:19 2019

@author: michaelcantow
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup #parse html code
import requests #get html code
import gspread#spreadsheet library
from oauth2client.service_account import ServiceAccountCredentials #spreadsheet library

articlepages = ['https://www.elephantjournal.com/#', 'https://www.elephantjournal.com/#trending', 'https://www.elephantjournal.com/#latest', 'https://www.elephantjournal.com/#editor', 'https://www.elephantjournal.com/#today', 'https://www.elephantjournal.com/#week', 'https://www.elephantjournal.com/#month', 'https://www.elephantjournal.com/#year', 'https://www.elephantjournal.com/#alltime']
#def getArticleLinks(articlepages):
#    '''
#    takes in links of pages to scrape
#    returns href to later be used to retrieve author info
#    '''
#    links = []
#    chrome_path = r'/Users/michaelcantow/Documents/Michael Jerrick Code/chromedriver'
#    chrome_options = webdriver.ChromeOptions()
#    chrome_options.add_argument("--incognito")
#    driver = webdriver.Chrome(chrome_path, options=chrome_options)  
#    for page in articlepages: 
#        driver.get(page)
#        articlesHTML = driver.find_elements(By.XPATH,'//*[@class="clickthrough"]')
#        for el in articlesHTML:
#            href = el.get_attribute('href')
#            links.append(href)
#    driver.close()
#    Links = []
#    for i in links:
#        if i not in Links:
#            Links.append(i)
#    return(links)

#Links = getArticleLinks(articlepages)
######################################################
### leave above code commented I saved it as test.txt file
######################################################
#with open('test.txt') as f:
#    lines = f.read().split(',')
#Links = lines
#
#for article in ['https://www.elephantjournal.com/2017/07/why-afternoon-naps-are-a-sign-of-health-not-laziness/', 'https://www.elephantjournal.com/2018/11/11-ways-we-can-all-benefit-from-trying-on-japanese-culture/', 'https://www.elephantjournal.com/2017/06/what-it-really-means-if-youve-been-ghosted-dumped-unfriended-or-blocked/']:
#    chrome_path = r'/Users/michaelcantow/Documents/Michael Jerrick Code/chromedriver'
#    chrome_options = webdriver.ChromeOptions()
#    chrome_options.add_argument("--incognito")
#    driver = webdriver.Chrome(chrome_path, options=chrome_options)  
#    driver.get(article)
#    try:
#        close = driver.find_element(By.XPATH,'//html/body/div[11]/div[2]/p[6]/a')
#        close.click()
#    except:
#        pass
#    try:
#        author = driver.find_element(By.XPATH,'//html/body/div/div/div/div/div/span/span/span/a')
#        authorLink = author.get_attribute('href')
#        driver.get(authorLink)
#        bio = driver.find_element(By.XPATH,'//html/body/div/div/div/div/div/div/div/p')
#        print(bio.text)
#        ##### xpath for bio links //*[@rel="noopener"]
##        print(bio.text)
##        print(bio.get_attribute('href'))
#    except:
#        pass
#    driver.close()

################################################################
######## got list of articles with selenium, now going to use beautiful soup,
######## use txt with article link to get author link

#with open('test.txt') as f:
#    lines = f.read().split(',')
#Links = lines

'''
['5.5', 'Betsy Heeney', " Editor's Pick", 'The Devastating, Traumatizing Road to Recovering from Childhood Sexual Trauma.', 'https://www.elephantjournal.com/2019/07/the-devastating-traumatizing-road-to-recovering-from-childhood-sexual-trauma-betsy-heeney/']
['0.6', 'Richard Josephson', 'The Buddhist view on Comfort Zones.', 'https://www.elephantjournal.com/2019/07/the-rut-of-the-comfort-zone/']
['10', 'Suzanne Falter', '8 Ground Rules for Better Emotional Self-Care.', 'https://www.elephantjournal.com/2018/09/8-ground-rules-for-better-emotional-self-care/']
['2.8', 'Nicole Cameron', '6 Minutes of Grief.', 'https://www.elephantjournal.com/2019/07/this-is-grief/']
['6.8', 'Kathryn Kurdt', 'A Psychological Condom for Online Dating: Don’t Feed the Narcissists.', 'https://www.elephantjournal.com/2019/07/a-psychological-condom-for-online-dating-dont-feed-the-narcissists-kathryn-kurdt/']
'''
                
                


#### returns [[eco-score, name, articleTitle, articleLink, isEditorPick]]
articlepages = ['https://www.elephantjournal.com/#', 'https://www.elephantjournal.com/#trending', 'https://www.elephantjournal.com/#latest', 'https://www.elephantjournal.com/#editor', 'https://www.elephantjournal.com/#today', 'https://www.elephantjournal.com/#week', 'https://www.elephantjournal.com/#month', 'https://www.elephantjournal.com/#year', 'https://www.elephantjournal.com/#alltime']
scraped = 0
firstScrape = []
for page in articlepages:
    result = requests.get(page)
    soup = BeautifulSoup(result.content, features = "lxml")
    authorItem = soup.find_all('article')
    for item in authorItem:
        text = item.text
        returnStrip = text.strip() #get rid of empty lines
        returnSplit = returnStrip.splitlines() #split lines
        returnClean = []
        for e in returnSplit:
            if e != '':
                returnClean.append(e)
        returnClean[0] = float(returnClean[0])
        f =item.find_all('a')
        for h in f:
            href = h.get('href')
            if href and 'https://www.elephantjournal.com' in href:
                returnClean.append(href)
        if len(returnClean) == 5: #editors pick
            returnClean.pop(2)
            returnClean.append('True')
            if returnClean not in firstScrape:
                firstScrape.append(returnClean)
        elif len(returnClean) == 4:
            returnClean.append('False')
            if returnClean not in firstScrape:
                firstScrape.append(returnClean)
        

#    links1 = soup.find_all('a', {"class" : "clickthrough"})
#    for link1 in links1:
#        href = link1.get('href')
#        scraped += 1
#        if href not in Links1:
#            Links1.append(href)
#        print('Scraped article ' + str(scraped/9)[:4] + ' percent of links')
            
print(len(firstScrape))
        
secondScrape = []
for q in firstScrape:
    try:
        url = q[3]
        result = requests.get(url)
        soup1 = BeautifulSoup(result.content, features = "lxml")
        a = soup1.find_all('a')
        for tag in a:
            href = tag.get('href')
            if 'https://www.elephantjournal.com/author/' in href: #link to the author page
                q.append(href)
                secondScrape.append(q)
                break 
    except:
        pass

## secondScrape = [[eco-score, name, articleTitle, articleLink, isEditorPick, authorPageHref]]

twoDArray = [['eco-score', 'name', 'articleTitle', 'articleLink', 'isEditorPick', 'authorPageHref', 'followers', 'bioTxt', 'instagramLink', 'facebookLink', 'twitterLink', 'otherLinks']]
counter = 0 
for p in secondScrape:
    try:
        author = p[-1]
        result = requests.get(author)
        soup2 = BeautifulSoup(result.content, features = "lxml")
        followers = soup2.find('span', {"class" : "follower-number"})
        followers = followers.text
        bio = soup2.find('div', {"class" : "author-bio-wrap"})
        bioo = bio.findChild()
        bioTxt = bioo.text
        links = []
        ass = bio.find_all('a')
        for a in ass:
            links.append(a.get('href'))
        instagramLink = ''
        facebookLink = ''
        twitterLink = ''
        otherLinks = ''
        for link in links:
            if 'intagram' in link:
                instagramLink += link
            elif 'facebook' in link:
                facebookLink += link
            elif 'twitter' in link:
                twitterLink += link
            else:
                otherLinks += link
                otherLinks += ' ' 
        counter += 1
        print('Scraped ' + str(counter/len(secondScrape) * 100)[:5] + 'percent of author pages')
        toAppend = p + [followers, bioTxt, instagramLink, facebookLink, twitterLink, otherLinks]
        twoDArray.append(toAppend)
        
    except:
        pass

print(twoDArray)

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
#
scope = ['https://www.googleapis.com/auth/drive']
name = 'Test-Export-Data-829118260f20.json'#string of name of json file with Google API credentials
credentials = ServiceAccountCredentials.from_json_keyfile_name(name, scope)
client = gspread.authorize(credentials)
spreadsheet_name = 'elephant2'
export2dArray(spreadsheet_name, twoDArray)


#print(authorPages)
#print('Length of authorPages:  ' + str(len(authorPages)))
        
#with open('exportHere.txt', 'w') as fi:
#    for el in authorPages:
#        fi.write("%s\n" % el)


#### scrap############################3
#result = requests.get('https://www.elephantjournal.com/2017/07/why-afternoon-naps-are-a-sign-of-health-not-laziness/')
#soup1 = BeautifulSoup(result.content, features = "lxml")
#a = soup1.find_all('a')
#for i in a:
#    b = i.get('href')
#    if 'https://www.elephantjournal.com/author/' in b:
#        print(b)
#        break
#######################################


