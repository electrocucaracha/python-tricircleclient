# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import six
import testtools

import fixtures
from oslo_utils import encodeutils

from tricircleclient import exceptions


class TestExceptions(testtools.TestCase):

    def test_exception_print_with_unicode(self):
        class TestException(exceptions.ClientException):
            pass

        multibyte_unicode_string = u'\uff21\uff22\uff23'
        e = TestException(message=multibyte_unicode_string)

        fixture = fixtures.StringStream('stdout')
        self.useFixture(fixture)
        with fixtures.MonkeyPatch('sys.stdout', fixture.stream):
            print(e)
        self.assertEqual(multibyte_unicode_string,
                         fixture.getDetails().get('stdout').as_text())

    def test_exception_message_with_encoded_unicode(self):
        class TestException(exceptions.ClientException):
            pass

        multibyte_string = u'\uff21\uff22\uff23'
        multibyte_binary = encodeutils.safe_encode(multibyte_string)
        e = TestException(message=multibyte_binary)
        self.assertEqual(multibyte_string, six.text_type(e))
