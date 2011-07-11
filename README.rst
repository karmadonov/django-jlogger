--------------
django-jlogger
--------------

Simple logging to a database for Django

======
Setup
======

Grab the git repository from github and run setup.py:

        (({git clone git://github.com/django-jlogger/django-jlogger.git}))
        (({$ cd django-jlogger}))
        (({$ python setup.py install}))

=======
Install
=======

Just update your settings.py and add jlogger to ``INSTALLED_APPS``::

        INSTALLED_APPS = (
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.sites',
            'django.contrib.admin',
            ...
            'jlogger',
            ...
        )

=============
Configuration
=============

If you want to use some additional settings, you can add to settings.py this settings.

################################
Alternative database for logging
################################

If you want use a alternative database to store error logs, you must add this database to DATABASES, example:

        DATABASES = {
            'default': {
                ...
            },
            'logs': {
                ...
            }
        }

then add JLoggerRouter to DATABASE_ROUTERS:

        DATABASE_ROUTERS = ['jlogger.routers.JLoggerRouter']

and add to JLOGGER settings:

        JLOGGER = {
            ...
            'database': 'logs',
            ...
        }

################
Mailing settings
################

For using mail notification add to JLOGGER settings:

        MANAGERS = (
            ('Kirill', 'kirill@example.com'),
        )

        JLOGGER = {
            ...
            # Address that will be sent a letter
            'mail_from': 'logging@jazzrate.com',
            # Whom will be sent an email
            'mail_to': MANAGERS,
            # Log level for send notification
            'mail_if': ('ERROR', 'WARNING', 'CRITICAL'),
            ...
        }

################
Handle exception
################

Not recommended, but you can use ProcessExceptionMiddleware for automatic logging exception, just add it to MIDDLEWARE_CLASSES:

        MIDDLEWARE_CLASSES = (
            ...
            'jlogger.middleware.ProcessExceptionMiddleware',
            ...
        )
