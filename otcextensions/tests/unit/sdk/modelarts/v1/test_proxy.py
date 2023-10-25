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

from otcextensions.sdk.modelarts.v1 import _proxy
# from otcextensions.sdk.modelarts.v2 import _proxy as _proxyv2

from otcextensions.sdk.modelarts.v1 import model

from openstack.tests.unit import test_proxy_base


class TestModelartsProxy(test_proxy_base.TestProxyBase):
    def setUp(self):
        super(TestModelartsProxy, self).setUp()
        self.proxy = _proxy.Proxy(self.session)
        # self.proxy_v2 = _proxyv2.Proxy(self.session)


class TestModel(TestModelartsProxy):

    def test_model_create(self):
        self.verify_create(
            self.proxy.create_model, model.Model,
            method_kwargs={'x': 1, 'y': 2, 'z': 3},
            expected_kwargs={
                'prepend_key': False,
                'x': 1, 'y': 2, 'z': 3
            }
        )

    def test_model_delete(self):
        self.verify_delete(self.proxy.delete_model,
                           model.Model, True)

    def test_model_get(self):
        self.verify_get(self.proxy.get_model, model.Model)

    def test_models(self):
        self.verify_list(self.proxy.models, model.Model)
