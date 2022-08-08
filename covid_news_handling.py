
import json
import logging
import requests
from covid_data_handler import *


with open("config.json") as config_file:
    config = json.load(config_file)
    api_key = config['api_key']
    logging_file = config['logging_file']
    key_terms = config['key_terms']


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(filename='logging.log')
stdout_handler = logging.StreamHandler(stream=sys.stdout)
handlers = [file_handler, stdout_handler]

logging.basicConfig(
    level=logging.DEBUG, 
    format='[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
    handlers=handlers
)


def news_API_request(covid_terms = 'Covid, COVID-19, coronavirus'):
    '''the function deal with the news api reqeust'''
    try:
        main_url = 'https://newsapi.org/v2/everything?q=' + key_terms +'&apiKey='+api_key
        news = requests.get(main_url).json()
        articles = news['articles']

    except ValueError:
        logger.exception('Invalid API URL')
        main_url = 'https://newsapi.org/v2/everything?q=' + covid_terms +'&apiKey='+api_key
        news = requests.get(main_url).json()
        articles = news['articles']
    else:
        logger.info('News API Called')

    return articles



def update_news():
    '''check for news updates'''
    news_API_request = []
    lines = open(news_API_request, "r").readlines()
    for line in lines:
        news_API_request.append(line.strip())
    return(news_API_request)


  
