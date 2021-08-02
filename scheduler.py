import schedule
import time
from script import *

from datetime import date
from datetime import timedelta

# Get today's date
today = date.today()

# Yesterday date
yesterday = today - timedelta(days=1)

# schedule downloading data every day for previous date at 6:00 pm considering data gets uploaded at sgx before that
schedule.every().tuesday.at("18:00").do(download_data, yesterday.strftime("%d %b %Y"))
schedule.every().wednesday.at("18:00").do(download_data, yesterday.strftime("%d %b %Y"))
schedule.every().thursday.at("18:00").do(download_data, yesterday.strftime("%d %b %Y"))
schedule.every().friday.at("18:00").do(download_data, yesterday.strftime("%d %b %Y"))
schedule.every().saturday.at("18:00").do(download_data, yesterday.strftime("%d %b %Y"))

while True:
    schedule.run_pending()
    time.sleep(5*60)
