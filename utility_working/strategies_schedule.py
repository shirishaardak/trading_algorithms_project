
import schedule
from datetime import datetime
import time

def strategies_schedule(schedule_funcation, schedule_timeframe):
    schedule.every(schedule_timeframe).minutes.do(schedule_funcation)
    while True:         
        if  (datetime.now().minute == (0 or 15 or 30 or 45)):
            while True:                                           
                schedule.run_pending()
                time.sleep(1)
