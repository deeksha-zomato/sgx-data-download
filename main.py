import sys
from script import *
from datetime import date
from datetime import timedelta

if len(sys.argv) > 1:
    download_date = sys.argv[1]
else:
    # Get today's date
    today = date.today()
    #set default date as today's date
    download_date = str(today.strftime("%d %b %Y"))

# Calling download_data function
download_data(download_date)