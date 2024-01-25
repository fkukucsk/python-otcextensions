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
#
from openstack.tests.unit import base
from otcextensions.sdk.modelartsv2.v2 import dataset

EXAMPLE = {
    "label_stats": [
        {
            "name": "daisy",
            "type": 0,
            "property": {"@modelarts:color": "#266b5e"},
            "count": 0,
            "sample_count": 0,
        },
        {
            "name": "dandelion",
            "type": 0,
            "property": {"@modelarts:color": "#1a0135"},
            "count": 0,
            "sample_count": 0,
        },
    ],
    "sample_stats": {
        "un_annotation": 500,
        "all": 500,
        "total": 500,
        "deleted": 0,
        "manual_annotation": 0,
        "auto_annotation": 0,
        "lefted": 500,
    },
    "key_sample_stats": {
        "total": 500,
        "non_key_sample": 500,
        "key_sample": 0,
    },
    "deletion_stats": {},
    "metadata_stats": {},
    "data_spliting_enable": False,
}


class TestStatistics(base.TestCase):
    def setUp(self):
        super(TestStatistics, self).setUp()

    def test_basic(self):
        sot = dataset.Statistics()

        self.assertEqual(
            "/datasets/%(dataset_id)s/data-annotations/stats", sot.base_path
        )
        self.assertEqual(None, sot.resource_key)
        self.assertEqual(None, sot.resources_key)

        self.assertFalse(sot.allow_list)
        self.assertTrue(sot.allow_fetch)
        self.assertFalse(sot.allow_create)
        self.assertFalse(sot.allow_delete)
        self.assertFalse(sot.allow_commit)

    def test_make_it(self):
        updated_sot_attrs = ("data_spliting_enable",)
        sot = dataset.Statistics(**EXAMPLE)
        self.assertEqual(
            EXAMPLE["data_spliting_enable"], sot.is_data_spliting_enabled
        )

        for key, value in EXAMPLE.items():
            if key not in updated_sot_attrs:
                self.assertEqual(getattr(sot, key), value)
