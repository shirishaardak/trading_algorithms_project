
import schedule
from datetime import datetime
import time

def strategies_schedule(schedule_funcation, schedule_timeframe):
    schedule.every(schedule_timeframe).minutes.do(schedule_funcation)
    while True:             
            if (datetime.now().minute == 00 and datetime.now().second == 00) or (datetime.now().minute == 15 and datetime.now().second == 00) or (datetime.now().minute == 30 and datetime.now().second == 00) or (datetime.now().minute == 45 and datetime.now().second == 00):
                print(datetime.now())                                           
                schedule.run_pending()
                time.sleep(1)
