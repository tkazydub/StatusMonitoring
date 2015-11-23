from __future__ import print_function
import os, json, datetime, httplib2
from apiclient import discovery
import oauth2client
from oauth2client import client, tools


try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret_test.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'

class CalendarEvents():
    def get_credentials(self):
        """Gets valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        Returns:
            Credentials, the obtained credential.
        """
        credential_dir = os.path.join(os.getcwd(), '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,
                                       'calendar-python-quickstart.json')

        store = oauth2client.file.Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
            flow.user_agent = APPLICATION_NAME
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            else: # Needed only for compatability with Python 2.6
                credentials = tools.run(flow, store)
            print('Storing credentials to ' + credential_path)
        return credentials

    def get_events(self,number_of_events=10):
        credentials = self.get_credentials()
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('calendar', 'v3', http=http)
        now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
        print('Getting the upcoming 10 events')
        eventsResult = service.events().list(
            calendarId='primary', timeMin=now, maxResults=number_of_events, singleEvents=True,
            orderBy='startTime').execute()
        events = eventsResult.get('items', [])
        list_of_events = []
        if not events:
            print('No upcoming events found.')
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            end = event['end'].get('dateTime', event['end'].get('date'))
            summary = event['summary']
            try:
                location = event["location"]
            except KeyError:
                location = None
            # now = datetime.datetime.now().isoformat()
            # if start >= now:
            #     list_of_events.append({"start": start, "end":end, "summary":summary, "location":location})
            list_of_events.append({"start": start, "end":end, "summary":summary, "location":location})
        print(list_of_events)
        return list_of_events

    def get_configs(self):
        with open('calendar_config.json') as config:
            data = json.load(config)
        configs = {}
        if data:
            for key in data["default_settings"]:
                configs[key] = data["user_settings"][key] if data['user_settings'][key] else data['default_settings'][key]
        else:
            print("Unable to find Calendar configs")
        return configs

    def save_configs(self,conf):
        data = json.load(open('calendar_config.json'))
        for key in conf:
            data['user_settings'][key] = conf[key] if conf[key] else data['default_settings'][key]
        with open('calendar_config.json','w') as f:
            json.dump(data,f)
