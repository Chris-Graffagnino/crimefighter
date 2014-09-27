from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
from datetime import datetime
from crimeapp.models import TaskHistory
from utils import getcrime

logger = get_task_logger(__name__)


# A periodic task that will run every minute (the symbol "*" means every)
@periodic_task(run_every=(crontab(hour="*", minute="*", day_of_week="*")), ignore_result=False)
def scraper_example():
    logger.info("Start task")
    now = datetime.now()
    date_now = now.strftime("%d-%m-%Y %H:%M:%S")
    # Perform all the operations you want here
    temp_crime = getcrime.create_daily_booking_list()
      
    # The name of the Task, use to find the correct TaskHistory object
    name = "scraper_example"
    taskhistory = TaskHistory.objects.get_or_create(name=name)[0]
    taskhistory.history.update({date_now: result})
    taskhistory.save()
    result_name = "Bob"
    resulttest = Result.objects.get_or_create(result_name=result_name)[0]
    result.history.update({result: result})
    resulttest.save()
    logger.info("Task finished: result = %i" % result)

    
    

