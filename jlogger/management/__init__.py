# Creating database for logs on post_syncdb
from django.db.models.signals import post_syncdb
from django.core.management import call_command

import jlogger.models


def post_sync(sender, db, **kwargs):
    log_settings = jlogger.models._get_settings()
    if db != log_settings['database']:
        call_command('syncdb', database=log_settings['database'])

if jlogger.models._get_settings()['database']:
    post_syncdb.connect(post_sync, sender=jlogger.models)
