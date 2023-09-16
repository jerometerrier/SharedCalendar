from __future__ import print_function

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.




class CalendarGoogle:
	def __init__(self):
		self.SCOPES = ['https://www.googleapis.com/auth/calendar']
		
		"""Shows basic usage of the Google Calendar API.
		Prints the start and name of the next 10 events on the user's calendar.
		"""
		self.creds = None
		# The file token.json stores the user's access and refresh tokens, and is
		# created automatically when the authorization flow completes for the first
		# time.
		if os.path.exists('token.json'):
			self.creds = Credentials.from_authorized_user_file('token.json', self.SCOPES)
		# If there are no (valid) credentials available, let the user log in.
		if not self.creds or not self.creds.valid:
			if self.creds and self.creds.expired and self.creds.refresh_token:
				self.creds.refresh(Request())
			else:
				self.flow = InstalledAppFlow.from_client_secrets_file(
					'credentials.json', self.SCOPES)
				self.creds = self.flow.run_local_server(port=0)
			# Save the credentials for the next run
			with open('token.json', 'w') as token:
				token.write(self.creds.to_json())
	def GetListCalendar(self, verbose = False):
		try:
			self.service = build('calendar', 'v3', credentials=self.creds)
			# page_token = None
			# while True:
			self.calendar_list = self.service.calendarList().list().execute()
				# if verbose:
				# 	for calendar_list_entry in self.calendar_list['items']:
				# 		print(calendar_list_entry['summary'])
				# 	page_token = self.calendar_list.get('nextPageToken')
				# 	if not page_token:
				# 		break
		except HttpError as error:
			print('An error occurred: %s' % error)
	def GetIDCalendar(self, name):
		self.GetListCalendar()
		self.CalName = name
		self.IDCalendar = [cal['id'] for cal in self.calendar_list['items'] if cal['summary'] == self.CalName][0]
		if self.IDCalendar == '':
			print('No calendar found')
	def GetEvents(self):
		if self.IDCalendar == '':
			print('No calendar found')
			print('Please use GetIDCalendar()')
		else:
			self.events_result = self.service.events().list(calendarId=self.IDCalendar, timeMin=datetime.datetime.utcnow().isoformat() + 'Z',
												maxResults=10, singleEvents=True,
												orderBy='startTime').execute()
			self.events = self.events_result.get('items', [])
			if not self.events:
				print('No upcoming events found.')
			for event in self.events:
				start = event['start'].get('dateTime', event['start'].get('date'))
				start = datetime.datetime.strptime(start, '%Y-%m-%dT%H:%M:%S%z')
				start = start.strftime('%d/%m/%Y %H:%M')
				print(f'{self.CalName} : {start} ==> {event["summary"]}')
	def CreateEvent(self, name, start, end, description = ''):
		event = {
			'summary': name,
			'location': '',
			'description': description,
			'start': {
				'dateTime': start,
				'timeZone': 'Europe/Paris',
			},
			'end': {
				'dateTime': end,
				'timeZone': 'Europe/Paris',
			},
			'recurrence': [
				# 'RRULE:FREQ=DAILY;COUNT=2'
			],
			'attendees': [
				{'email': 'test@test.com'
	 				},
					 
			],
			'reminders': {
				'useDefault': False,
				'overrides': [
					{'method': 'email', 'minutes': 24 * 60},
					{'method': 'popup', 'minutes': 10},
				],
			},
		}
		event = self.service.events().insert(calendarId=self.IDCalendar, body=event).execute()
		print('Event created: %s' % (event.get('htmlLink')))

	

def main():
	CalJerome = CalendarGoogle()
	CalJerome.GetListCalendar()
	CalJerome.GetIDCalendar('Garde Alternee')
	CalJerome.GetEvents()
	CalElise = CalendarGoogle()
	CalElise.GetListCalendar()
	CalElise.GetIDCalendar('Garde Elise')
	CalElise.CreateEvent('Test2', '2023-09-18T10:00:00+02:00', '2023-09-18T11:00:00+02:00', 'Description test')
	CalElise.GetEvents()



if __name__ == '__main__':
    main()