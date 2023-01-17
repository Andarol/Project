import datetime
import pickle
import os.path
from datetime import date, datetime
import googleapiclient
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials

from googleapiclient.errors import HttpError


# If modifying these scopes, delete the file token.pickle.
class My_calendar:
    def __init__(self,credential_file):
        self.SCOPES = ['https://www.googleapis.com/auth/calendar']

        self.CREDENTIALS_FILE = credential_file

    def get_calendar_service(self):

        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.CREDENTIALS_FILE, self.SCOPES)
                creds = flow.run_local_server(port=0)

            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        service = build('calendar', 'v3', credentials=creds)
        return service

    def get_list_of_calendars(self):
        service = self.get_calendar_service()
        # Call the Calendar API
        print('Getting list of calendars')
        calendars_result = service.calendarList().list().execute()

        calendars = calendars_result.get('items', [])

        if not calendars:
            print('No calendars found.')
        for calendar in calendars:
            summary = calendar['summary']
            id = calendar['id']
            primary = "Primary" if calendar.get('primary') else ""
            return ("%s\t%s\t%s" % (summary, id, primary))


    def get_list_of_events(self):
        service = self.get_calendar_service()
        list = ['']
        # Call the Calendar API
        now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        events_result = service.events().list(
            calendarId='primary', timeMin=now,
            maxResults=10, singleEvents=True,
            orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            pass
            # print('No upcoming events found.')
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            a = {event['summary']: event['id']}
            list.append(a)
        return list


    def create_event(self,year_time, month_time, day_time, hour_time, email, name):
        # creates one hour event tomorrow 10 AM IST
        service = self.get_calendar_service()

        d = datetime.now().date()
        tomorrow = datetime(year_time, month_time, day_time, hour_time) + timedelta(days=1)
        start = tomorrow.isoformat()
        end = (tomorrow + timedelta(hours=1)).isoformat()

        event_result = service.events().insert(calendarId='primary',
                                           body={
                                               "summary": str(name),
                                               "description": 'This is a tutorial example of automating google calendar with python',
                                               "start": {"dateTime": start, "timeZone": 'Europe/Kyiv'},
                                               "end": {"dateTime": end, "timeZone": 'Europe/Kyiv'},
                                               'attendees': [
                                                   {'email': str(email)},
                                               ],
                                           }
                                           ).execute()




    def delete_event(self,id_eventid):
        # Delete the event
        service = self.get_calendar_service()
        try:
            service.events().delete(
                calendarId='primary',
                eventId=str(id_eventid),
            ).execute()
        except googleapiclient.errors.HttpError:
            return False
        return True
