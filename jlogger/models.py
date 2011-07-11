import sys
import inspect
import os

from django.db import models
from django.core.mail import send_mail
from django.conf import settings
from django.utils.translation import ugettext as _


class JLogger(models.Model):
    """
        List of attributes:
            created    - time when the log record was created
            filename   - full pathname of the source file where the
                         logging call was issued
            lineno     - source line number where the logging call
                         was issued
            message    - the logged message
            exc_info   - exception tuple (if available)
            level      - numeric logging level for the message
                         e.g. DEBUG, INFO, WARNING, ERROR, CRITICAL
            funcname   - name of function containing the logging call
            process    - process ID (if available)
            uname      - information identifying the current OS
            user       - name of the user that send request
            user_email - email of the user that send request
            arguments  - information about arguments of caller function
    """

    LEVEL_CHOICES = (
        ('D', _('DEBUG')),
        ('I', _('INFO')),
        ('W', _('WARNING')),
        ('E', _('ERROR')),
        ('C', _('CRITICAL'))
    )

    created = models.DateTimeField(_('Date created'), auto_now_add=True)
    filename = models.CharField(_('File name'), max_length=200)
    lineno = models.IntegerField(_('Line number'))
    message = models.TextField(_('Message'))
    exc_info = models.CharField(_("Exception info"),
        max_length=200, null=True, blank=True,
        help_text=_("Exception that is currently being handled"))
    level = models.CharField(_('Log level'),
        max_length=1, choices=LEVEL_CHOICES)
    appname = models.CharField(_("Application name"),
        max_length=50, null=True, blank=True)
    funcname = models.CharField(_('Function name'), max_length=100)
    process = models.IntegerField(_("Process ID"),
        null=True, blank=True,
        help_text=_("(if available)"))
    uname = models.CharField(_("Current OS"),
        max_length=200, null=True, blank=True,
        help_text=_("Information identifying the current OS"))
    user = models.CharField(_('User'), max_length=30)
    user_email = models.CharField(_('User email'),
        max_length=75, null=True, blank=True)
    arguments = models.TextField(_('Arguments'),
        help_text=_("Information about arguments of caller function"))

    def log(self, level, msg):
        self.level = _get_level(level)
        self.message = msg
        exec_frame = sys._getframe(2)
        code_info = inspect.getframeinfo(exec_frame, context=0)
        self.filename = code_info[0][:200]
        self.lineno = int(code_info[1])
        self.funcname = code_info[2][:100]
        for item in settings.INSTALLED_APPS:
            if item in self.filename:
                self.appname = item
                break
        if sys.exc_info()[0] is not None:
            self.exc_info = sys.exc_info()[:200]
            sys.exc_clear()
        try:
            self.uname = os.uname()
            self.process = int(os.getpid())
        except:
            pass
        self.arguments = str(inspect.getargvalues(exec_frame))
        if 'request' in inspect.getargvalues(exec_frame)[3]:
            request = inspect.getargvalues(exec_frame)[3]['request']
            if request.user.is_authenticated():
                self.user = str(request .user)
                self.user_email = request.user.email
            else:
                self.user = 'AnonymousUser'
        self.save()
        self._send_error()


    def _send_error(self):
        """ If settings defined, then send message"""
        if (getattr(settings, 'JLOGGER', None) and
            'mail_to' in settings.JLOGGER and
            'mail_if' in settings.JLOGGER and
            _get_level_name(self.level) in settings.JLOGGER['mail_if']):
            subject = _("Oops, new log entry in JLogger with level %s!") % \
                _get_level_name(self.level)
            message = _("Log message:\n%s\n") % self.message
            message += _("In application: %s\n\n") % self.appname
            if getattr(settings, 'SITE_URL', None):
                message += _("Details: %s" % settings.SITE_URL)
            if 'mail_from' in settings.JLOGGER:
                mail_from = settings.JLOGGER['mail_from']
            else:
                mail_from = settings.JLOGGER['mail_to'][0][1]
            mail_to = []
            for user in settings.JLOGGER['mail_to']:
                mail_to.append(user[1])
            send_mail(subject, message, mail_from, mail_to, fail_silently=True)

    def level_icon(self):
        if self.level == 'W':
            return """<img src="/static/admin/img/admin/icon_alert.gif"
                      title="Warning">"""
        elif self.level == 'I':
            return """<img src="/static/admin/img/admin/icon_success.gif"
                      title="Info">"""
        elif self.level == 'D':
            return """<img src="/static/admin/img/admin/selector-search.gif"
                      title="Debug">"""
        elif self.level == 'E':
            return """<img src="/static/admin/img/admin/icon_error.gif"
                      title="Error">"""
        elif self.level == 'C':
            return """<img src="/static/admin/img/admin/icon_deletelink.gif"
                      title="Critical">"""
        else:
            return self.level
    level_icon.short_description = _('Level')
    level_icon.allow_tags = True

    def pre_arguments(self):
        return "<br><pre>%s</pre>" % self.arguments
    pre_arguments.short_description = _('Arguments')
    pre_arguments.allow_tags = True

    def __unicode__(self):
        return '%s - %s - %s' % (self.level, self.appname, self.message)

    class Meta:
        verbose_name = u'log'
        verbose_name_plural = u'logs'


def _get_level(level):
    """ Convert level name to one chars symbols
    """
    if level in ('1', 'D', 'DEBUG'):
        return 'D'
    if level in ('2', 'I', 'INFO'):
        return 'I'
    if level in ('3', 'W', 'WARNING'):
        return 'W'
    if level in ('4', 'E', 'ERROR'):
        return 'E'
    if level in ('5', 'C', 'CRITICAL'):
        return 'C'


def _get_level_name(level):
    """ Convert one chars symbols to level name
    """
    if level is 'D':
        return 'DEBUG'
    if level is 'I':
        return 'INFO'
    if level is 'W':
        return 'WARNING'
    if level is 'E':
        return 'ERROR'
    if level is 'C':
        return 'CRITICAL'


def _get_settings():
    """ Generate settings for jlogger """
    log_settings = getattr(settings, 'JLOGGER', {})

    # If database not setup in settings, then using False
    if 'database' not in log_settings:
        log_settings['database'] = None

    # If mail_to not setup in settings, then sending mail to ADMIN
    # or if ADMIN not undefined then don't use emails
    if 'mail_to' not in log_settings:
        if getattr(settings, 'ADMIN', None):
            log_settings['mail_to'] = settings.ADMIN
        else:
            log_settings['mail_to'] = None

    # If mail_if not setup in settings, then using default settings
    if 'mail_if' not in log_settings:
        log_settings['mail_if'] = ('ERROR', 'CRITICAL')
    return log_settings
