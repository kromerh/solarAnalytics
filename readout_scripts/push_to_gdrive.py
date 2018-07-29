# from pydrive.auth import GoogleAuth
# from pydrive.drive import GoogleDrive
# gauth = GoogleAuth()
# gauth.LocalWebserverAuth()
# drive = GoogleDrive(gauth)

# drive.auth.service.files().copy(fileId=file,
#                            body={"parents": [{"kind": "drive#fileLink",
#                                  "id": folder}], 'title': title}).execute()


from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

# Setup the Drive v3 API
SCOPES = 'https://www.googleapis.com/auth/drive.metadata.readonly'
store = file.Storage('client_credentials.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('drive', 'v3', http=creds.authorize(Http()))

# Call the Drive v3 API

folder = "/Solaranlage"
title = "Copy of my other file"
file = "test.txt"
results = service.files().copy(fileId=file, body={"parents": [{"kind": "drive#fileLink", "id": folder}], 'title': title}).execute()
