"""
    tests.logging
    ~~~~~~~~~~~~~

    This is more like examples than unittest for logging.
"""

import os
import unittest
import tempfile

from zask import Zask


class TestLogging(unittest.TestCase):

    def setUp(self):
        fd, path = tempfile.mkstemp()
        self.default_config = {
            "DEBUG": True,
            "ERROR_LOG": path
        }

    def tearDown(self):
        os.unlink(self.default_config['ERROR_LOG'])

    def test_debug_mode(self):
        app = Zask(__name__)
        app.config = self.default_config
        app.logger.debug("debug")
        app.logger.info("info")
        app.logger.error("error")
        app.logger.exception("exception")

    def test_prod_mode(self):
        app = Zask(__name__)
        app.config = self.default_config
        app.config['DEBUG'] = False
        app.config['PRODUCTION_LOGGING_LEVEL'] = 'warning'
        app.logger.debug("debug")
        app.logger.info("info")
        app.logger.warning("warning")
        app.logger.error("error")
        app.logger.exception("exception")

        print('')
        print('printing file:')
        with open(app.config['ERROR_LOG'], 'r') as fin:
            print(fin.read())

    def test_prod_class(self):
        app = Zask(__name__)
        app.config = self.default_config
        app.config['DEBUG'] = False
        app.config['PRODUCTION_LOGGING_CLASS'] = 'WatchedFileHandler'

        app.logger.debug("debug")
        app.logger.info("info")
        app.logger.warning("warning")
        app.logger.error("error")
        app.logger.exception("exception")

        self.assertEqual(len(app.logger.handlers), 1)
        hdlr = app.logger.handlers[0]
        self.assertEqual(hdlr.__class__.__name__, 'WatchedFileHandler')

        print('')
        print('printing file:')
        with open(app.config['ERROR_LOG'], 'r') as fin:
            print(fin.read())


if __name__ == '__main__':
    unittest.main()
