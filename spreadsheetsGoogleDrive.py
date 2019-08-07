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
  "project_id": "test-export-data",
  "private_key_id": "829118260f2070516ae0eb025291bf20b86fdad4",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQCjNJQE8d5bUgTA\nnelT9q5wxM1S3LVZuQnm40qBQ47EgNgJ1zxMbi5pvfp45Zn3A8dL+2/S/h34dBgP\nNOoJaC5kJwMfTKqseHwF08LVZ1XGveMp5ltSP0TQuCaXt1q3fjDGZvQFeEoL+oym\nuaAuYxh7ZiPrjCNPBa1WM8JCeDLXjmVcuSvjqRJz6IyBJa8+MUv4jqtTtxdoJG0h\nKvBW9ExXYvlQumlpicxcouOO82wUMjTOJaWNAYhP8nUFJLAWkVcGgvB3ZrrxSY76\nmtJa9Y8qWxShwzfnNr/nVTpYHX54NJgBvxwz3uLtAswaUp1+rdQAKE5K7roXjgEA\nemNWWH8lAgMBAAECggEABXCXHsYSulpUwGMoYo0mRH8kH9xYQBjCkNCnzFYHNXCy\nTWZVmG+TZPYOhJvp4pmcjuFfLrobyiBRJ/qZyBKnTzJyBceiqF6DYGyt7GUwxE/S\neUmivBj8mcoK4UOHhsuyOP63/fxZLXveVx/4oUCE0aIhKt9QKE4LuG6VDZhKNjSM\nteWpedBLALtWjj2ofkI2JrcC130uMlE4Q8Gwo6E9cm3RCQ5YbiJAU9EWo5keDwl5\nbDfU8pCGz9d0CK7Yijpdpiruc0acVKbhQW9WgUbQpXnkuKhEbpwshCm5IvUsAWKr\npF2aXtm+wrEAD6NsFgaEEOSKdUu6D9hJr0B7ULgoOQKBgQDlExk4X3khg3WwyxL5\nDrZDcU4+pJgZhW1yCbZX0ginf/+GGdF+/QyoShpeupfBNWcr5sV3LR6mAaz7v9fA\nmMpmeV1SWd+LrpLtcD7jBpQznWIpfFvlSs063Y8I7lKoTpU7TnKxI6EqV9wtZoye\nrpiu2mc99ugQxxRwaMpq869KGQKBgQC2Y3YgwYk3KiprGSom/ASwHUAa+wBc5pUL\nK2I6ZQnU8vnr12GvfM5rWPeBrDfsrQ9dC8EKuwHn7806XFpbfIm/5vnt+mbgH8FV\n9mGbNctWzywg7B3hbQsxdYZ7jmEVUsQl4Pcw0FZgllnQU8svJtBF9nG2NzG3rAVT\nHqfTwiDW7QKBgQCrVNqDIF1f5IwM/AYnw4os7T0Be2fLhtEx/vOjwZL5fLGoIf1f\nxnJGGI6alWLVflS5MDQ3C8clkJFKBdWf1mdjt5hF9LRPK/X2owJWGOCVrjvyHXI6\nD/Vp9rZ5jo7CFWxmXClKNgTfv7ENP+si8CGAfhfD77zod43g+W+UCMjtWQKBgQCz\n+Fjr4Y0gXf8VRvONHEkT7wj+loa5JN4U824t6N1Wv5tU2GaP3ztgOZ2g2uskI3Bx\ng9OsXvN2he2glNikRbM3JRehd+Bjb3I6/K87lE1dD3if0914Pz04RJu697dcbxsV\ntXK1PB6/mBxvsP9hO49wOcni33uznY5zgmBgV8JH0QKBgQDZ5sMXOLdIYJJklDQb\nsUad6CLDUGG5SRJNHujhGu0CBTOvyMPVo6FhOLKx1KWDJQH4CMNiCo/nj0+CwF2b\nNRrBxcrfWSuBVCmU9KBKt1LeBfYPfvIZtdt0auyjraPm5tgXIHCg54kMCG9Tj5wb\n44u3GDbHqQqclUoFoaOvEyqVHA==\n-----END PRIVATE KEY-----\n",
  "client_email": "exportspreadsheet@test-export-data.iam.gserviceaccount.com",
  "client_id": "113766360211122547152",
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