import re
import urllib
import requests 
from bs4 import BeautifulSoup


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
