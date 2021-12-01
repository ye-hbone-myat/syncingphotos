# https://developers.google.com/drive/api/v3/quickstart/python
from __future__ import print_function
import pickle
import os.path
import pprint
import httplib2
from googleapiclient.discovery import build
import googleapiclient.http
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import sys
import os

# https://developers.google.com/analytics/devguides/config/mgmt/v3/quickstart/service-py
from oauth2client.service_account import ServiceAccountCredentials
credentials = ServiceAccountCredentials.from_json_keyfile_name("/Users/bigpapa/solid-century.json", scopes="https://www.googleapis.com/auth/drive")

# https://developers.google.com/drive/api/v3/quickstart/python
service = build('drive', 'v3', credentials=credentials)
count = 0
PARENTID = '1U_d9sr3igrbFByxSr61-xlUhJ2ddiHGk'
checkfilename = ""
checkfolder_id = ""

def checkfile(filename,parentid):
    page_token = None
    query = f"parents='{parentid}'"
    while True:
        response = service.files().list(q=query,
                                          spaces='drive', 
                                          supportsAllDrives=True, includeItemsFromAllDrives=True,
                                          fields='nextPageToken, files(id, name)',
                                          pageToken=page_token).execute()
        for file in response.get('files', []):
            # Process change
            checkfilename = file.get('name')
            if checkfilename == filename:
                return True
            
        page_token = response.get('nextPageToken', None)
        if page_token is None:
            return False
            break

def gdriveupload(FILENAME,folderid):
    # Metadata about the file.
    splitname = FILENAME.split('/')
    filename = splitname[-1]
    MIMETYPE = 'image/jpeg'
    if checkfile(filename,folderid) is False:
        media_body = googleapiclient.http.MediaFileUpload(
            FILENAME,
            mimetype=MIMETYPE,
            resumable=True
        )
        # The body contains the metadata for the file.
        body = {
            'parents': [folderid],
            'name': filename
        }
        # Perform the request and print the result.
        new_file = service.files().create(
            body=body, media_body=media_body, supportsAllDrives=True).execute()
        pprint.pprint(new_file)
    else:
        print(filename)
        print("Image exists and skipping.....")

def getListOfFiles(dirName):
    # create a list of file and sub directories 
    # names in the given directory 
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory 
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)
                
    return allFiles

def createfolder(FOLDER):
    global count
    global checkfilename
    global checkfolder_id
    splitname = FOLDER.split('/')
    filename = splitname[-2]
    MIMETYPE = 'application/vnd.google-apps.folder'
    global PARENTID
    if count == 0:        
        body = {
            'mimeType': MIMETYPE,
            'name': filename,
            'parents': [PARENTID]
        }
        #Perform the request and print the result.
        new_folder = service.files().create(
        body=body, supportsAllDrives=True).execute()
        folder_id = new_folder.get('id')
        checkfilename = filename
        checkfolder_id = folder_id
        count = count + 1
        #Upload all the files within the folder to Google Drive
        gdriveupload(FOLDER,folder_id)
    else:
        if checkfilename != filename:
            body = {
            'mimeType': MIMETYPE,
            'name': filename,
            'parents': [PARENTID]
            }
            #Perform the request and print the result.
            new_folder = service.files().create(
            body=body, supportsAllDrives=True).execute()
            folder_id = new_folder.get('id')
            checkfilename = filename
            checkfolder_id = folder_id
            gdriveupload(FOLDER,folder_id)
        else:
            gdriveupload(FOLDER,checkfolder_id)
        
def checkfolder(foldername):
    page_token = None
    global PARENTID 
    query = f"parents='{PARENTID}'"
    while True:
        response = service.files().list(q=query,
                                          spaces='drive', 
                                          supportsAllDrives=True, includeItemsFromAllDrives=True,
                                          fields='nextPageToken, files(id, name)',
                                          pageToken=page_token).execute()
        for file in response.get('files', []):
            # Process change
            checkfoldername = file.get('name')
            if foldername == checkfoldername:
                return True
            
        page_token = response.get('nextPageToken', None)
        if page_token is None:
            return False
            break

def getfolderid(folder):
    page_token = None
    global PARENTID
    query = f"parents='{PARENTID}'"
    while True:
        response = service.files().list(q=query,
                                          spaces='drive', 
                                          supportsAllDrives=True, includeItemsFromAllDrives=True,
                                          fields='nextPageToken, files(id, name)',
                                          pageToken=page_token).execute()
        for file in response.get('files', []):
            # Process change
            checkfoldername = file.get('name')
            if checkfoldername == folder:
                folderid = file.get('id')
                return folderid
            
        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break

def main(dirName):
    
    # Get the list of all files in directory tree at given path
    listOfFiles = getListOfFiles(dirName)
        
    # Get the list of all files in directory tree at given path
    listOfFiles = list()
    for (dirpath, dirnames, filenames) in os.walk(dirName):
        listOfFiles += [os.path.join(dirpath, file) for file in filenames]
            
    # Print the files    
    for elem in listOfFiles:
        check = elem.split('/')
        checkfile = check[-1]
        checkfoldername = check[-2]

        if checkfile != '.DS_Store':
            print(checkfoldername)
            if checkfolder(checkfoldername) is True:
                folderid = getfolderid(checkfoldername)
                print('Folder exists and update......')
                gdriveupload(elem,folderid)
                
            else:
                createfolder(elem)
                print('Folder doest exist and creating......')

if __name__ == '__main__':
    main(sys.argv[1])