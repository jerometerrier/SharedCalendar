from __future__ import print_function

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.


def is_date_format(date):
	try:
		datetime.datetime.strptime(date, '%d/%m/%Y')
		return True
	except ValueError:
		print("Incorrect data format, should be DD/MM/YYYY")
		return False


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
	def GetEvents(self, start_date, end_date):
		self.events = []
		if not is_date_format(start_date) or not is_date_format(end_date):
			return
		start_date = datetime.datetime.strptime(start_date, '%d/%m/%Y').isoformat() + 'Z'
		end_date = datetime.datetime.strptime(end_date, '%d/%m/%Y').isoformat() + 'Z'

		if end_date<start_date:
			print('to_date must be after from_date')
			return
		if self.IDCalendar == '':
			print('No calendar found')
			print('Please use GetIDCalendar()')
		else:
			self.events_result = self.service.events().list(calendarId=self.IDCalendar, timeMin=start_date,
											timeMax=end_date, singleEvents=True,
												orderBy='startTime').execute()
			self.events_items = self.events_result.get('items', [])
			if not self.events_items:
				print('No upcoming events found.')
			for event in self.events_items:
				start = event['start'].get('dateTime', event['start'].get('date'))
				if len(start) == 10 and start.count('-') == 2:
					start = datetime.date.fromisoformat(start)
				elif len(start) >= 19 and start[10] == 'T' and start.count('-') == 2 and start.count(':') >= 2:
					start = datetime.datetime.strptime(start, '%Y-%m-%dT%H:%M:%S%z')
				else:
					print("Format non reconnu :", start)
					#renvoi une erreur
					return

				start = start.strftime('%d/%m/%Y %H:%M')
				self.events.append({'start' : start,
						'summary': event['summary'],
						 'id': event['id']})
				# print(f'{self.CalName} : {start} ==> {event["summary"]}')
	def CreateEvent(self, name, start, end, description = ''):
		event = {
			'summary': name,
			'location': '',
			'description': description,
			'start': {
				'date': start,
				'timeZone': 'Europe/Paris',
			},
			'end': {
				'date': end,
				'timeZone': 'Europe/Paris',
			},
			'recurrence': [
				# 'RRULE:FREQ=DAILY;COUNT=2'
			],
			'attendees': [
				{'email': 'test@test.com'
	 				},
					 
			],
			# 'reminders': {
			# 	'useDefault': False,
			# 	'overrides': [
			# 		{'method': 'email', 'minutes': 24 * 60},
			# 		{'method': 'popup', 'minutes': 10},
			# 	],
			# },
		}
		event = self.service.events().insert(calendarId=self.IDCalendar, body=event).execute()
		print('Event created: %s' % (event.get('htmlLink')))
	def DeleteEvent(self, event_id):
		self.service.events().delete(calendarId=self.IDCalendar, eventId=event_id).execute()
		print('Event deleted')
	def DeleteAllEvents(self, start_date, end_date, name):
		self.GetEvents(start_date, end_date)
		for event in self.events:
			if event['summary'] == name:
				print(f"{event['summary']} : {event['start']}")
				self.DeleteEvent(event['id'])

	



class CalendrierGarde:
	def __init__(self):
		self.first_day = None
		self.Day1 = None
		self.Day2 = None
		self.Day3 = None
		self.Day4 = None
		self.Day5 = None
		self.Day6 = None
		self.Day7 = None
		self.Day8 = None
		self.Day9 = None
		self.Day10 = None
		self.Day11 = None
		self.Day12 = None
		self.Day13 = None
		self.Day14 = None

		pass
	def DeuxTroisDeux(self, first_day, calendar1, calendar2):
		if not is_date_format(first_day):
			return
		first_day = datetime.datetime.strptime(first_day, '%d/%m/%Y')
		self.Day1 = first_day
		self.Day2 = first_day + datetime.timedelta(days=1)
		self.Day3 = first_day + datetime.timedelta(days=2)
		self.Day4 = first_day + datetime.timedelta(days=3)		
		self.Day5 = first_day + datetime.timedelta(days=4)
		self.Day6 = first_day + datetime.timedelta(days=5)
		self.Day7 = first_day + datetime.timedelta(days=6)
		self.Day8 = first_day + datetime.timedelta(days=7)
		self.Day9 = first_day + datetime.timedelta(days=8)
		self.Day10 = first_day + datetime.timedelta(days=9)
		self.Day11 = first_day + datetime.timedelta(days=10)
		self.Day12 = first_day + datetime.timedelta(days=11)
		self.Day13 = first_day + datetime.timedelta(days=12)
		self.Day14 = first_day + datetime.timedelta(days=13)


		self.Day1Cal = calendar1
		self.Day2Cal = calendar1
		self.Day3Cal = calendar2
		self.Day4Cal = calendar2
		self.Day5Cal = calendar2
		self.Day6Cal = calendar1
		self.Day7Cal = calendar1
		self.Day8Cal = calendar2
		self.Day9Cal = calendar2
		self.Day10Cal = calendar1
		self.Day11Cal = calendar1
		self.Day12Cal = calendar1
		self.Day13Cal = calendar2
		self.Day14Cal = calendar2
	
	def showCalendrier(self):
		print(f"Jour 1 : {self.Day1}")
		print(f"Jour 2 : {self.Day2}")
		print(f"Jour 3 : {self.Day3}")
		print(f"Jour 4 : {self.Day4}")
		print(f"Jour 5 : {self.Day5}")
		print(f"Jour 6 : {self.Day6}")
		print(f"Jour 7 : {self.Day7}")
		print(f"Jour 8 : {self.Day8}")
		print(f"Jour 9 : {self.Day9}")
		print(f"Jour 10 : {self.Day10}")
		print(f"Jour 11 : {self.Day11}")
		print(f"Jour 12 : {self.Day12}")
		print(f"Jour 13 : {self.Day13}")
		print(f"Jour 14 : {self.Day14}")

	def createDefaultEvent(self):
		# Créez une liste pour stocker les variables Day1Cal à Day14Cal
		calendar_list = [
			(self.Day1Cal, self.Day1),(self.Day2Cal, self.Day2),
			(self.Day3Cal, self.Day3),(self.Day4Cal, self.Day4),
			(self.Day5Cal, self.Day5),(self.Day6Cal, self.Day6),
			(self.Day7Cal, self.Day7),(self.Day8Cal, self.Day8),
			(self.Day9Cal, self.Day9),(self.Day10Cal, self.Day10),
			(self.Day11Cal, self.Day11),(self.Day12Cal, self.Day12),
			(self.Day13Cal, self.Day13),(self.Day14Cal, self.Day14)]

		if any(cal[0] is None for cal in calendar_list):
			print("Please set calendar")

		for cal in calendar_list:
			start_date = cal[1].strftime('%Y-%m-%d')
			end_date = (cal[1] + datetime.timedelta(days=1)).strftime('%Y-%m-%d')

			cal[0].CreateEvent('Garde', start_date, end_date, 'Garde alternee')
	
	def checkIntregrity(self):
		pass
		
		

	
def main():
	CalJerome = CalendarGoogle()
	CalJerome.GetListCalendar()
	CalJerome.GetIDCalendar('Garde Alternee')
	CalJerome.GetEvents("01/09/2023", "18/09/2023")
	CalElise = CalendarGoogle()
	CalElise.GetListCalendar()
	CalElise.GetIDCalendar('Garde Elise')
	# CalElise.CreateEvent('Test2', '2023-09-18T10:00:00+02:00', '2023-09-18T11:00:00+02:00', 'Description test')
	CalElise.GetEvents("01/09/2023", "18/09/2023")
	# print(CalJerome.events)
	# CalElise.DeleteAllEvents("01/09/2023", "18/09/2023", "Garde")
	calendrier = CalendrierGarde()
	calendrier.DeuxTroisDeux("01/09/2023", CalJerome, CalElise)
	# calendrier.showCalendrier()
	calendrier.createDefaultEvent()




def init_calendar(start_date, end_date):
	if not is_date_format(start_date) or not is_date_format(end_date):
		return
	start_date = datetime.datetime.strptime(start_date, '%d/%m/%Y')#.isoformat() + 'Z'
	start_date_iso = start_date.isoformat() + 'Z'
	end_date = datetime.datetime.strptime(end_date, '%d/%m/%Y')#.isoformat() + 'Z'
	end_date_iso = end_date.isoformat() + 'Z'

	# Calcul de la plage de dates
	date_range = [start_date + datetime.timedelta(days=i) for i in range((end_date - start_date).days + 1)]

	# Afficher la plage de dates
	for date in date_range:
		print(date.date())
	
if __name__ == '__main__':
    main()
	# init_calendar("01/09/2023", "18/09/2023")