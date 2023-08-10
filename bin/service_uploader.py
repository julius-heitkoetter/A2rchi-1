import os
from threading import Thread

from interfaces.uploader_app import app
from utils.scraper import Scraper
from utils.data_manager import DataManager

#flag that if set to true, will stop all the threads
#configured so that if any thread fails, they all stop
stop_jobs = False 

def run_app():
    """
    Function which runs the flask app. 
    Note, before the flask app is run, the 
    data manager should be run to create the 
    necessary directories. 
    """
    global stop_jobs

    try:
        app.run(debug=False, port=5003)
    except:
        stop_jobs = True

    return

def run_scraper():
    """
    function which runs the scraper app
    """
    global stop_jobs

    scraper=Scraper()

    while not stop_jobs:
        try:
            print("Starting hard scrape")
            scraper.hard_scrape(verbose=True)
            print("Completed hard scrape")
        except:
            stop_jobs = True
        os.system("sleep 7d")
    
    return
    
def run_data_manager():
    """
    function which runs the data manager
    """
    global stop_jobs

    data_manager = DataManager()
    while not stop_jobs:
        try:
            print("Starting update vectorstore")
            data_manager.update_vectorstore()
            print("Completed update vectorstore \n")
        except:
            stop_jobs = True
        os.system("sleep 60")

    return

#create initial instance of scraper
scraper=Scraper()
scraper.hard_scrape(verbose=True)

#create initial instance of data manager
data_manager = DataManager()
data_manager.create_vectorstore()
data_manager.update_vectorstore()

#create threads
app_thread = Thread(target = run_app)
scraper_thread = Thread(target = run_scraper)
data_manager_thread = Thread(target = run_data_manager)

#Run the app, scraper, and data manager threads 
app_thread.start()
scraper_thread.start()
data_manager_thread.start()