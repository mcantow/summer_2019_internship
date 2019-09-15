le #!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
These functions import GOOGLE SHEETS spreadsheets into python as a 2D array
and will export a 2D array into GOGGLE SHEETS as a spreadsheet
############
To set up API,
Go to google api manager, create project, enable apis and services, then search for
and enable google drive. Then create credentials, (google drive api, webserver, app data, no)
name = exportSpreadsheet, make it project editor. Now click and it will create a 
JSON file as show below. copy client email and share spreadsheet with it.
#############
Google API credentials for exportSpreadsheet project. Save this file as json IN FOLDER with 
script it will be called by
{
  "type": "service_account",
  "project_id": "x",
  "private_key_id": "x" #input yours for x
  "private_key": "-----BEGIN PRIVATE KEY-----\x\n-----END PRIVATE KEY-----\n",
  "client_email": "exportspreadsheet@test-export-data.iam.gserviceaccount.com",
  "client_id": "x",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/exportspreadsheet%40test-export-data.iam.gserviceaccount.com"
}

SHARE SHEET WITH CLIENT_EMAIL and the below code should work
"""
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time

####create api object ########
scope = ['https://www.googleapis.com/auth/drive']
name = 'Test-Export-Data-829118260f20.json'#string of name of json file with Google API credentials
credentials = ServiceAccountCredentials.from_json_keyfile_name(name, scope)
client = gspread.authorize(credentials)




def importSpreadsheet(spreadsheet_name):
    '''
    input: name of spreadsheet in google drive to be imported
    output: 2D array of data in spreadsheet
    '''
    sheet = client.open(spreadsheet_name).sheet1
    data = sheet.get_all_values()
    return data


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
spreadsheet_name = 'Test Spreadsheet'
twoDArray = [['Name', 'Email', 'password'], ['John', 'john@gmail.com', 'password1!'], ['hPPY', 'hp@gmail.com', 'password2!']]
export2dArray(spreadsheet_name, twoDArray)
#        
        
########################################################################################        
########################################################################################


###### call importSpreadsheet #########
#spreadsheet_name = 'Test Spreadsheet'
#spreadsheet = importSpreadsheet(spreadsheet_name)
#print(spreadsheet)  
