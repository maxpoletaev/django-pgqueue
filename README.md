# Django PGQueue

The project was initially forked from [django-postgres-queue][dpq] for internal use
in some of my projects. After some changes and refactoring, adding tests, features 
like warm shutdown I decided to put in on GitHub and PyPI as a standalone package
just in case.

## Installation

```
pip install django-pgqueue
```

Then add `pqueue` into `INSTALLED_APPS` and run `manage.py migrate` to create the jobs table.

## Usage

Initiate a queue object with defined tasks. This can go wherever you like and can 
be called whatever you like. For example:

```
# someapp/task_queue.py

from pqueue.queue import Queue


def say_hello(queue, job):
    name = job.kwargs['name']
    print('Hello, {}!'.format(name))


task_queue = Queue(
    tasks={
        'say_hello': say_hello,
    },
    notify_channel='someapp_task_queue',
)
```

Now define the worker command

```
# someapp/management/commands/pgqueue_worker.py

from pgqueue.worker import WorkerCommand
from someapp.queue import task_queue


class Command(WorkerCommand):
    queue = task_queue
```

And call the task this way:

```
from someapp.queue import task_queue

task_queue.enqueue('say_hello', {'name': 'Django'})
```

Please note that only primitives can be used in job’s arguments as they are stored
as JSON in the database. When you try to pass any complex non-json-serializable object,
you will get an error saying `object is not json serializable`.

## Periodic tasks

There is no built in way to run jobs periodically like celerybeat in Celery.
But you still can use cron. For example you can create a universal command
to execute any task. Something like this:

```
import json

from django.core.management import BaseCommand
from someapp.queue import task_queue


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('task_name')
        parser.add_argument('task_kwargs')

    def handle(self, task_name, task_kwargs, **options):
        task_queue.enqueue(task_name, json.loads(task_kwargs))
```

And then put it into your cron records:

```
0 0 * * *  /path/to/python manage.py run_task say_hello '{"name": "Django!"}'
```


[dpq]: https://github.com/gavinwahl/django-postgres-queue
