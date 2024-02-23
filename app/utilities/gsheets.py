
import os
from typing import Union
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


class Gsheets():
    def __init__(self, sheetID: str):
        creds = None
        self.sheetID = sheetID
        scope = ["https://www.googleapis.com/auth/spreadsheets"]
        token_path = os.path.join(os.getcwd(), "app", "assets","gsheet-creds", "token.json")
        creds_path = os.path.join(os.getcwd(), "app", "assets", "gsheet-creds", "credentials.json")
        if os.path.exists(token_path):
            creds = Credentials.from_authorized_user_file(token_path, scopes=scope)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(creds_path, scopes=scope)
                creds = flow.run_local_server(port=0)
            with open(token_path, "w") as token:
                token.write(creds.to_json())
        

        try:
            service = build("sheets", "v4", credentials=creds)
            self.sheet = service.spreadsheets()
        except HttpError as err:
            print(err)

    def get(self, range: str):
        response = (self.sheet.values().get(spreadsheetId = self.sheetID, range=range).execute())
        values = response.get("values", [])
        return values[0]
    
    def append(self, data: list):
        if isinstance(data[0], str):
            temp = []
            temp.append(data)
            data = temp
        body = {"values": data}
        response = self.sheet.values().append(spreadsheetId = self.sheetID, range= "Sheet1!A1", body =body, valueInputOption = "RAW").execute()
        
        

        

    

    





