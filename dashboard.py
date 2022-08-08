
import sched
import time
from flask import Flask, render_template, request, redirect
import logging
from covid_data_handler import covid_API_resquest
from covid_news_handling import news_API_request
schedule = sched.scheduler(time.time, time.sleep)

app = Flask(__name__)

@app.route('/')
def webpage():
    return render_template('index.html', title='covid daily update', local_7day_infections='last_7days')

@app.route('/index')

def return_home():
    return redirect('/')
app.run()


news = news_API_request()
closed_news = []

def removing_news():
    article = request.args.get('notif')
    logging.info("Request to close news article made")
    closed_news.append(article)

    for article in news:
        if article['title'] in closed_news:
            news.remove(article)
            logging.info("news article removed from news list")

    return news




@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def dashboard():

    '''this fucntion deal with the dashbaord and linking it to the html'''
    last_7days, current_hospital_cases, total_deaths = covid_API_resquest('England', 'Nation')
    local_average = covid_API_resquest()[2]
    logging.info("covid data API requests made")
    update_schedules = []

    hospital_cases = "National hospital cases:", str(hospital_cases)
    deaths = "National death total: ", str(deaths)

    if request.method == 'GET':

      
        text_field = request.args.get('two')
        if text_field:
            update_time = request.args.get('update')
            covid_data = request.args.get('covid-data')
            news_update = request.args.get('news')
            repeat = request.args.get('repeat')
            
            
            logging.debug("schedule to be update at: "+update_time+" ,Name: "+text_field+" To update: " +
                          covid_data + news_update+" "+repeat)
           

        return render_template(
            'index.html', 
            title='Covid Dashboard', 
            news_articles=news, 
            deaths_total=total_deaths,
            hospital_cases=current_hospital_cases, 
            national_7day_infections=last_7days,
            local_7day_infections=local_average, 
            updates=update_schedules, 
            image='covid_19_photo.png',
            notif=removing_news())

app.run()


