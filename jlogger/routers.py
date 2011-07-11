from django.conf import settings


class JLoggerRouter(object):
    """ A router to control all database operations on models
        in the jlogger application
    """
    if getattr(settings, 'JLOGGER', None) and 'database' in settings.JLOGGER:
        using = settings.JLOGGER['database']
    else:
        using = None
    sysname = "django_jlogger"

    def db_for_read(self, model, **hints):
        """ Point all operations on jlogger models to using db
        """
        if model._meta.app_label == 'jlogger':
            return self.using
        return None

    def db_for_write(self, model, **hints):
        """ Point all operations on jlogger models to using db
        """
        if model._meta.app_label == 'jlogger':
            return self.using
        return None

    def allow_syncdb(self, db, model):
        """ Make sure the jlogger app only appears on the using db
        """
        if db == self.using:
            return model._meta.app_label == 'jlogger'
        elif model._meta.app_label == 'jlogger':
            return False
        return None
