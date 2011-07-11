from django.contrib import admin
from django.utils.translation import ugettext as _

from models import JLogger


class JLoggerAdmin(admin.ModelAdmin):
    list_filter = ('level', 'appname')
    search_fields = ['message', 'user']
    ordering = ['-created']
    list_display = ['level_icon', 'message', 'created', 'appname']
    list_display_links = ['message']
    readonly_fields = ('created', 'filename', 'lineno', 'message', 'exc_info',
                       'level', 'appname', 'funcname', 'process', 'uname',
                       'user', 'user_email', 'pre_arguments')
    fieldsets = (
        (_('Log Info'), {
        'fields': (('level', 'message', 'created'),)
        }),
        (_('Code Info'), {
        'fields': ('appname', 'filename', 'lineno', 'funcname')
        }),
        (_('User Info'), {
        'fields': (('user', 'user_email'),)
        }),
        (_('Executional Info'), {
        'fields': ('exc_info', 'process', 'uname', 'pre_arguments')
        }),
    )


admin.site.register(JLogger, JLoggerAdmin)
