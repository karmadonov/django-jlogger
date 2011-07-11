from django.test import TestCase
from models import _get_level_name, _get_level, JLogger
from jlogger import logger

class JloggerTest(TestCase):
    def test_get_level_name(self):
        """
        Dummy tests that _get_level_name always return result
        """
        self.assertEqual(_get_level_name('D'), 'DEBUG')
        self.assertEqual(_get_level_name('I'), 'INFO')
        self.assertEqual(_get_level_name('W'), 'WARNING')
        self.assertEqual(_get_level_name('E'), 'ERROR')
        self.assertEqual(_get_level_name('C'), 'CRITICAL')

    def test_get_level(self):
        """
        Dummy tests that _get_level always return result
        """
        for level in ('1', 'D', 'DEBUG'):
            self.assertEqual(_get_level(level), 'D')
        for level in ('2', 'I', 'INFO'):
            self.assertEqual(_get_level(level), 'I')
        for level in ('3', 'W', 'WARNING'):
            self.assertEqual(_get_level(level), 'W')
        for level in ('4', 'E', 'ERROR'):
            self.assertEqual(_get_level(level), 'E')
        for level in ('5', 'C', 'CRITICAL'):
            self.assertEqual(_get_level(level), 'C')

    def test_logger(self):
        logger.debug('Debug log')
        logger.info('Info log')
        logger.warning('Info warning')
        logger.error('Info error')
        logger.critical('Info critical')
        logs = JLogger.objects.all()
        self.assertEqual(len(logs), 5)