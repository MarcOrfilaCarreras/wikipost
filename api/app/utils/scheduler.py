from app.extensions import logging
from apscheduler.events import EVENT_JOB_ERROR
from apscheduler.events import EVENT_JOB_EXECUTED
from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.jobstores.base import JobLookupError
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.schedulers.background import BackgroundScheduler


class Scheduler(object):
    REDIS_HOST = None
    REDIS_PORT = None
    REDIS_DB = None

    WORKER = None

    def __init__(self, redis_host=None, redis_port=None, redis_db=None):
        if not ((redis_host is None) or (redis_port is None) or (redis_db is None)):
            Scheduler.REDIS_HOST = redis_host
            Scheduler.REDIS_PORT = redis_port
            Scheduler.REDIS_DB = redis_db

            logging.info('[SCHEDULER] Initialized with Redis at %s:%d (DB %d)',
                         Scheduler.REDIS_HOST, Scheduler.REDIS_PORT, Scheduler.REDIS_DB)

    def listener(self, event):
        if event.exception:
            logging.error(
                f'[SCHEDULER] Job {event.job_id} failed with error: {event.exception}')
        else:
            logging.info(
                f'[SCHEDULER] Job {event.job_id} completed successfully.')

    def connect(self):
        if (Scheduler.REDIS_HOST is None) or (Scheduler.REDIS_PORT is None) or (Scheduler.REDIS_DB is None):
            raise ValueError('Redis connection details are missing')

        jobstores = {
            'default': RedisJobStore(host=Scheduler.REDIS_HOST, port=Scheduler.REDIS_PORT, db=Scheduler.REDIS_DB)
        }

        executors = {
            'default': ThreadPoolExecutor(5)
        }

        Scheduler.WORKER = BackgroundScheduler(
            jobstores=jobstores, executors=executors)
        Scheduler.WORKER.add_listener(
            self.listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)

        logging.info('[SCHEDULER] Worker initialized and listener added')

    def add_job(self, job_function, cron='0 0 * * *', **kwargs):
        if Scheduler.WORKER is None:
            raise RuntimeError(
                "Scheduler worker is not initialized. Call 'connect' first")

        if cron:
            parts = cron.strip().split()

            if len(parts) != 5:
                raise ValueError(
                    'Cron string must have exactly 5 fields: minute, hour, day, month, day_of_week')

            minute, hour, day, month, day_of_week = parts
            kwargs.update({
                'minute': minute,
                'hour': hour,
                'day': day,
                'month': month,
                'day_of_week': day_of_week
            })

        job = Scheduler.WORKER.add_job(
            job_function, 'cron', misfire_grace_time=None, **kwargs)
        logging.info(f'[SCHEDULER] Job {job.id} added')

        return job

    def delete_job(self, id):
        if Scheduler.WORKER is None:
            raise RuntimeError(
                "Scheduler worker is not initialized. Call 'connect' first")

        try:
            Scheduler.WORKER.remove_job(id)
        except JobLookupError as e:
            pass
        except Exception as e:
            return False

        logging.info(f'[SCHEDULER] Job {id} deleted')

        return True

    def start(self):
        if Scheduler.WORKER is None:
            raise RuntimeError(
                "Scheduler worker is not initialized. Call 'connect' first")

        Scheduler.WORKER.start()
        logging.info('[SCHEDULER] Started')
