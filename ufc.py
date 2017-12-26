import re
import urllib
import requests 
from bs4 import BeautifulSoup

#method to get a fighter's webpage on UFC site
def get_fighter_page(fighter_name):
	
	fighter_name_input_web = fighter_name.replace(' ', '-')
	fighter_page = "http://www.ufc.com/fighter/" + fighter_name_input_web

	try:

		fighter_request = urllib.request.Request(fighter_page)
		fighter_soup = BeautifulSoup(urllib.request.urlopen(fighter_request), "html.parser")

		return fighter_soup

	except urllib.error.HTTPError as e:

		print ("Either there is no record for this fighter/the fighter does not exist, or the name you are providing is not spelled correctly")
		return



#method to get the stats of a single fighter
def get_fighter_profile(fighter_name_input):

	#string manipulation to get first and last name capitalized

	fighter_soup = get_fighter_page(fighter_name_input)
	fighter_name_input = fighter_name_input.title()

	print (fighter_name_input)
	print ("------")
	print ("\b")


	#stats and stuff
	skill_breakdown = fighter_soup.find('div', class_="skill-breakdown").find_all('td', class_="value")
	striking_and_grappling_percentage = fighter_soup.find_all('div', class_="bar-text")
	striking_defense = fighter_soup.find('div', id="striking-defense-percentage-area").find("div", class_="number-area")
	takedown_defense = fighter_soup.find('div', id="takedown-defense-percentage")
	fighter_info = fighter_soup.find('div', class_="fighter-info").find_all('td', class_="value")
	info_label = fighter_soup.find('div', class_="fighter-info").find_all('td', class_="label")


	print ("Record: " + skill_breakdown[0].text)
	print ("Summary: " + skill_breakdown[1].text)
	
	print ("\b")
	print ("Striking Percentage: " + striking_and_grappling_percentage[0].text.strip()[0:3])



	#this loop is to go through the striking and grappling statistics
	#to get takedown percentage, because current iteration of website
	#has more information that gets collected from the scraper and not
	#all fighters have all information filled out

	find_grappling_index = 2

	while find_grappling_index <= len(striking_and_grappling_percentage):
		if "Successful" in striking_and_grappling_percentage[find_grappling_index].text:
			print ("Takedown Percentage: " + " ".join(striking_and_grappling_percentage[find_grappling_index].text.split())[0:3])
			break
		else :
			find_grappling_index = find_grappling_index+1


	#resume consistent indexes for getting into
	print ("Striking Defense (The percentage of total strikes avoided): " + striking_defense.text.strip())
	print ("Takedown Defense (The percentage of total takedowns avoided): " + takedown_defense.text.strip())
	print ("\b")


	index = 0;
	for info in fighter_info:
		print (" ".join(info_label[index].text.split()) + " " + " ".join(info.text.split()))
		index = index + 1
	
	print ("\b")



#compare fighters
def compare_fighters(first_fighter, second_fighter):

	try:

		#gets webpage of the first fighter inputted
		first_fighter_soup = get_fighter_page(first_fighter)

		#gets webpage of the second fighter inputted
		second_fighter_soup = get_fighter_page(second_fighter)

		print (first_fighter + " vs " + second_fighter)
		print ("------")
		print ("\b")


		#skill breakdown for both fighters

		first_skill_breakdown = first_fighter_soup.find('div', class_="skill-breakdown").find_all('td', class_="value")
		second_skill_breakdown = second_fighter_soup.find('div', class_="skill-breakdown").find_all('td', class_="value")

		print (first_fighter + "'s Record: " + first_skill_breakdown[0].text)
		print (second_fighter + "'s Record: " + second_skill_breakdown[0].text)

		print ("\b")

		print (first_fighter + "'s Speciality: " + first_skill_breakdown[1].text)
		print (second_fighter + "'s Speciality: " + second_skill_breakdown[1].text)

		print ("\b")


		#striking and grappling for both fighters

		first_striking_and_grappling_percentage = first_fighter_soup.find_all('div', class_="bar-text")
		second_striking_and_grappling_percentage = second_fighter_soup.find_all('div', class_="bar-text")


		#DO THAT LOOP THING

		first_grappling_index = 2
		second_grappling_index = 2

		while first_grappling_index <= len(first_striking_and_grappling_percentage):
			if "Successful" in first_striking_and_grappling_percentage[first_grappling_index].text:
				print ("Takedown Percentage for " + first_fighter + ": " + " ".join(first_striking_and_grappling_percentage[first_grappling_index].text.split())[0:3])
				break
			else :
				first_grappling_index = first_grappling_index+1


		while second_grappling_index <= len(second_striking_and_grappling_percentage):
			if "Successful" in second_striking_and_grappling_percentage[second_grappling_index].text:
				print ("Takedown Percentage for " + second_fighter + ": " + " ".join(second_striking_and_grappling_percentage[second_grappling_index].text.split())[0:3])
				break
			else :
				second_grappling_index = second_grappling_index+1

		print ("\b")

		#striking defense for both fighters

		first_striking_defense = first_fighter_soup.find('div', id="striking-defense-percentage-area").find("div", class_="number-area")
		second_striking_defense = second_fighter_soup.find('div', id="striking-defense-percentage-area").find("div", class_="number-area")


		#takedown defense for both fighters

		first_takedown_defense = first_fighter_soup.find('div', id="takedown-defense-percentage")
		second_takedown_defense = second_fighter_soup.find('div', id="takedown-defense-percentage")


		print ("Striking Defense for " + first_fighter + ": " + first_striking_defense.text.strip())
		print ("Striking Defense for " + second_fighter + ": " + second_striking_defense.text.strip())

		print ("\b")

		print ("Takedown Defense for " + first_fighter + ": " + first_takedown_defense.text.strip())
		print ("Takedown Defense for " + second_fighter + ": " + second_takedown_defense.text.strip())

		
	except urllib.error.HTTPError as e:

		print ("Either there is no record for this fighter/the fighter does not exist, or the name you are providing is not spelled correctly")


#method to get the schedule of upcoming fights
def get_ufc_schedule():

	try:

		schedule_request = urllib.request.Request("http://www.ufc.com/schedule/event")
		schedule_soup = BeautifulSoup(urllib.request.urlopen(schedule_request), "html.parser")

		table_events = schedule_soup.find('div', class_="tab-content")

		events = table_events.find_all('div', class_="event-title")
		event_dates = table_events.find_all('div', class_="date")
		event_times = table_events.find_all('div', class_="time")
		event_locations = table_events.find_all('h3', class_="location")
		location_arena = table_events.find_all('span', class_="location-split")

		count = 0

		print ("UFC FIGHT SCHEDULE")
		print ("*** Schedule is subject to change ***")
		print ("\b")

		for an_event in events:

			#prints event title
			print (events[count].text.strip())
			
			#prints event date
			print (event_dates[count].text.strip())
			
			#prints location
			print (location_arena[count].text)
			print (event_locations[count].text.replace(location_arena[count].text, ''))

			print ("\b")
			count = count+1

			#check in case table is longer than actual events presented
			if count > len(events):
				break

	except urllib.error.HTTPError as e:

		print ("Error in accessing schedule")

	