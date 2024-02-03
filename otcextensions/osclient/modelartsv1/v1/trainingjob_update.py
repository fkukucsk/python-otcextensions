
#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
#
"""ModelArts training job v1 action implementations"""
import logging

from osc_lib import exceptions
from osc_lib import utils
from osc_lib.cli import parseractions
from osc_lib.command import command
from otcextensions.common import cli_utils
from otcextensions.common import sdk_utils
from otcextensions.i18n import _

LOG = logging.getLogger(__name__)

class TrainingJobUpdate(command.ShowOne):
    _description = _('Modify the description of a training job')

    def get_parser(self, prog_name):
        parser = super(TrainingJobUpdate, self).get_parser(prog_name)
        parser.add_argument('--job_id', metavar='<job_id>', required=True, type=int, help=_('ID of a training job'))
        parser.add_argument('--job_desc', metavar='<job_desc>', required=True, type=str, help=_('Description of a training job'))
        return parser

    def take_action(self, parsed_args):      
        client = self.app.client_manager.modelartsv1
        attrs = {}
        args_list = ['job_id', 'job_desc']
        for arg in args_list:
            val = getattr(parsed_args, arg)
            if val:
                attrs[arg] = val

        client.modify_trainingjob_description(**attrs)
    
