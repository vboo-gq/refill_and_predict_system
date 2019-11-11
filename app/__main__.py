"""Main app"""

from datetime import datetime, timedelta
import random
import time

from app import SCHEDULER, LOGGER
from app.api import download_resources, refill
from app.database import save_resources
from app.app import need_refill, max_refill_seconds, print_resources


def job_check_resources(state_id, capital_id, resource_id, do_refill):
    """Check resources and refill if necessary"""
    regions = download_resources(state_id, resource_id)
    print_resources(regions)
    save_resources(state_id, regions, resource_id)
    if do_refill and need_refill(regions, 25):
        max_seconds = max_refill_seconds(regions, 25, 900)
        random_seconds = random.randint(0, max_seconds)
        random_time_delta = timedelta(seconds=random_seconds)
        scheduled_date = datetime.now() + random_time_delta
        job_id = 'refill_{}_{}'.format(capital_id, resource_id)
        LOGGER.info(
            'Refil resource %s at %s (%s minutes)',
            resource_id,
            scheduled_date,
            round(random_time_delta.seconds / 60)
        )
        job = SCHEDULER.get_job(job_id)
        if not job:
            SCHEDULER.add_job(
                job_refill_resource,
                'date',
                args=[state_id, capital_id, resource_id],
                id=job_id,
                run_date=scheduled_date
            )

def job_refill_resource(state_id, capital_id, resource_id):
    """Execute refill job"""
    refill(state_id, capital_id, resource_id)

def add_check_resources(state_id, capital_id, resource_id, do_refill, minute):
    """Add check resources job"""
    SCHEDULER.add_job(
        job_check_resources,
        'cron',
        args=[state_id, capital_id, resource_id, do_refill],
        id='{}_check_{}'.format(state_id, resource_id),
        replace_existing=True,
        minute=minute
    )

if __name__ == '__main__':
    # job_refill_resource(2788, 4002, 0)
    # job_check_resources(2788, 4002, 0, False) # VN
    # job_check_resources(2620, 4002, 0, False) # Zeelandiae

    # VN
    add_check_resources(2788, 4008, 0, True, '0,15,30,45')
    add_check_resources(2788, 4008, 11, True, '0')
    # Zeelandiae
    add_check_resources(2620, 0, 0, False, '50')
    # Belgium
    add_check_resources(2604, 0, 0, False, '40')

    try:
        while True:
            time.sleep(100)
    except KeyboardInterrupt:
        LOGGER.info('Exiting application')
        SCHEDULER.shutdown()
        exit()
