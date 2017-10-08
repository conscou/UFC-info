import urllib2
import requests 
from bs4 import BeautifulSoup



#method to get the stats of a single fighter
def get_fighter_profile(fighter_name_input):

	fighter_name_input = fighter_name_input.replace(' ', '-')
	fighter = "http://www.ufc.com/fighter/" + fighter_name_input


	try:

		fighter_request = urllib2.Request(fighter)
		fighter_page = urllib2.urlopen(fighter_request)



	except urllib2.HTTPError, e:

		print "Either there is no record for this fighter, or the fighter does not exist"

	


#method to get the schedule of upcoming fights
def get_ufc_schedule():

	schedule_page = urllib2.urlopen("http://www.ufc.com/schedule/event")
	schedule_soup = BeautifulSoup(schedule_page, "html.parser")

	table_events = schedule_soup.find('div', class_="tab-content")

	events = table_events.find_all('div', class_="event-title")
	event_dates = table_events.find_all('div', class_="date")
	event_times = table_events.find_all('div', class_="time")
	event_locations = table_events.find_all('h3', class_="location")
	location_arena = table_events.find_all('span', class_="location-split")

	count = 0

	#there is a "hidden" list of times in the current markup for the UFC website
	#Actual fight times for listed fights start at index 20 -- must work on a
	#workaround for this

	time_count = 20


	print "*** NOTE: Schedule is subject to change ***"
	print "\n"

	for an_event in events:


		#prints event title
		print events[count].text.strip()


		#case to handle if there is no listed time
		if event_times[time_count].text.replace("ETPT", '').strip() == '':
			print event_dates[count].text.strip() + " @ " + "Time TBD"
		#case to handle when time is listed
		else:
			print event_dates[count].text.strip() + " @ " + event_times[time_count].text.replace("ETPT", '').strip() + " ET/PT"
		
		print location_arena[count].text
		print event_locations[count].text.replace(location_arena[count].text, '')

		print "\n"
		count = count+1
		time_count = time_count+1

		#check in case table is longer than actual events presented
		if count > len(events):
			break

