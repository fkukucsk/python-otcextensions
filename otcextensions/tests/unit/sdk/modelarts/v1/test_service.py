# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from openstack.tests.unit import base

from otcextensions.sdk.modelarts.v1 import service
from otcextensions.tests.unit.sdk.modelarts.v1.examples \
    import EXAMPLE_SERVICE as EXAMPLE


class TestService(base.TestCase):

    def setUp(self):
        super(TestService, self).setUp()

    def test_basic(self):
        sot = service.Service()

        self.assertEqual('/services', sot.base_path)
        # self.assertEqual('', sot.resource_key)
        # self.assertEqual('', sot.resources_key)

        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_fetch)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_delete)
        self.assertFalse(sot.allow_commit)

    def test_make_it(self):
        updated_sot_attrs = []
        sot = service.Service(**EXAMPLE)
        # self.assertEqual(EXAMPLE['create_time'], sot.created_at)

        for key, value in EXAMPLE.items():
            if key not in updated_sot_attrs:
                print("key", key, "\nvalue:", value)
                self.assertEqual(getattr(sot, key), value)
