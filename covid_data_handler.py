from uk_covid19 import Cov19API
import logging
import json
import sys

import sched, time
scheduler = sched.scheduler(time.time, time.sleep)


with open("config.json") as config_file:
    config_data = json.load(config_file)
   
    logging_file = config_data['logging_file']


""" this is to settup the loggings"""
file_handler = logging.FileHandler(filename=logging_file)
stdout_handler = logging.StreamHandler(stream=sys.stdout)
handlers = [file_handler, stdout_handler]

logging.basicConfig(
    level=logging.DEBUG, 
    format='[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
    handlers=handlers
)

national_covid_data = []
local_covid_data = []

def parse_csv_data(csv_filename):
    """"" this function takes parse_csv_data and return a list of strings"""
    list_of_strings = []
    lines = open(csv_filename, "r").readlines()
    for line in lines:
        list_of_strings.append(line.strip())
    return list_of_strings

def process_covid_csv_data(covid_csv_data):
    '''''this function process covid data, takes covid data and takes out all the
     key information needed, such as last_7days, current_hospital_cases, total_deaths
    '''
    last_7days = 0
    #new cases from last 7 days 
    for i in range(3, 10):
        last_7days += int(covid_csv_data[i].split(",")[6])
    #current_hospital_cases  7_019
    current_hospital_cases = 0
    for i in range(2):
        current_hospital_cases = (covid_csv_data[i].split(",")[5])
    #total_deaths 141_544
    total_deaths = 0
    for i in range(15):
        total_deaths = (covid_csv_data[i].split(",")[4])
    
    return last_7days, current_hospital_cases, total_deaths
    


def covid_API_resquest(location=config_data['default_location'], location_type=config_data['default_location_type']):
    '''the fucntion covid api request takes in the location and location type variable and looks up for covid data relating'''

    filters = ['areaType='+location_type,'areaName='+location]
    your_dict = {
        "date": "date",
        "areaName": "areaName",
        "areaCode": "areaCode",
        "newCasesByPublishDate": "newCasesByPublishDate",
        "cumCasesByPublishDate": "cumCasesByPublishDate",
        "newDeaths28DaysByDeathDate": "newDeaths28DaysByDeathDate",
        "cumDeaths28DaysByDeathDate": "cumDeaths28DaysByDeathDate"
    }

    api = Cov19API(filters=filters, structure=your_dict)
    data = api.get_json()["data"]


    if location_type == 'ltla':
        global local_covid_data
        local_covid_data = data
    elif location_type == "nation":
        global national_covid_data
        national_covid_data = data
    return(data)


def schedule_covid_updates(update_interval, update_name, location, location_type):
    '''this function will schedule upadtes and the intervals given for the news articles'''
    scheduler.enter(update_interval, 1, update_name, (location, location_type))
    schedule_covid_updates(3, covid_API_resquest, "Exeter", "ltla")
    schedule_covid_updates(5, covid_API_resquest, "England", "nation")
    scheduler.run()

