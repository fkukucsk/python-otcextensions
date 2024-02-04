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
from openstack import resource


class Metrics(resource.Resource):
    base_path = "/datasets/%(dataset_id)s/metrics"

    resource_key = "metrics"

    allow_fetch = True

    #: Dataset ID.
    dataset_id = resource.URI("dataset_id")

    # Properties
    #: End time of the monitoring information.
    end_time = resource.Body("end_time", type=float)
    #: Start time of the monitoring information.
    start_time = resource.Body("start_time", type=float)
    #: ID of a team labeling task.
    workforce_task_id = resource.Body("workforce_task_id", type=str)






