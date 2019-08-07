# -*- coding: utf-8 -*-
"""
Data scraper for seeking alpha.com. Set up as class which scrapes a user profile for desired data.
Must get list of user links to use the scraper on, code for that is towards end of document
tried to organize this code so it can be reused, but each scraper needs
to be fairly costumized

QUESTIONS: how many users do we want (roughly), do we want rss, discard users with no links?

documentation: https://www.crummy.com/software/BeautifulSoup/bs4/doc/#searching-the-tree

if persistent error try: soup = BeautifulSoup(html_doc, 'html.parser')

https://seekingalpha.com/opinion-leaders/technology/4
//*[@id="content_wrapper"]/div/div/div/ul/li/span/a/@href

"""
import requests #get html code
from bs4 import BeautifulSoup #parse html code
import time #avoid overflow on google api
import gspread#spreadsheet library
from oauth2client.service_account import ServiceAccountCredentials #spreadsheet library

class seekingAlpha():

    def __init__(self, user_url):
        result = requests.get(user_url)
        self.soup = BeautifulSoup(result.content, features = "lxml")
        self.user_url = user_url
#        self.soup = soup


    def getName(self):
        '''
        returns name as a string
        should only be called by scrapeAuthor method
        '''
        nameDash = self.user_url[32:]
        name = ''
        for i in nameDash:
            if i == '-':
                name += ' '
            else:
                name += i
        return (name)


    def getLinks(self):
        '''
        returns links from desired box as a tuple
        should only be called by scrapeAuthor method
        '''
        releventLinks = []
        
        ### made this try except since was getting some wierd errors
        
        
        try:
            twitter = self.soup.find('a', {'id': 'twitter'})
            twitterHref = twitter.get('href')
            if twitterHref != '#':
                releventLinks.append('Twitter: ' + str(twitterHref))
        except: 
            pass
             
        try:   
            linkedin = self.soup.find('a', {'id' : 'linked_in'})
            linkedHref = linkedin.get('href')
            if linkedHref != '#':
                releventLinks.append('linkedIn: ' + str(linkedHref))
        except:
            pass
         
        try:   
            personalWebsite = self.soup.find('a', {'id' : 'personal_url'})
            personalHref = personalWebsite.get('href')
            if personalHref != '#':
                releventLinks.append('personalWebsite: ' + str(personalHref))
        except:
            pass
        
        #####rss is in the box they wanted but is just a link to xml file
#        try:
#            rss = self.soup.find('a', {'id' : 'rss_link'})
#            rssHref = rss.get('href')
#            if rssHref != '#':
#                releventLinks.append('rss: ' + str(rssHref))
#        except:
#            pass
        
        toReturn = ''
        for link in releventLinks:
            toReturn += link + ' ' 
        return toReturn


    def getMiddleData(self):
        '''
        gets all i tages and finds numFollowers, numFollowing, numArticles. 
        returns these as floats
        
        functiongrouped together for 3 attributes since they have similar HTMLfootprints
        
        should only be called by scrapeAuthor method
        '''
        issue = False #flag for incomplete profiles
        
        iTags = self.soup.find_all('i')
        numFollowers= None
        numFollowing = None
        numArticles = None
        for tag in iTags:
            tagName = tag.get('data-profile-tab-count')
            if tagName is not None:
                if 'followers' in tagName:
                    numFollowers = tag.text
                elif 'following' in tagName:
                    numFollowing = tag.text
                elif 'articles' in tagName and 'premium' not in tagName:
                    numArticles = tag.text
        if numFollowers is not None:        
            numFollowers = convertSAstringToFloat(numFollowers)
        else: 
            issue = True
            
        if numFollowing is not None:
            numFollowing= convertSAstringToFloat(numFollowing)
        else: 
            issue = True
            
        if numArticles is not None:
            numArticles = convertSAstringToFloat(numArticles)
        else: 
            issue = True
        
        middleData = [numFollowers, numFollowing, numArticles]
        
        if issue: #incomplete profile, choosing not to scrape these
            return None
        return middleData
    
    
    def getBio(self):
        '''
        gets bio for given user, returns string
        should only be called by scrapeAuthor method
        '''
        try: #in case of empty bio
            pTags = self.soup.find_all('p')
            text = None
            for tag in pTags:
                tagName = tag.get('class')
                if tagName is not None and 'profile-bio-truncate' in tagName:
                    text = tag.text
            return text
        except:
            return None

        
    
    def getFirstArticle(self):
        '''
        gets first article name and tag for given user, returns list
        should only be called by scrapeAuthor method
        '''
        try: #in case no articles
            div = self.soup.find('div', {'class': 'author-article-title'})
            child = div.findChildren("a" , recursive=False)[0]
            name = child.text
            link = child.get('href')
            link = 'https://seekingalpha.com' + link
            return([name, link])
        except: 
            return None
        
        
    
    
    def scrapeAuthor(self):
        '''
        returns[[author_name, followers, following, num_articles, links(tuple)]]
        should be called for on each author iteration to get list of their data attributes
        '''
        name = self.getName()
        middleData = self.getMiddleData()
        bio = self.getBio()
        article = self.getFirstArticle()
        links = self.getLinks()
        if middleData is not None and bio is not None and article is not None: #make sure complete profile
            items = [name, self.user_url] + middleData + [bio] + article  + [links] 
            return items
        return None


def convertSAstringToFloat(SAstr):
    '''
    seeking alpha for users with following 1k-10k returns this as x,xxx (python doesnt use commas)
    and for users with following 10K plus uses xx.xk to display
    
    this functon convers the seeking alpha string notation to python float so 
    in sheets we can sort nuerically
    
    input: seeking alpha string type
    returns: float of desired number
    '''
    try:
        return(float(SAstr))
    except ValueError:
        pyFloat = ''
        
        if 'K' not in SAstr:
            for char in SAstr:
                if char == ',':
                    pass
                else:
                    pyFloat += char
                    
        else:
            if '.' not in SAstr:
                pyFloat += SAstr[:-1]
                pyFloat += '000'
            else:
                temp = ''
                temp += SAstr[:-1]
                temp += '00'
                for char in temp: 
                    if char != '.':
                        pyFloat += char
        pyFloat =float(pyFloat)
        return pyFloat



def getUserData(toScrape):
    '''
    caller function for seekingAlpha class
    input: 1D array with user urls (lonly location piece ex. 
           ['/author/christopher-vanwert', '/author/hans-centena', '/author/mott-capital-management']
           but this can be changed) 
           to scrape:
    returns: LOL :[[name, num_followers, num_following, num_articles, links]]
    '''
    twoDarray = [['name', 'user_url', 'num_followers', 'num_following', 'num_articles', 'bio', 'articleName', 'articleTitle', 'Twitter/linkedIn/personalSite']]
    counter = 0
    print('Beggining webscrape of seekingAlpha...')
    for el in toScrape:
        counter += 1
        authorLocation = el[0]
        user_url = 'https://seekingalpha.com' + authorLocation
        bot = seekingAlpha(user_url)
        data = bot.scrapeAuthor()
        if data is not None:
            twoDarray.append(data)
        print(str(counter/len(toScrape)*100)[:4] + '%')
    print('Finished Scraping Website: Seeking Alpha')
    return twoDarray

def getToScrape(start_urls):###NOTWORKING. the page has a robot detector
    ####solution: we into sheets did importxml, copied xpath and added @href
    '''
    input: list of start urls with a lot of links to scrape
    return: a list of author links
    '''
    authorsToScrape = []
    for url in start_urls:
        result = requests.get(url)
        soup = BeautifulSoup(result.content, features = "lxml")
        links = soup.find_all('a')
        print(links)
#        for link in links:
#            href = link.get('href')
#            if 'author' in href or 'user' in href:
#                if href not in authorsToScrape:
#                    authorsToScrape.append(href)
#    return(authorsToScrape)
        



scope = ['https://www.googleapis.com/auth/drive']
name = 'Test-Export-Data-829118260f20.json'#string of name of json file with Google API credentials
credentials = ServiceAccountCredentials.from_json_keyfile_name(name, scope)
client = gspread.authorize(credentials)


def export2dArray(spreadsheet_name, twoDArray):
    '''
    input: name of spreadsheet in google drive to export to
    outpt: none, edits existing spreadsheet in google drive
    '''
    sheet = client.open(spreadsheet_name).sheet1
    print('Exporting data to spreadsheet...')
    counter = 0
    for row in twoDArray:
        counter += 1
        print(str(counter/len(twoDArray)*100)[:4] + '%')
        sheet.append_row(row)
        time.sleep(1) #avoid google api issue, limit 10 requests per 10 seconds so sleep 1 second
    print('Task Completed: finished webscrape and exported findings to Google Sheets')
    
def importSpreadsheet(spreadsheet_name):
    '''
    input: name of spreadsheet in google drive to be imported
    output: 2D array of data in spreadsheet
    '''
    sheet = client.open(spreadsheet_name).sheet1
    data = sheet.get_all_values()
    return data 

#################   get desired 2D array in seeking seekingScrape sheet #####################
 
##### get twoDArray
#toScrape = ['/author/christopher-vanwert', '/author/hans-centena', '/author/mott-capital-management', '/author/stone-fox-capital', '/author/patrick-mayles', '/author/john-engle', '/author/renegade-investment-research', '/author/anton-wahlman', '/author/2ndmarketcapital', '/author/bill-maurer', '/author/dhierin-bechai', '/author/hans-centena', '/author/steven-chen', '/author/matt-bohlsen', '/author/cornerstone-investments', '/author/john-vincent', '/author/fund-letters', '/author/fund-letter-stock-ideas', '/author/harris-oakmark', '/author/clearbridge-investments', '/author/insiderinsights', '/author/the-insiders-forum', '/author/giovanni-dimauro', '/author/asif-suria', '/author/filing-scanner', '/author/donovan-jones', '/author/euan-jones', '/author/david-evans', '/author/bilbao-asset-management', '/author/renaissance-capital-ipo-research', '/author/alpha-exposure', '/author/hindenburg-investment-research', '/author/rota-fortunae', '/author/vincent-ventures', '/author/the-friendly-bear', '/author/dividend-sensei', '/author/stefan-redlich', '/author/dale-roberts', '/author/the-part-time-investor', '/author/financially-free-investor', '/author/arturo-neto-cfa', '/author/rida-morwa', '/author/arbitrage-trader', '/author/the-belgian-dentist', '/author/the-fortune-teller', '/author/dividend-sensei', '/author/rida-morwa', '/author/pendragony', '/author/double-dividend-stocks', '/author/achilles-research', '/author/dividend-sensei', '/author/fredrik-arnold', '/author/the-dividend-guy', '/author/ferdis', '/author/ploutos', '/author/financially-free-investor', '/author/treading-softly', '/author/dividend-sensei', '/author/rida-morwa', '/author/colorado-wealth-management-fund', '/author/tipswatch', '/author/arbitrage-trader', '/author/jeremy-lakosh', '/author/kwan-chen-ma', '/author/luca-zambelli', '/author/brad-thomas', '/author/arturo-neto-cfa', '/author/jussi-askola', '/author/achilles-research', '/author/colorado-wealth-management-fund', '/author/christopher-vanwert', '/author/avi-gilburt', '/author/the-heisenberg', '/author/lance-roberts', '/author/bill-ehrman', '/author/andrew-hecht', '/author/avi-gilburt', '/author/clif-droke', '/author/adam-hamilton', '/author/robert-kientz', '/author/hfir', '/author/andrew-hecht', '/author/kirk-spano', '/author/andrei-evbuoma', '/author/hfir-energy', '/author/jeff-miller', '/author/eric-basmajian', '/author/independent-trader', '/author/john-m-mason', '/author/cashflow-capitalist', '/author/marc-chandler', '/author/dean-popplewell', '/author/andrew-hecht', '/author/discount-fountain', '/author/hedge-insider', '/author/brad-thomas', '/author/jussi-askola', '/author/hoya-capital-real-estate', '/author/david-haggith', '/author/wolf-richter', '/author/r-paul-drake', '/author/logan-kane', '/author/christopher-hamilton', '/author/danielle-park-cfa', '/author/ld-investments', '/author/victor-dergunov', '/author/the-freedonia-cooperative', '/author/daniel-amerman-cfa', '/author/avi-gilburt', '/author/thomas-hughes', '/author/hans-centena', '/author/fun-trading', '/author/power-hedge', '/author/long-player', '/author/vladimir-zernov', '/author/shock-exchange', '/author/daniel-jones', '/author/wg-investment-research', '/author/john-m-mason', '/author/achilles-research', '/author/christopher-vanwert', '/author/bill-maurer', '/author/john-engle', '/author/gary-bourgeault', '/author/anton-wahlman', '/author/brad-thomas', '/author/arturo-neto-cfa', '/author/achilles-research', '/author/christopher-vanwert', '/author/rida-morwa', '/author/terry-chrisomalis', '/author/dividend-sensei', '/author/biologics', '/author/donovan-jones', '/author/biosci-capital-partners', '/author/stephen-simpson-cfa', '/author/henrik-alex', '/author/edward-ambrose', '/author/jp-research', '/author/chuck-carnevale', '/author/patrick-mayles', '/author/christopher-vanwert', '/author/hans-centena', '/author/steven-chen', '/author/arturo-neto-cfa', '/author/stone-fox-capital', '/author/arturo-neto-cfa', '/author/mott-capital-management', '/author/bill-maurer', '/author/kwan-chen-ma', '/author/brad-thomas', '/author/robert-sam-kovacs', '/author/long-player', '/author/wealth-insights', '/author/power-player', '/author/hans-centena', '/author/steven-chen', '/author/david-pinsen', '/author/arturo-neto-cfa', '/author/ploutos', '/author/stanford-chemist', '/author/power-hedge', '/author/alpha-gen-capital', '/author/arbitrage-trader', '/author/arturo-neto-cfa', '/author/arturo-neto-cfa', '/author/andres-cardenal-cfa', '/author/stanford-chemist', '/author/victor-dergunov', '/author/dividend-seeker', '/author/david-trainer', '/author/cm-market-insights', '/author/dave-dierking-cfa', '/author/zacks-funds', '/author/josh-ortner']
#toScrape = ['/author/john-engle']
toScrape = importSpreadsheet('seekingScrape')#2D array

twoDArray = getUserData(toScrape)

##### export twoDArray #########    
spreadsheet_name = 'ssImportHere'
export2dArray(spreadsheet_name, twoDArray)


#############################3##   test methods     #########################
###############################################################################
#user_url = 'https://seekingalpha.com/author/steven-chen' 
#user_url = 'https://seekingalpha.com//author/2ndmarketcapital'
#bot = seekingAlpha(user_url) 

#test = bot.getFirstArticle()
#print(test)

#test = bot.getBio()
#print(test)
#
###test getName ##working
#name = bot.getName()
#print(name)
#
####test getLinks #working
#links = bot.getLinks()
#print(links)
##
####test getMiddleData
#data = bot.getMiddleData()
#print(data)
#
####test scrapeAuthor#####
#data = bot.scrapeAuthor()
#print(data)

####test convertSAstringToFloat(SAstr)
#SAstr = '19.8K'
#response = convertSAstringToFloat(SAstr)
#print(response)
#if response == 1234:
#    print('converted to float successfully')



########### gets list of authors #################################################
##################################################################################

#starturl = 'https://seekingalpha.com/opinion-leaders/long-ideas' 
##bot = seekingAlpha(starturl) 
#
#result = requests.get(starturl)
#soup = BeautifulSoup(result.content, features = "lxml")
#links = soup.find_all('div') #very easy to get all links from a page, filtering is the challeng
#print(links)
#authorsToScrape = []
#for link in links:
#    href = link.get('href')
#    if 'author' in href:
#        authorsToScrape.append(href)
#print(authorsToScrape)






######################## SCRAP CODE ###############################################
#debug######
#result = requests.get(user_url)
#soup = BeautifulSoup(result.content, features = "lxml")
#iTags = soup.find_all('i')
#toPrint = []
#numFollowers = None
#for tag in iTags:
#    tagName = tag.get('data-profile-tab-count')
#    toPrint.append(tagName)
#    if 'followers' in tag:
#        numFollowers = tag.text
#print(toPrint)
#print(iTags)
####################





#url = 'https://seekingalpha.com/leader-board/opinion-leaders'
#result = requests.get(url)
#soup = BeautifulSoup(result.content, features = "lxml")
#links = soup.find_all('a') #very easy to get all links from a page, filtering is the challenge
#authorsToScrape = []
#for link in links:
# href = link.get('href')
# if 'author' in href:
# authorsToScrape.append(href)
#print(authorsToScrape)

######### scrape desired links from authors ##################
#data = []
#toScrape = ['/author/christopher-vanwert', '/author/hans-centena', '/author/mott-capital-management', '/author/stone-fox-capital', '/author/patrick-mayles', '/author/john-engle', '/author/renegade-investment-research', '/author/anton-wahlman', '/author/2ndmarketcapital', '/author/bill-maurer', '/author/dhierin-bechai', '/author/hans-centena', '/author/steven-chen', '/author/matt-bohlsen', '/author/cornerstone-investments', '/author/john-vincent', '/author/fund-letters', '/author/fund-letter-stock-ideas', '/author/harris-oakmark', '/author/clearbridge-investments', '/author/insiderinsights', '/author/the-insiders-forum', '/author/giovanni-dimauro', '/author/asif-suria', '/author/filing-scanner', '/author/donovan-jones', '/author/euan-jones', '/author/david-evans', '/author/bilbao-asset-management', '/author/renaissance-capital-ipo-research', '/author/alpha-exposure', '/author/hindenburg-investment-research', '/author/rota-fortunae', '/author/vincent-ventures', '/author/the-friendly-bear', '/author/dividend-sensei', '/author/stefan-redlich', '/author/dale-roberts', '/author/the-part-time-investor', '/author/financially-free-investor', '/author/arturo-neto-cfa', '/author/rida-morwa', '/author/arbitrage-trader', '/author/the-belgian-dentist', '/author/the-fortune-teller', '/author/dividend-sensei', '/author/rida-morwa', '/author/pendragony', '/author/double-dividend-stocks', '/author/achilles-research', '/author/dividend-sensei', '/author/fredrik-arnold', '/author/the-dividend-guy', '/author/ferdis', '/author/ploutos', '/author/financially-free-investor', '/author/treading-softly', '/author/dividend-sensei', '/author/rida-morwa', '/author/colorado-wealth-management-fund', '/author/tipswatch', '/author/arbitrage-trader', '/author/jeremy-lakosh', '/author/kwan-chen-ma', '/author/luca-zambelli', '/author/brad-thomas', '/author/arturo-neto-cfa', '/author/jussi-askola', '/author/achilles-research', '/author/colorado-wealth-management-fund', '/author/christopher-vanwert', '/author/avi-gilburt', '/author/the-heisenberg', '/author/lance-roberts', '/author/bill-ehrman', '/author/andrew-hecht', '/author/avi-gilburt', '/author/clif-droke', '/author/adam-hamilton', '/author/robert-kientz', '/author/hfir', '/author/andrew-hecht', '/author/kirk-spano', '/author/andrei-evbuoma', '/author/hfir-energy', '/author/jeff-miller', '/author/eric-basmajian', '/author/independent-trader', '/author/john-m-mason', '/author/cashflow-capitalist', '/author/marc-chandler', '/author/dean-popplewell', '/author/andrew-hecht', '/author/discount-fountain', '/author/hedge-insider', '/author/brad-thomas', '/author/jussi-askola', '/author/hoya-capital-real-estate', '/author/david-haggith', '/author/wolf-richter', '/author/r-paul-drake', '/author/logan-kane', '/author/christopher-hamilton', '/author/danielle-park-cfa', '/author/ld-investments', '/author/victor-dergunov', '/author/the-freedonia-cooperative', '/author/daniel-amerman-cfa', '/author/avi-gilburt', '/author/thomas-hughes', '/author/hans-centena', '/author/fun-trading', '/author/power-hedge', '/author/long-player', '/author/vladimir-zernov', '/author/shock-exchange', '/author/daniel-jones', '/author/wg-investment-research', '/author/john-m-mason', '/author/achilles-research', '/author/christopher-vanwert', '/author/bill-maurer', '/author/john-engle', '/author/gary-bourgeault', '/author/anton-wahlman', '/author/brad-thomas', '/author/arturo-neto-cfa', '/author/achilles-research', '/author/christopher-vanwert', '/author/rida-morwa', '/author/terry-chrisomalis', '/author/dividend-sensei', '/author/biologics', '/author/donovan-jones', '/author/biosci-capital-partners', '/author/stephen-simpson-cfa', '/author/henrik-alex', '/author/edward-ambrose', '/author/jp-research', '/author/chuck-carnevale', '/author/patrick-mayles', '/author/christopher-vanwert', '/author/hans-centena', '/author/steven-chen', '/author/arturo-neto-cfa', '/author/stone-fox-capital', '/author/arturo-neto-cfa', '/author/mott-capital-management', '/author/bill-maurer', '/author/kwan-chen-ma', '/author/brad-thomas', '/author/robert-sam-kovacs', '/author/long-player', '/author/wealth-insights', '/author/power-player', '/author/hans-centena', '/author/steven-chen', '/author/david-pinsen', '/author/arturo-neto-cfa', '/author/ploutos', '/author/stanford-chemist', '/author/power-hedge', '/author/alpha-gen-capital', '/author/arbitrage-trader', '/author/arturo-neto-cfa', '/author/arturo-neto-cfa', '/author/andres-cardenal-cfa', '/author/stanford-chemist', '/author/victor-dergunov', '/author/dividend-seeker', '/author/david-trainer', '/author/cm-market-insights', '/author/dave-dierking-cfa', '/author/zacks-funds', '/author/josh-ortner']
#for author in toScrape:
# url = 'https://seekingalpha.com' + author
# result = requests.get(url)
# soup = BeautifulSoup(result.content, features = "lxml")
# name = soup.find('div', {'class' : 'username'})
# if name is not None:
# success += 1
# #### desired links can be filtered by <i> tag. Will try to iterate through these until we hit mute
# #### mute is the last link for every page



#url = 'https://seekingalpha.com/author/steven-chen'
#result = requests.get(url)
#soup = BeautifulSoup(result.content, features = "lxml")
#
#
#nameDash = url[32:]
#name = ''
#for i in nameDash:
# if i == '-':
# name += ' '
# else:
# name += i
#print(name)

#name = soup.find('div', {'class' : 'username'})
#name = soup.find('username')
#nameText = name.text




##### get links scrap code#####
#  for link in links:
#            if link != None:
#                href = link.get('href')
#                releventLinks.append(href)

#     links = self.soup.find_all('a')
#        
#        # for link in links:
#        # href = link.get('href')
#        # releventLinks.append(href)
#        
#        keywords = ['https://linkedin', 'https://twitter']
#        for link in links:
#            href = link.get('href')
#            for word in keywords:
#                if word in href:
#                    releventLinks.append(href)

####### RIP dead methods: #########
#    def getNumFollowers(self):
#        '''
#        returns number of followers as a string
#        should only be called by scrapeAuthor method
#        '''
#        followersHTML = self.soup.find_all('i')
##        followersStr = followersHTML.text
##        return followersStr
#        return followersHTML
#    
#    def getNumFollowing(self):
#        '''
#        return number of users current user is following
#        should only be called by the scrapeAuthor method
#        '''
#        followingHTML = self.soup.find('i', {'data-profile-tab-count': 'following'})
#        followingStr = followingHTML.text
#        return followingStr
#        
#    def getNumArticles(self):
#        '''
#        returns number of articles as a string
#        should only be called by scrapeAuthor method
#        '''
#        numArticlesHTML = self.soup.find('i', {'data-profile-tab-count' : "articles_count"})
#        numArticlesStr = numArticlesHTML.text
#        return numArticlesStr