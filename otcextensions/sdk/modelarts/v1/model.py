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
# import six
from openstack import resource
from openstack import exceptions
import json


class Model(resource.Resource):
    base_path = '/models'

    resources_key = 'models'

    allow_create = True
    allow_list = True
    allow_commit = False
    allow_delete = True
    allow_fetch = True
    allow_patch = False

    _query_mapping = resource.QueryParameters(
        'name',
        'model_version',
        'status',
        'model_type',
        'not_model_type',
        'description',
        'offset',
        'limit',
        'sort_by',
        'order',
        'workspace_id',
        name='model_name',
        status='model_status'
    )

    # Properties
    #: Model name. The value can contain 1 to 64 visible characters,...
    #: including Chinese characters.
    #: Only letters, Chinese characters, digits, hyphens (-),...
    #: and underscores (_) are allowed.
    name = resource.Body('name', alias='model_name')
    model_name = resource.Body('model_name', alias='name')

    #: Model version in the format of Digit.Digit.Digit. ...
    #: The value range of the digits is [1, 99].
    #: Note that no part of the version number can start with 0. ...
    #: For example, 01.01.01 is not allowed.
    version = resource.Body('version', alias='model_version')
    model_version = resource.Body('model_version', alias='version')
    #: OBS path where the model is located or ...
    #: the template address of the SWR image
    source_location = resource.Body('source_location', type=str)
    source_type = resource.Body('source_type', type=str)

    #: Model type. The value can be TensorFlow, MXNet, Caffe, Spark_MLlib, ...
    #: Scikit_Learn, XGBoost, Image, or PyTorch,
    #: which is read from the configuration file.
    model_type = resource.Body('model_type', type=str)
    #: Model ID
    model_id = resource.Body('model_id', alternate_id=True)
    #: Model size, in bytes
    model_size = resource.Body('model_size', type=int)
    description = resource.Body('description', type=str)
    #: Model runtime environment
    runtime = resource.Body('runtime', type=str)
    #: Tenant to which a model belongs
    tenant_id = resource.Body('tenant', type=str)
    #: Project to which a model belongs
    project_id = resource.Body('project', type=str)
    #: User to which a model belongs
    market_flag = resource.Body('market_flag', type=bool)
    publishable_flag = resource.Body('publishable_flag', type=bool)

    owner_id = resource.Body('owner', type=str)
    status = resource.Body('status', alias='model_status')
    model_status = resource.Body('model_status', type=str, alias='status')
    execution_code = resource.Body('execution_code', type=str)
    image_address = resource.Body('image_address', type=str)
    input_params = resource.Body('input_params', type=list)
    ai_project = resource.Body('ai_project', type=str)
    output_params = resource.Body('output_params', type=list)
    dependencies = resource.Body('dependencies', type=list, list_type=dict)
    tunable = resource.Body('tunable', type=bool)
    model_metrics = resource.Body('model_metrics', type=dict)
    model_algorithm = resource.Body('model_algorithm', type=str)
    model_source = resource.Body('model_source', type=str)
    apis = resource.Body('apis', type=list, list_type=dict)
    model_labels = resource.Body('model_labels', type=list)
    labels_map = resource.Body('labels_map', type=dict)
    workspace_id = resource.Body('workspace_id', type=str)
    install_type = resource.Body('install_type', type=list)
    specification = resource.Body('specification', type=dict)
    config = resource.Body('config', type=dict)
    created_at = resource.Body('create_at', type=int)

    def _translate_response(self, response, has_body=None, error_message=None):
        """Given a KSA response, inflate this instance with its data
        DELETE operations don't return a body, so only try to work
        with a body when has_body is True.
        This method updates attributes that correspond to headers
        and body on this instance and clears the dirty set.
        """
        if has_body is None:
            has_body = self.has_body

        exceptions.raise_from_response(response, error_message=error_message)

        if has_body:
            try:
                body = response.json()
                if self.resource_key and self.resource_key in body:
                    body = body[self.resource_key]
                for key in ('model_metrics', 'config', 'apis',
                            'output_params', 'input_params'):
                    if key in body:
                        if isinstance(body[key], str):
                            body[key] = json.loads(body[key])
                        elif key in ('output_params', 'input_params') and \
                                isinstance(body[key], list):
                            for param in body[key]:
                                if isinstance(param.get('param_desc'), str):
                                    param['param_desc'] = json.loads(
                                        param['param_desc'])

                # Do not allow keys called "self" through. Glance chose
                # to name a key "self", so we need to pop it out because
                # we can't send it through cls.existing and into the
                # Resource initializer. "self" is already the first
                # argument and is practically a reserved word.
                body.pop("self", None)
                body_attrs = self._consume_body_attrs(body)
                if self._allow_unknown_attrs_in_body:
                    body_attrs.update(body)
                    self._unknown_attrs_in_body.update(body)
                elif self._store_unknown_attrs_as_properties:
                    body_attrs = self._pack_attrs_under_properties(
                        body_attrs, body
                    )

                self._body.attributes.update(body_attrs)
                self._body.clean()
                if self.commit_jsonpatch or self.allow_patch:
                    # We need the original body to compare against
                    self._original_body = body_attrs.copy()
            except ValueError:
                # Server returned not parse-able response (202, 204, etc)
                # Do simply nothing
                pass

        headers = self._consume_header_attrs(response.headers)
        self._header.attributes.update(headers)
        self._header.clean()
