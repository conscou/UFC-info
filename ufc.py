import urllib2
import requests 
from bs4 import BeautifulSoup


#method to get the stats of a single fighter
def get_fighter_profile(fighter_name_input):

	fighter_name_input_web = fighter_name_input.replace(' ', '-')
	fighter = "http://www.ufc.com/fighter/" + fighter_name_input_web

	try:

		fighter_request = urllib2.Request(fighter)
		fighter_soup = BeautifulSoup(urllib2.urlopen(fighter_request), "html.parser")

		#string manipulation to get first and last name capitalized
		fighter_name_input = fighter_name_input.title()

		print fighter_name_input
		print "------"
		print "\b"


		#stats and stuff
		skill_breakdown = fighter_soup.find('div', class_="skill-breakdown").find_all('td', class_="value")
		striking_and_grappling_percentage = fighter_soup.find_all('div', class_="bar-text")
		striking_defense = fighter_soup.find('div', id="striking-defense-percentage-area").find("div", class_="number-area")
		takedown_defense = fighter_soup.find('div', id="takedown-defense-percentage")
		fighter_info = fighter_soup.find('div', class_="fighter-info").find_all('td', class_="value")
		info_label = fighter_soup.find('div', class_="fighter-info").find_all('td', class_="label")


		print "Record: " + skill_breakdown[0].text
		print "Summary: " + skill_breakdown[1].text
		
		print "\b"
		print "Striking Percentage: " + striking_and_grappling_percentage[0].text.strip()[0:3]



		#this loop is to go through the striking and grappling statistics
		#to get takedown percentage, because current iteration of website
		#has more information that gets collected from the scraper and not
		#all fighters have all information filled out

		find_grappling_index = 2

		while find_grappling_index <= len(striking_and_grappling_percentage):
			if "Successful" in striking_and_grappling_percentage[find_grappling_index].text:
				print "Takedown Percentage: " + " ".join(striking_and_grappling_percentage[find_grappling_index].text.split())[0:3]
				break
			else :
				find_grappling_index = find_grappling_index+1


		#resume consistent indexes for getting into
		print "Striking Defense (The percentage of total strikes avoided): " + striking_defense.text.strip()
		print "Takedown Defense (The percentage of total takedowns avoided): " + takedown_defense.text.strip()
		print "\b"


		index = 0;
		for info in fighter_info:
			print " ".join(info_label[index].text.split()) + " " + " ".join(info.text.split())
			index = index + 1
		
		print "\b"

	except urllib2.HTTPError, e:

		print "Either there is no record for this fighter/the fighter does not exist, or the name you are providing is not spelled correctly"

	

#method to get the schedule of upcoming fights
def get_ufc_schedule():

	try:

		schedule_request = urllib2.Request("http://www.ufc.com/schedule/event")
		schedule_soup = BeautifulSoup(urllib2.urlopen(schedule_request), "html.parser")

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

		print "UFC FIGHT SCHEDULE"
		print "*** Schedule is subject to change ***"
		print "\b"

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

			print "\b"
			count = count+1
			time_count = time_count+1

			#check in case table is longer than actual events presented
			if count > len(events):
				break

	except urllib2.HTTPError, e:

		print "Error in accessing schedule"


