# -*- coding: utf-8 -*-
'''
unit tests for the script engine
'''
# Import Python libs
from __future__ import absolute_import, print_function, unicode_literals

# Import Salt Testing Libs
from tests.support.mixins import LoaderModuleMockMixin
from tests.support.unit import skipIf, TestCase
from tests.support.mock import (
    NO_MOCK,
    NO_MOCK_REASON,
    patch)

# Import Salt Libs
import salt.engines.script as script
from salt.exceptions import CommandExecutionError


@skipIf(NO_MOCK, NO_MOCK_REASON)
class EngineScriptTestCase(TestCase, LoaderModuleMockMixin):
    '''
    Test cases for salt.engine.script
    '''

    def setup_loader_modules(self):
        return {
            script: {
                '__opts__': {
                    '__role': '',
                    'extension_modules': ''
                }
             }
        }

    def test__get_serializer(self):
        '''
        Test known serializer is returned or exception is raised
        if unknown serializer
        '''
        self.assertTrue(script._get_serializer('yaml'))

        with self.assertRaises(CommandExecutionError):
            script._get_serializer('bad')

    def test__read_stdout(self):
        '''
        Test we can yield stdout
        '''
        with patch('subprocess.Popen') as popen_mock:
            popen_mock.stdout.readline.return_value = 'test'
            self.assertEqual(next(script._read_stdout(popen_mock)), 'test')
