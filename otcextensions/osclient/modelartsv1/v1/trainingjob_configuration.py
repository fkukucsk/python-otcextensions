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
"""ModelArts training job configuration v1 action implementations"""
import logging

from osc_lib import utils
from osc_lib.command import command
from otcextensions.common import cli_utils
from otcextensions.common import sdk_utils
from otcextensions.i18n import _

LOG = logging.getLogger(__name__)

_formatters = {
    "create_time": cli_utils.UnixTimestampFormatter,
}
#     "config": cli_utils.YamlFormat}


def _flatten_output(obj):
    data = {
        "is_success": obj.is_success,
        "config_total_count": obj.config_total_count,
        "configs": obj.configs,
    }
    return data


def _get_columns(item):
    column_map = {}
    return sdk_utils.get_osc_show_columns_for_sdk_resource(item, column_map)


class DeleteTrainingJobConfiguration(command.Command):
    _description = _(
        "This API is used to delete a training job configuration."
    )

    def get_parser(self, prog_name):
        parser = super(DeleteTrainingJobConfiguration, self).get_parser(
            prog_name
        )
        parser.add_argument(
            "configName",
            metavar="<configName>",
            help=_("Name of a training job configuration"),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv1
        client.delete_trainingjob_configuration(
            config_name=parsed_args.configName
        )


class CreateTrainingJobConfiguration(command.ShowOne):
    _description = _(
        "This API is used to create a training job configuration."
    )

    def get_parser(self, prog_name):
        parser = super(CreateTrainingJobConfiguration, self).get_parser(
            prog_name
        )
        parser.add_argument(
            "--config-name",
            metavar="<config_name>",
            required=True,
            help=_(
                "Name of a training job configuration. The value is a "
                "string of 1 to 64 characters consisting of only digits, "
                "letters, underscores (_), and hyphens (-)."
            ),
        )
        parser.add_argument(
            "--config-desc",
            metavar="<config_desc>",
            help=_(
                "Description of a training job configuration. The value "
                "is a string of 0 to 256 characters. By default, this "
                "parameter is left blank."
            ),
        )
        parser.add_argument(
            "--worker-server-num",
            metavar="<worker_server_num>",
            required=True,
            help=_("Number of workers in a training job."),
        )
        parser.add_argument(
            "--app-url",
            metavar="<app_url>",
            required=True,
            help=_(
                "Code directory of a training job, for example, /usr/app/."
            ),
        )
        parser.add_argument(
            "--boot-file-url",
            metavar="<boot_file_url>",
            required=True,
            help=_(
                "Boot file of a training job, which needs to be stored "
                "in the code directory, for example, /usr/app/boot.py."
            ),
        )
        parser.add_argument(
            "--model-id",
            metavar="<model_id>",
            help=_(
                "Model ID of a training job. After setting model_id, "
                "you do not need to set app_url or boot_file_url, and "
                "engine_id."
            ),
        )
        parser.add_argument(
            "--parameter",
            metavar="<parameter>",
            help=_(
                "Running parameters of a training job. It is a collection "
                "of label-value pairs."
            ),
        )
        parser.add_argument(
            "--spec-id",
            metavar="<spec_id>",
            required=True,
            help=_(
                "ID of the resource specifications selected for a "
                "training job."
            ),
        )
        parser.add_argument(
            "--data-url",
            metavar="<data_url>",
            required=True,
            help=_("data_url"),
        )
        parser.add_argument(
            "--dataset-id",
            metavar="<dataset_id>",
            required=True,
            help=_("Dataset ID of a training job."),
        )
        parser.add_argument(
            "--dataset-version-id",
            metavar="<dataset_version_id>",
            required=True,
            help=_("Dataset version ID of a training job."),
        )
        parser.add_argument(
            "--data-source",
            metavar="<data_source>",
            required=True,
            help=_(" "),
        )
        parser.add_argument(
            "--engine-id",
            metavar="<engine_id>",
            required=True,
            help=_(
                "ID of the engine selected for a training job. "
                "The default value is 1."
            ),
        )
        parser.add_argument(
            "--train-url",
            metavar="<train_url>",
            help=_(
                "OBS URL of the output file of a training job. "
                "By default, this parameter is left blank."
            ),
        )
        parser.add_argument(
            "--log-url",
            metavar="<property>",
            help=_(
                "OBS URL of the logs of a training job. "
                "By default, this parameter is left blank."
            ),
        )
        parser.add_argument(
            "--user-image-url",
            metavar="<user_image_url>",
            help=_("SWR URL of a custom image used by a training job."),
        )
        parser.add_argument(
            "--user-command",
            metavar="<user_command>",
            help=_(
                "Boot command used to start the container of a custom "
                "image of a training job. "
            ),
        )
        parser.add_argument(
            "--dataset-version",
            metavar="<dataset_version>",
            required=True,
            help=_("Dataset version ID of a training job."),
        )
        parser.add_argument(
            "--type",
            metavar="<type>",
            required=True,
            help=_(
                "Dataset type. The value can be obs or dataset. OBS and "
                "dataset cannot be used at the same time."
            ),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv1

        attrs = {}
        if parsed_args.config_name:
            attrs["config_name"] = parsed_args.config_name
        if parsed_args.config_desc:
            attrs["config_desc"] = parsed_args.config_desc
        if parsed_args.worker_server_num:
            attrs["worker_server_num"] = parsed_args.worker_server_num
        if parsed_args.app_url:
            attrs["app_url"] = parsed_args.app_url
        if parsed_args.boot_file_url:
            attrs["boot_file_url"] = parsed_args.boot_file_url
        if parsed_args.model_id:
            attrs["model_id"] = parsed_args.model_id
        if parsed_args.parameter:
            attrs["parameter"] = parsed_args.parameter
        if parsed_args.spec_id:
            attrs["spec_id"] = parsed_args.spec_id
        if parsed_args.data_url:
            attrs["data_url"] = parsed_args.data_url
        if parsed_args.dataset_id:
            attrs["dataset_id"] = parsed_args.dataset_id
        if parsed_args.dataset_version_id:
            attrs["dataset_version_id"] = parsed_args.dataset_version_id
        if parsed_args.data_source:
            attrs["data_source"] = parsed_args.data_source
        if parsed_args.engine_id:
            attrs["engine_id"] = parsed_args.engine_id
        if parsed_args.train_url:
            attrs["train_url"] = parsed_args.train_url
        if parsed_args.log_url:
            attrs["log_url"] = parsed_args.log_url
        if parsed_args.user_image_url:
            attrs["user_image_url"] = parsed_args.user_image_url
        if parsed_args.user_command:
            attrs["user_command"] = parsed_args.user_command
        if parsed_args.dataset_id:
            attrs["dataset_id"] = parsed_args.dataset_id
        if parsed_args.dataset_version:
            attrs["dataset_version"] = parsed_args.dataset_version
        if parsed_args.type:
            attrs["type"] = parsed_args.type

        obj = client.create_trainjobconf(**attrs)

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns)

        return display_columns, data


class ShowTrainingJobConfiguration(command.ShowOne):
    _description = _("Show details of a modelarts training job config name")

    def get_parser(self, prog_name):
        parser = super(ShowTrainingJobConfiguration, self).get_parser(
            prog_name
        )
        parser.add_argument(
            "--config_name",
            metavar="<config_name>",
            help=_("Name of a training job configuration"),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv1

        data = client.show_trainjob_conf(
            trainjob_config=parsed_args.config_name,
        )

        display_columns, columns = _get_columns(data)
        data = utils.get_item_properties(data, columns)

        return (display_columns, data)


class UpdateTrainingJobConfiguration(command.Command):
    _description = _("Update Training Job Configuration")

    def get_parser(self, prog_name):
        parser = super(UpdateTrainingJobConfiguration, self).get_parser(
            prog_name
        )
        parser.add_argument(
            "--config-name",
            metavar="<config_name>",
            help=_(
                "Service description, which contains a maximum of 100 "
                "characters. If this parameter is not set, the service "
                "description is not updated."
            ),
        )
        parser.add_argument(
            "--config-desc",
            metavar="<config_desc>",
            required=False,
            type=str,
            help=_("Description of a training job configuration"),
        )
        parser.add_argument(
            "--worker-server-num",
            metavar="<worker_server_num>",
            required=True,
            type=int,
            help=_("Number of workers in a training job"),
        )
        parser.add_argument(
            "--app-url",
            metavar="<app_url>",
            required=True,
            type=str,
            help=_("Code directory of a training job, for example, /usr/app/"),
        )
        parser.add_argument(
            "--boot-file-url",
            metavar="<boot_file_url>",
            required=True,
            type=str,
            help=_(
                "Boot file of a training job, which needs to be stored in the code directory, for example, /usr/app/boot"
            ),
        )
        parser.add_argument(
            "--model-id",
            metavar="<model_id>",
            required=True,
            type=int,
            help=_("Model ID of a training job"),
        )
        parser.add_argument(
            "--spec-id",
            metavar="<spec_id>",
            required=True,
            type=int,
            help=_(
                "ID of the resource specifications selected for a training job"
            ),
        )
        parser.add_argument(
            "--data-url",
            metavar="<data_url>",
            required=False,
            type=str,
            help=_(
                "OBS URL of the dataset required by a training job, for example, /usr/data/"
            ),
        )
        parser.add_argument(
            "--dataset-id",
            metavar="<dataset_id>",
            required=False,
            type=str,
            help=_("Dataset ID of a training job"),
        )
        parser.add_argument(
            "--dataset-version-id",
            metavar="<dataset_version_id>",
            required=False,
            type=str,
            help=_("Dataset version ID of a training job"),
        )
        parser.add_argument(
            "--engine-id",
            metavar="<engine_id>",
            required=True,
            type=int,
            help=_("ID of the engine selected for a training job"),
        )
        parser.add_argument(
            "--train-url",
            metavar="<train_url>",
            required=False,
            type=str,
            help=_("OBS URL of the output file of a training job"),
        )
        parser.add_argument(
            "--log-url",
            metavar="<log_url>",
            required=False,
            type=str,
            help=_("OBS URL of the logs of a training job"),
        )
        parser.add_argument(
            "--user-image-url",
            metavar="<user_image_url>",
            required=False,
            type=str,
            help=_("SWR URL of a custom image used by a training job"),
        )
        parser.add_argument(
            "--user-command",
            metavar="<user_command>",
            required=False,
            type=str,
            help=_(
                "Boot command used to start the container of a custom image of a training job"
            ),
        )
        parser.add_argument(
            "--dataset-version",
            metavar="<dataset_version>",
            required=False,
            type=str,
            help=_("Dataset version ID of a training job"),
        )
        parser.add_argument(
            "--type",
            metavar="<type>",
            required=False,
            type=str,
            help=_("Dataset type"),
        )
        parser.add_argument(
            "--label",
            metavar="<label>",
            required=False,
            type=str,
            help=_("Parameter name"),
        )
        parser.add_argument(
            "--value",
            metavar="<value>",
            required=False,
            type=str,
            help=_("Parameter value"),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv1
        attrs = {}
        args_list = [
            "config_name",
            "config_desc",
            "worker_server_num",
            "app_url",
            "boot_file_url",
            "model_id",
            "spec_id",
            "data_url",
            "dataset_id",
            "dataset_version_id",
            "engine_id",
            "train_url",
            "log_url",
            "user_image_url",
            "user_command",
            "dataset_version",
            "type",
            "data_url",
            "label",
            "value",
        ]
        for arg in args_list:
            val = getattr(parsed_args, arg)
            if val:
                attrs[arg] = val

        client.modify_trainingjob_configuration(
            parsed_args.config_name, **attrs
        )


class ListTrainingJobConfigurations(command.Lister):
    _description = _(
        "This API is used to query the created training "
        "job configurations that meet the search criteria."
    )
    columns = ("is_success", "config_total_count", "configs")

    def get_parser(self, prog_name):
        parser = super(ListTrainingJobConfigurations, self).get_parser(
            prog_name
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv1

        query = {}
        data = client.trainingjob_configurations(**query)

        table = (
            self.columns,
            (
                utils.get_dict_properties(_flatten_output(s), self.columns)
                for s in data
            ),
        )
        return table
