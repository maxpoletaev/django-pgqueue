from datetime import timedelta
from functools import wraps
import copy

from django.utils import timezone

ATTEMPT_COUNTER = 'retry_attempt'


def _delay(seconds):
    return timezone.now() + timedelta(seconds=seconds)


def repeat(interval):
    """
    Endlessly repeats a task, every `delay` (a timedelta).

        @repeat(datetime.timedelta(minutes=5)
        def task(queue, job):
            pass

    This will run `task` every 5 minutes. It's up to you to kick off the first
    task, though.
    """
    def wrapper(func):
        @wraps(func)
        def decorator(queue, job):
            queue.enqueue_once(job.task, job.kwargs, execute_at=(timezone.now() + interval))
            return func(queue, job)
        return decorator
    return wrapper


def retry(exceptions, delay, max_attempts):
    """
    Retries failed task every `interval` (a timedelta).

        @retry([Exception], delay=timedelta(seconds=30), max_attempts=10)
        def task(queue, job):
            pass

    This will repeat `task` every 30 seconds if it fails with `Exception`
    but not more than ten times. When `max_attempts` is reached,
    the original exception will be raised.
    """
    def wrapper(func):
        @wraps(func)
        def decorator(queue, job):
            try:
                return func(queue, job)
            except Exception as e:
                if not isinstance(e, tuple(exceptions)) or queue is None:
                    raise

                attempt = job.context.get(ATTEMPT_COUNTER, 0) + 1
                if attempt > max_attempts:
                    raise

                context = copy.deepcopy(job.context)
                context[ATTEMPT_COUNTER] = attempt
                execute_at = timezone.now() + delay
                queue.enqueue(job.task, job.kwargs, context=context, execute_at=execute_at)

        return decorator
    return wrapper
