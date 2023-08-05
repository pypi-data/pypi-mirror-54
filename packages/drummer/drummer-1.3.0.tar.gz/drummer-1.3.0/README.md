# Drummer

Drummer is a python multi-process and multi-task job scheduler for Linux, best served as a systemd service. You can create jobs with your own tasks, and you can decide the execution flow depending on the outcome of each task.

For instance: if task A succeeds, then execute task B; if it fails, then execute task C. And, no matter the result of A, always do execute also task D.

Drummer is heavily insipired by [Comodojo Extender](https://github.com/comodojo): I wish therefore to acknowledge its author.


### Quick start

Installation is quick and easy.

> \> pip install drummer

Specify a folder where to init Drummer environment and, optionally, a filename for the internal database.

> \> drummer-admin init BASE_FOLDER [--database database_file]

During the initialization, Drummer will ask whether it should create also the related Linux systemd service file (this is the recommended choice). It will ask also which python executable to use, should you use a Virtualenv installation.

Now you are *almost* ready to start.


### How Drummer works

Drummer machinery is composed of three processes:
1. a scheduler process, built on top of [sched module](https://docs.python.org/3/library/sched.html "Python Event Scheduler")
2. a socket listener, to handle requests and responses with the Drummer cli
3. a main process, which puts together all pieces and takes care of the overall behaviour

In order to ensure the multi-tasking capability, each task is run by a separate process.

When you create a new environment for Drummer, you will notice several files and folders being created:
- the **config** folder, for configuration and task file and, if you chose so, the systemd file;
- a **database** folder, which contains the internal sqlite database with schedules;
- a **tasks** folder, for placing your tasks;
- the CLI launcher, **drummer-cli.py**.


### Configuration

Configuration is stored in file *drummer-config.yml*.

Among all, you can specify where to store the log file and the database, which folder to use for your tasks (by default, Drummer looks for them inside the **tasks** folder), how many task can be runned at the same time, and so on.


### Tasks

To be well formed, user-defined tasks should respect few basic requirements, i.e. they:
- extend the **Task** class provided by **drummer** module
- implement a **run** method as execution entry point
- use the **Response** class, along with a valid **StatusCode**, for handling the task outcome (valid **StatusCode** attributes are: "STATUS_OK", "STATUS_WARNING", "STATUS_ERROR")

A fully working example:

```
from drummer import Task, Response, StatusCode

class MyTask(Task):

    def run(self, params):

        # the Drummer logger, built on top of python logging facility
        logger = self.logger

        logger.info('Starting MyTask')

        response = Response()

        try:

            with open('mytask.txt', 'w') as f:
                f.write('Hello world!')

            logger.info('File has been updated')

            response.set_status(StatusCode.STATUS_OK)
            response.set_data({'result': 'Task ended OK'})

        except:

            response.set_status(StatusCode.STATUS_ERROR)
            response.set_data({'result': 'Task had an error'})

        finally:

            return response
```

The *run* method takes a dictionary with optional task arguments. It is empty if no arguments are specified.

To complete the registration process, you have to declare the task, along with its path, inside *drummer-tasks.yml*. Drummer must know the path of python file to load (expressed as relative path with respect to base folder), and the name of the class which exposed the *run* method.

You can automatically update the task list with the **task:update** command. Drummer will parse all valid tasks found inside the *taskdir* folder.

Of course you can also *__init__* your task class; in that case, you must take care of configuration and logger, as in the following:

```
from drummer import Task

class MyTask(Task):

    def __init__(self, config, logger):

        # init Task class
        super().__init__(config, logger)

        # your init code here
        # ...

```

### cli

You can start Drummer in two ways: as a systemd service (via *systemctl* command) or with cli, by invoking the **service:start** command.

> \> python drummer-cli.py service:start

The cli provides commands to:
- list all jobs and get info on a single job
- add, remove, enable, disable, or immediately execute a schedule
- list and execute single tasks
- automatically register valid tasks
- import and export the schedulation table

For details see:

> \> python drummer-cli.py -h
