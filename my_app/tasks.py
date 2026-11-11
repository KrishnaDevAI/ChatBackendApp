from celery import shared_task
import time

# @shared_task(bind=True, autoretry_for=(Exception,), retry_kwargs={'max_retries': 3})
# def add_numbers(self, a, b):
#     time.sleep(5)  # simulate heavy work
#     return a + b


@shared_task
def add_numbers(a, b):
    return a + b
