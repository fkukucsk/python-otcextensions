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
'''ModelArts data import task v2 action implementations'''
import logging

from osc_lib import utils
from osc_lib.command import command
from otcextensions.common import sdk_utils

from otcextensions.i18n import _

LOG = logging.getLogger(__name__)


def _flatten_output(obj):
    data = {
        'task_id': obj.task_id,
        'dataset_id': obj.dataset_id,
        'import_path': obj.import_path
    }
    return data


def _get_columns(item):
    column_map = {
    }
    hidden = ['location']
    return sdk_utils.get_osc_show_columns_for_sdk_resource(item, column_map,
                                                           hidden)


class CreateDatasetImportTask(command.ShowOne):
    _description = _('Create a ModelArts dataset import task')

    def get_parser(self, prog_name):
        parser = super(CreateDatasetImportTask, self).get_parser(prog_name)
        parser.add_argument(
            '--dataset_id',
            metavar='<dataset_id>',
            required=True,
            help=_('Dataset ID.')
        )
        parser.add_argument(
            '--import_path',
            metavar='<import_path>',
            required=True,
            help=_('OBS path to which the data is imported. When importing '
                   'a manifest file, ensure that the path is accurate to '
                   'the manifest file.')
        )
        parser.add_argument(
            '--import_annotations',
            metavar='<import_annotations>',
            help=_('Whether to import labels. Default value: true')
        )
        parser.add_argument(
            '--import-type',
            metavar='<import_type>',
            help=_('Import mode. The default value is dir.'
                   '\ndir: Import the directory.'
                   '\nmanifest: Import the manifest file.')
        )
        parser.add_argument(
            '--import-folder',
            metavar='<import_folder>',
            help=_('Name of the subdirectory in the dataset storage '
                   'directory after import.')
        )
        parser.add_argument(
            '--final-annotation',
            metavar='<final_annotation>',
            help=_('Whether to directly import to the final result. '
                   'The default value is true.')
        )
        parser.add_argument(
            '--difficult-only',
            metavar='<difficult_only>',
            help=_('Whether to import only hard examples. '
                   'Default value: false.')
        )
        parser.add_argument(
            '--included-labels',
            metavar='<included_labels>',
            help=_('Whether to import only the labels specified by this '
                   'parameter.')
        )
        parser.add_argument(
            '--included-tags',
            metavar='<included_tags>',
            help=_('Whether to import only the labels corresponding to '
                   'the value.')
        )
        # Same parameter in Label, LabelAttribute. Must review!
        parser.add_argument(
            '--name',
            metavar='<name>',
            help=_('Label name ')
        )
        # Same parameter in Label, LabelAttribute. Must review!
        parser.add_argument(
            '--type',
            metavar='<type>',
            help=_('Label type. A triplet dataset can contain the following '
                   'types of labels:'
                   '\n101: text entity'
                   '\n102: triplet relationship')
        )
        # Same parameter in Label, must review!
        parser.add_argument(
            '--property',
            metavar='<property>',
            help=_('For details about the mandatory attributes of a '
                   'triplet label.')
        )
        # Path Parameters
        parser.add_argument(
            '--project_id',
            metavar='<project_id>',
            help=_('Project ID.')
        )
        # Request body parameters
        parser.add_argument(
            '--annotation_format',
            metavar='<annotation_format>',
            help=_('Format of the labeling information. Currently, only object '
                   'detection is supported. The options are as follows:'
                   '\nVOC: VOC'
                   '\nCOCO: COCO')
        )
        parser.add_argument(
            '--data_source',
            metavar='<data_source>',
            help=_('Data source.')
        )
        parser.add_argument(
            '--excluded_labels',
            metavar='<excluded_labels>',
            help=_('Do not import samples containing the specified label.')
        )
        parser.add_argument(
            '--import_origin',
            metavar='<import_origin>',
            help=_('Data source. The options are as follows:'
                   '\nobs: OBS bucket (default value)'
                   '\ndws: GaussDB(DWS)'
                   '\ndli: DLI'
                   '\nrds: RDS'
                   '\nmrs: MRS'
                   '\ninference: Inference service')
        )
        parser.add_argument(
            '--import_samples',
            metavar='<import_samples>',
            help=_('Whether to import samples. The options are as follows:'
                   '\ntrue: Import samples. (Default value)'
                   '\nfalse: Do not import samples.')
        )
        parser.add_argument(
            '--label_format',
            metavar='<label_format>',
            help=_('Label format. This parameter is used only for text datasets.')
        )
        # Same paramater in DataSource, must rewiew!
        parser.add_argument(
            '--with_column_header',
            metavar='<with_column_header>',
            help=_('Whether the first row in the file is a column name. This field is '
                   'valid for the table dataset. The options are as follows:'
                   '\ntrue: The first row in the file is the column name.'
                   '\nfalse: The first row in the file is not the column name. (Default value)')
        )
        # DataSource
        parser.add_argument(
            '--data_path',
            metavar='<data_path>',
            help=_('Data source path.')
        )
        parser.add_argument(
            '--data_type',
            metavar='<data_type>',
            help=_('Data type. The options are as follows:'
                   '\n0: OBS bucket (default value)'
                   '\n1: GaussDB(DWS)'
                   '\n2: DLI'
                   '\n3: RDS'
                   '\n4: MRS'
                   '\n5: AI Gallery'
                   '\n6: Inference service')
        )
        parser.add_argument(
            '--schema_maps',
            metavar='<schema_maps>',
            help=_('Schema mapping information corresponding to the table '
                   'data.')
        )
        parser.add_argument(
            '--source_info',
            metavar='<source_info>',
            help=_('nformation required for importing a table data source.')
        )
        # SchemaMap
        parser.add_argument(
            '--dest_name',
            metavar='<dest_name>',
            help=_('Name of the destination column.')
        )
        parser.add_argument(
            '--src_name',
            metavar='<src_name>',
            help=_('Name of the source column.')
        )
        # SourceInfo
        parser.add_argument(
            '--cluster_id',
            metavar='<cluster_id>',
            help=_('ID of an MRS cluster.')
        )
        parser.add_argument(
            '--cluster_mode',
            metavar='<cluster_mode>',
            help=_('Running mode of an MRS cluster. The options are as follows:'
                   '\n0: normal cluster'
                   '\n1: security cluster')
        )
        parser.add_argument(
            '--cluster_name',
            metavar='<cluster_name>',
            help=_('Name of an MRS cluster.')
        )
        parser.add_argument(
            '--database_name',
            metavar='<database_name>',
            help=_('Name of the database to which the table dataset is imported.')
        )
        parser.add_argument(
            '--input',
            metavar='<input>',
            help=_('HDFS path of a table dataset.')
        )
        parser.add_argument(
            '--ip',
            metavar='<ip>',
            help=_('IP address of your GaussDB(DWS) cluster.')
        )
        parser.add_argument(
            '--port',
            metavar='<port>',
            help=_('Port number of your GaussDB(DWS) cluster.')
        )
        parser.add_argument(
            '--queue_name',
            metavar='<queue_name>',
            help=_('DLI queue name of a table dataset.')
        )
        parser.add_argument(
            '--subnet_id',
            metavar='<subnet_id>',
            help=_('Subnet ID of an MRS cluster.')
        )
        parser.add_argument(
            '--table_name',
            metavar='<table_name>',
            help=_('Name of the table to which a table dataset is imported.')
        )
        parser.add_argument(
            '--user_name',
            metavar='<user_name>',
            help=_('Username, which is mandatory for GaussDB(DWS) data.')
        )
        parser.add_argument(
            '--user_password',
            metavar='<user_password>',
            help=_('User password, which is mandatory for GaussDB(DWS) data.')
        )
        parser.add_argument(
            '--vpc_id',
            metavar='<vpc_id>',
            help=_('ID of the VPC where an MRS cluster resides.')
        )
        # Label
        parser.add_argument(
            '--attributes',
            metavar='<attributes>',
            help=_('Multi-dimensional attribute of a label. For example, if the label is '
                   'music, attributes such as style and artist may be included.')
        )
        # LabelAttribute
        parser.add_argument(
            '--default_value',
            metavar='<default_value>',
            help=_('Default value of a label attribute.')
        )
        # Same parameter in LabelAttributeValue, must review!
        parser.add_argument(
            '--id',
            metavar='<id>',
            help=_('Label attribute ID.')
        )
        parser.add_argument(
            '--values',
            metavar='<values>',
            help=_('List of label attribute values.')
        )
        # LabelAttributeValue
        parser.add_argument(
            '--value',
            metavar='<value>',
            help=_('Label attribute value.')
        )
        # LabelProperty
        parser.add_argument(
            '--modelarts_color',
            metavar='<modelarts_color>',
            help=_('Default attribute: Label color, which is a hexadecimal code of the '
                   'color. By default, this parameter is left blank. Example: #FFFFF0.')
        )
        parser.add_argument(
            '--modelarts_default_shape',
            metavar='<modelarts_default_shape>',
            help=_('Default attribute: Default shape of an object detection label '
                   '(dedicated attribute). By default, this parameter is left blank. The '
                   'options are as follows:'
                   '\nbndbox: rectangle'
                   '\npolygon: polygon'
                   '\ncircle: circle'
                   '\nline: straight line'
                   '\ndashed: dotted line'
                   '\npoint: point'
                   '\npolyline: polyline')
        )
        parser.add_argument(
            '--modelarts_from_type',
            metavar='<modelarts_from_type>',
            help=_('Default attribute: Type of the head entity in the triplet relationship '
                   'label. This attribute must be specified when a relationship label is '
                   'created. This parameter is used only for the text triplet dataset.')
        )
        parser.add_argument(
            '--modelarts_rename_to',
            metavar='<modelarts_rename_to>',
            help=_('Default attribute: The new name of the label.')
        )
        parser.add_argument(
            '--modelarts_shortcut',
            metavar='<modelarts_shortcut>',
            help=_('Default attribute: Label shortcut key. By default, this parameter is '
                   'left blank. For example: D.')
        )
        parser.add_argument(
            '--modelarts_to_type',
            metavar='<modelarts_to_type>',
            help=_('Default attribute: Type of the tail entity in the triplet relationship '
                   'label. This attribute must be specified when a relationship label is '
                   'created. This parameter is used only for the text triplet dataset.')
        )
        # LabelFormat
        parser.add_argument(
            '--label_type',
            metavar='<label_type>',
            help=_('Label type of text classification. The options are as follows:'
                   '\n0: The label is separated from the text, and they are distinguished '
                   'by the fixed suffix _result. For example, the text file is abc.txt, and '
                   'the label file is abc_result.txt.'
                   '\n1: Default value. Labels and texts are stored in the same file and '
                   'separated by separators. You can use text_sample_separator to '
                   'specify the separator between the text and label and '
                   'text_label_separator to specify the separator between labels.')
        )
        parser.add_argument(
            '--text_label_separator',
            metavar='<text_label_separator>',
            help=_('Separator between labels. By default, a comma (,) is used as the '
                   'separator. The separator needs to be escaped. The separator can '
                   'contain only one character, such as a letter, a digit, or any of the '
                   "following special characters: !@#$%^&*_=|?/':.;,")
        )
        parser.add_argument(
            '--text_sample_separator',
            metavar='<text_sample_separator>',
            help=_('Separator between the text and label. By default, the Tab key is used as '
                   'the separator. The separator needs to be escaped. The separator can '
                   'contain only one character, such as a letter, a digit, or any of the '
                   "following special characters: !@#$%^&*_=|?/':.;,")
        )
        # Response body parameters
        parser.add_argument(
            '--task_id',
            metavar='<task_id>',
            help=_('ID of an import task.')
        )
        return parser

    def take_action(self, parsed_args):

        client = self.app.client_manager.modelarts

        attrs = {}

        if parsed_args.dataset_id:
            attrs['dataset_id'] = parsed_args.dataset_id
        if parsed_args.import_path:
            attrs['import_path'] = parsed_args.import_path
        if parsed_args.import_annotations:
            attrs['import_annotations'] = parsed_args.import_annotations
        if parsed_args.import_type:
            attrs['import_type'] = parsed_args.import_type
        if parsed_args.import_folder:
            attrs['import_folder'] = parsed_args.import_folder
        if parsed_args.final_annotation:
            attrs['final_annotation'] = parsed_args.final_annotation
        if parsed_args.import_annotations:
            attrs['import_annotations'] = parsed_args.import_annotations
        if parsed_args.difficult_only:
            attrs['difficult_only'] = parsed_args.difficult_only
        if parsed_args.included_labels:
            attrs['included_labels'] = parsed_args.included_labels
        if parsed_args.included_tags:
            attrs['included_tags'] = parsed_args.included_tags
        if parsed_args.name:
            attrs['name'] = parsed_args.name
        if parsed_args.type:
            attrs['type'] = parsed_args.type
        if parsed_args.property:
            attrs['property'] = parsed_args.property

        if parsed_args.project_id:
            attrs['project_id'] = parsed_args.project_id
        if parsed_args.annotation_format:
            attrs['annotation_format'] = parsed_args.annotation_format
        if parsed_args.data_source:
            attrs['data_source'] = parsed_args.data_source
        if parsed_args.excluded_labels:
            attrs['excluded_labels'] = parsed_args.excluded_labels
        if parsed_args.import_origin:
            attrs['import_origin'] = parsed_args.import_origin
        if parsed_args.import_samples:
            attrs['import_samples'] = parsed_args.import_samples
        if parsed_args.label_format:
            attrs['label_format'] = parsed_args.label_format
        if parsed_args.with_column_header:
            attrs['with_column_header'] = parsed_args.with_column_header
        if parsed_args.data_path:
            attrs['data_path'] = parsed_args.data_path
        if parsed_args.data_type:
            attrs['data_type'] = parsed_args.data_type
        if parsed_args.schema_maps:
            attrs['schema_maps'] = parsed_args.schema_maps
        if parsed_args.source_info:
            attrs['source_info'] = parsed_args.source_info
        if parsed_args.dest_name:
            attrs['dest_name'] = parsed_args.dest_name
        if parsed_args.src_name:
            attrs['src_name'] = parsed_args.src_name
        if parsed_args.cluster_id:
            attrs['cluster_id'] = parsed_args.cluster_id
        if parsed_args.cluster_mode:
            attrs['cluster_mode'] = parsed_args.cluster_mode
        if parsed_args.cluster_name:
            attrs['cluster_name'] = parsed_args.cluster_name
        if parsed_args.database_name:
            attrs['database_name'] = parsed_args.database_name
        if parsed_args.input:
            attrs['input'] = parsed_args.input
        if parsed_args.ip:
            attrs['ip'] = parsed_args.ip
        if parsed_args.port:
            attrs['port'] = parsed_args.port
        if parsed_args.queue_name:
            attrs['queue_name'] = parsed_args.queue_name
        if parsed_args.subnet_id:
            attrs['subnet_id'] = parsed_args.subnet_id
        if parsed_args.table_name:
            attrs['table_name'] = parsed_args.table_name
        if parsed_args.user_name:
            attrs['user_name'] = parsed_args.user_name
        if parsed_args.user_password:
            attrs['user_password'] = parsed_args.user_password
        if parsed_args.vpc_id:
            attrs['vpc_id'] = parsed_args.vpc_id
        if parsed_args.attributes:
            attrs['attributes'] = parsed_args.attributes
        if parsed_args.default_value:
            attrs['default_value'] = parsed_args.default_value
        if parsed_args.id:
            attrs['id'] = parsed_args.id
        if parsed_args.values:
            attrs['values'] = parsed_args.values
        if parsed_args.value:
            attrs['value'] = parsed_args.value
        if parsed_args.modelarts_color:
            attrs['modelarts_color'] = parsed_args.modelarts_color
        if parsed_args.modelarts_default_shape:
            attrs['modelarts_default_shape'] = parsed_args.modelarts_default_shape
        if parsed_args.modelarts_from_type:
            attrs['modelarts_from_type'] = parsed_args.modelarts_from_type
        if parsed_args.modelarts_rename_to:
            attrs['modelarts_rename_to'] = parsed_args.modelarts_rename_to
        if parsed_args.modelarts_shortcut:
            attrs['modelarts_shortcut'] = parsed_args.modelarts_shortcut
        if parsed_args.modelarts_to_type:
            attrs['modelarts_to_type'] = parsed_args.modelarts_to_type
        if parsed_args.label_type:
            attrs['label_type'] = parsed_args.label_type
        if parsed_args.text_label_separator:
            attrs['text_label_separator'] = parsed_args.text_label_separator
        if parsed_args.text_sample_separator:
            attrs['text_sample_separator'] = parsed_args.text_sample_separator
        if parsed_args.task_id:
            attrs['task_id'] = parsed_args.task_id

        obj = client.create_dataset_import_task(**attrs)

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns)

        return (display_columns, data)


class ShowDatasetImportTask(command.ShowOne):
    _description = _('Show details of a MA dataset import task')

    def get_parser(self, prog_name):
        parser = super(ShowDatasetImportTask, self).get_parser(prog_name)

        # Same parameter in Response body parameters, must review!
        parser.add_argument(
            '--dataset_id',
            metavar='<dataset_id>',
            required=True,
            help=_('Enter dataset id')
        )
        # Same parameter in Response body parameters, must review!
        parser.add_argument(
            '--task_id',
            metavar='<task_id>',
            required=True,
            help=_('Enter task id')
        )
        #Path Parameters
        parser.add_argument(
            '--project_id',
            metavar='<project_id>',
            help=_('Enter project ID.')
        )
        #Response body parameters
        parser.add_argument(
            '--annotated_sample_count',
            metavar='<annotated_sample_count>',
            help=_('Number of labeled samples.')
        )
        parser.add_argument(
            '--create_time',
            metavar='<create_time>',
            help=_('Time when a task is created.')
        )
        parser.add_argument(
            '--data_source',
            metavar='<data_source>',
            help=_('Data source.')
        )
        parser.add_argument(
            '--elapsed_time',
            metavar='<elapsed_time>',
            help=_('Task running time, in seconds.')
        )
        parser.add_argument(
            '--error_code',
            metavar='<error_code>',
            help=_('Error code.')
        )
        parser.add_argument(
            '--error_msg',
            metavar='<error_msg>',
            help=_('Error message.')
        )
        parser.add_argument(
            '--file_statistics',
            metavar='<file_statistics>',
            help=_('Progress of file copy.')
        )
        parser.add_argument(
            '--finished_file_count',
            metavar='<finished_file_count>',
            help=_('Number of files that have been transferred.')
        )
        parser.add_argument(
            '--finished_file_size',
            metavar='<finished_file_size>',
            help=_('Size of the file that has been transferred, in bytes.')
        )
        parser.add_argument(
            '--import_path',
            metavar='<import_path>',
            help=_('OBS path or manifest path to be imported.'
                   '\nWhen importing a manifest file, ensure that the path is '
                   'accurate to the manifest file.'
                   '\nWhen a path is imported as a directory, the dataset type can '
                   'only support image classification, object detection, text '
                   'classification, or sound classification.')
        )
        parser.add_argument(
            '--import_type',
            metavar='<import_type>',
            help=_('Import mode. The options are as follows:'
                   '\n0: Import by directory.'
                   '\n1: Import by manifest file.')
        )
        parser.add_argument(
            '--imported_sample_count',
            metavar='<imported_sample_count>',
            help=_('Number of imported samples.')
        )
        parser.add_argument(
            '--imported_sub_sample_count',
            metavar='<imported_sub_sample_count>',
            help=_('Number of imported subsamples.')
        )
        parser.add_argument(
            '--processor_task_id',
            metavar='<processor_task_id>',
            help=_('ID of a preprocessing task.')
        )
        parser.add_argument(
            '--processor_task_status',
            metavar='<processor_task_status>',
            help=_('Status of a preprocessing task.')
        )
        parser.add_argument(
            '--status',
            metavar='<status>',
            help=_('Status of an import task. The options are as follows:'
                   '\nQUEUING: queuing'
                   '\nSTARTING: execution started'
                   '\nRUNNING: running'
                   '\nCOMPLETED: completed'
                   '\nFAILED: failed'
                   '\nNOT_EXIST: not found')
        )
        parser.add_argument(
            '--total_file_count',
            metavar='<total_file_count>',
            help=_('Total number of files.')
        )
        parser.add_argument(
            '--total_file_size',
            metavar='<total_file_size>',
            help=_('Total file size, in bytes.')
        )
        parser.add_argument(
            '--total_sample_count',
            metavar='<total_sample_count>',
            help=_('Total number of samples.')
        )
        parser.add_argument(
            '--total_sub_sample_count',
            metavar='<total_sub_sample_count>',
            help=_('Total number of subsamples generated from the parent samples.')
        )
        parser.add_argument(
            '--unconfirmed_sample_count',
            metavar='<unconfirmed_sample_count>',
            help=_('Number of samples to be confirmed.')
        )
        parser.add_argument(
            '--update_ms',
            metavar='<update_ms>',
            help=_('Time when a task is updated.')
        )
        # DataSource
        parser.add_argument(
            '--data_path',
            metavar='<data_path>',
            help=_('Data source path.')
        )
        parser.add_argument(
            '--data_type',
            metavar='<data_type>',
            help=_('Data type. The options are as follows:'
                   '\n0: OBS bucket (default value)'
                   '\n1: GaussDB(DWS)'
                   '\n2: DLI'
                   '\n3: RDS'
                   '\n4: MRS'
                   '\n5: AI Gallery'
                   '\n6: Inference service')
        )
        parser.add_argument(
            '--schema_maps',
            metavar='<schema_maps>',
            help=_('Schema mapping information corresponding to the table data.')
        )
        parser.add_argument(
            '--source_info',
            metavar='<source_info>',
            help=_('Information required for importing a table data source.')
        )
        parser.add_argument(
            '--with_column_header',
            metavar='<with_column_header>',
            help=_('Whether the first row in the file is a column name. This field is valid for '
                   'the table dataset. The options are as follows:'
                   '\ntrue: The first row in the file is the column name.'
                   '\nfalse: The first row in the file is not the column name.')
        )
        # SchemaMap
        parser.add_argument(
            '--dest_name',
            metavar='<dest_name>',
            help=_('Name of the destination column.')
        )
        parser.add_argument(
            '--src_name',
            metavar='<src_name>',
            help=_('Name of the source column.')
        )
        # SourceInfo
        parser.add_argument(
            '--cluster_id',
            metavar='<cluster_id>',
            help=_('ID of an MRS cluster.')
        )
        parser.add_argument(
            '--cluster_mode',
            metavar='<cluster_mode>',
            help=_('Running mode of an MRS cluster. The options are as follows:'
                   '\n0: normal cluster'
                   '\n1: security cluster')
        )
        parser.add_argument(
            '--cluster_name',
            metavar='<cluster_name>',
            help=_('Name of an MRS cluster.')
        )
        parser.add_argument(
            '--database_name',
            metavar='<database_name>',
            help=_('Name of the database to which the table dataset is imported.')
        )
        parser.add_argument(
            '--input',
            metavar='<input>',
            help=_('HDFS path of a table dataset.')
        )
        parser.add_argument(
            '--ip',
            metavar='<ip>',
            help=_('IP address of your GaussDB(DWS) cluster.')
        )
        parser.add_argument(
            '--port',
            metavar='<port>',
            help=_('Port number of your GaussDB(DWS) cluster.')
        )
        parser.add_argument(
            '--queue_name',
            metavar='<queue_name>',
            help=_('DLI queue name of a table dataset.')
        )
        parser.add_argument(
            '--subnet_id',
            metavar='<subnet_id>',
            help=_('Subnet ID of an MRS cluster.')
        )
        parser.add_argument(
            '--table_name',
            metavar='<table_name>',
            help=_('Name of the table to which a table dataset is imported.')
        )
        parser.add_argument(
            '--user_name',
            metavar='<user_name>',
            help=_('Username, which is mandatory for GaussDB(DWS) data.')
        )
        parser.add_argument(
            '--user_password',
            metavar='<user_password>',
            help=_('User password, which is mandatory for GaussDB(DWS) data.')
        )
        parser.add_argument(
            '--vpc_id',
            metavar='<vpc_id>',
            help=_('ID of the VPC where an MRS cluster resides.')
        )
        # FileCopyProgress
        parser.add_argument(
            '--file_num_finished',
            metavar='<file_num_finished>',
            help=_('Number of files that have been transferred.')
        )
        parser.add_argument(
            '--file_num_total',
            metavar='<file_num_total>',
            help=_('Total number of files.')
        )
        parser.add_argument(
            '--file_size_finished',
            metavar='<file_size_finished>',
            help=_('Size of the file that has been transferred, in bytes.')
        )
        parser.add_argument(
            '--file_size_total',
            metavar='<file_size_total>',
            help=_('Total file size, in bytes.')
        )

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.modelarts
        query = {}

        if parsed_args.dataset_id:
            query['dataset_id'] = parsed_args.dataset_id

        if parsed_args.task_id:
            query['task_id'] = parsed_args.task_id

        if parsed_args.project_id:
            query['project_id'] = parsed_args.project_id
        if parsed_args.annotated_sample_count:
            query['annotated_sample_count'] = parsed_args.annotated_sample_count
        if parsed_args.create_time:
            query['create_time'] = parsed_args.create_time
        if parsed_args.data_source:
            query['data_source'] = parsed_args.data_source
        if parsed_args.elapsed_time:
            query['elapsed_time'] = parsed_args.elapsed_time
        if parsed_args.error_code:
            query['error_code'] = parsed_args.error_code
        if parsed_args.error_msg:
            query['error_msg'] = parsed_args.error_msg
        if parsed_args.file_statistics:
            query['file_statistics'] = parsed_args.file_statistics
        if parsed_args.finished_file_count:
            query['finished_file_count'] = parsed_args.finished_file_count
        if parsed_args.finished_file_size:
            query['finished_file_size'] = parsed_args.finished_file_size
        if parsed_args.import_path:
            query['import_path'] = parsed_args.import_path
        if parsed_args.import_type:
            query['import_type'] = parsed_args.import_type
        if parsed_args.imported_sample_count:
            query['imported_sample_count'] = parsed_args.imported_sample_count
        if parsed_args.imported_sub_sample_count:
            query['imported_sub_sample_count'] = parsed_args.imported_sub_sample_count
        if parsed_args.processor_task_id:
            query['processor_task_id'] = parsed_args.processor_task_id
        if parsed_args.processor_task_status:
            query['processor_task_status'] = parsed_args.processor_task_status
        if parsed_args.status:
            query['status'] = parsed_args.status
        if parsed_args.total_file_count:
            query['total_file_count'] = parsed_args.total_file_count
        if parsed_args.total_file_size:
            query['total_file_size'] = parsed_args.total_file_size
        if parsed_args.total_sample_count:
            query['total_sample_count'] = parsed_args.total_sample_count
        if parsed_args.total_sub_sample_count:
            query['total_sub_sample_count'] = parsed_args.total_sub_sample_count
        if parsed_args.unconfirmed_sample_count:
            query['unconfirmed_sample_count'] = parsed_args.unconfirmed_sample_count
        if parsed_args.update_ms:
            query['update_ms'] = parsed_args.update_ms
        if parsed_args.data_path:
            query['data_path'] = parsed_args.data_path
        if parsed_args.data_type:
            query['data_type'] = parsed_args.data_type
        if parsed_args.schema_maps:
            query['schema_maps'] = parsed_args.schema_maps
        if parsed_args.source_info:
            query['source_info'] = parsed_args.source_info
        if parsed_args.with_column_header:
            query['with_column_header'] = parsed_args.with_column_header
        if parsed_args.dest_name:
            query['dest_name'] = parsed_args.dest_name
        if parsed_args.src_name:
            query['src_name'] = parsed_args.src_name
        if parsed_args.cluster_id:
            query['cluster_id'] = parsed_args.cluster_id
        if parsed_args.cluster_mode:
            query['cluster_mode'] = parsed_args.cluster_mode
        if parsed_args.cluster_name:
            query['cluster_name'] = parsed_args.cluster_name
        if parsed_args.database_name:
            query['database_name'] = parsed_args.database_name
        if parsed_args.input:
            query['input'] = parsed_args.input
        if parsed_args.ip:
            query['ip'] = parsed_args.ip
        if parsed_args.port:
            query['port'] = parsed_args.port
        if parsed_args.queue_name:
            query['queue_name'] = parsed_args.queue_name
        if parsed_args.subnet_id:
            query['subnet_id'] = parsed_args.subnet_id
        if parsed_args.table_name:
            query['table_name'] = parsed_args.table_name
        if parsed_args.user_name:
            query['user_name'] = parsed_args.user_name
        if parsed_args.user_password:
            query['user_password'] = parsed_args.user_password
        if parsed_args.vpc_id:
            query['vpc_id'] = parsed_args.vpc_id
        if parsed_args.file_num_finished:
            query['file_num_finished'] = parsed_args.file_num_finished
        if parsed_args.file_num_total:
            query['file_num_total'] = parsed_args.file_num_total
        if parsed_args.file_size_finished:
            query['file_size_finished'] = parsed_args.file_size_finished
        if parsed_args.file_size_total:
            query['file_size_total'] = parsed_args.file_size_total

        obj = client.show_dataset_import_task(**query)
        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns)

        return (display_columns, data)


class ListDatasetImportTasks(command.Lister):
    _description = _('Get properties of a vm')
    columns = (
        'task_id',
        'dataset_id',
        'import_path'
    )

    table_columns = (
        'task_id',
        'dataset_id',
        'import_path'
    )

    def get_parser(self, prog_name):
        parser = super(ListDatasetImportTasks, self).get_parser(prog_name)
        parser.add_argument(
            '--dataset_id',
            metavar='<dataset_id>',
            required=True,
            help=_('Name of the dataset to delete.')
        )
        # Path Parameters
        parser.add_argument(
            '--project_id',
            metavar='<project_id>',
            help=_('Project ID.')
            )
        # Query Parameters
        parser.add_argument(
            '--limit',
            metavar='<limit>',
            help=_('Maximum number of records returned on each page. The value ranges from 1 to '
                   '100. The default value is 10.')
        )
        parser.add_argument(
            '--offset',
            metavar='<offset>',
            help=_('Start page of the paging list. The default value is 0.')
        )
        # Response body parameters
        parser.add_argument(
            '--import_tasks',
            metavar='<import_tasks>',
            help=_('List of import tasks.')
        )
        parser.add_argument(
            '--total_count',
            metavar='<total_count>',
            help=_('Number of import tasks.')
        )
        # ImportTaskStatusResp
        parser.add_argument(
            '--annotated_sample_count',
            metavar='<annotated_sample_count>',
            help=_('Number of labeled samples.')
        )
        parser.add_argument(
            '--create_time',
            metavar='<create_time>',
            help=_('Time when a task is created.')
        )
        parser.add_argument(
            '--data_source',
            metavar='<data_source>',
            help=_('Data source.')
        )
        parser.add_argument(
            '--elapsed_time',
            metavar='<elapsed_time>',
            help=_('Task running time, in seconds.')
        )
        parser.add_argument(
            '--error_code',
            metavar='<error_code>',
            help=_('Error code.')
        )
        parser.add_argument(
            '--error_msg',
            metavar='<error_msg>',
            help=_('Error message.')
        )
        parser.add_argument(
            '--file_statistics',
            metavar='<file_statistics>',
            help=_('Progress of file copy.')
        )
        parser.add_argument(
            '--finished_file_count',
            metavar='<finished_file_count>',
            help=_('Number of files that have been transferred.')
        )
        parser.add_argument(
            '--finished_file_size',
            metavar='<finished_file_size>',
            help=_('Size of the file that has been transferred, in bytes.')
        )
        parser.add_argument(
            '--import_path',
            metavar='<import_path>',
            help=_('OBS path or manifest path to be imported.'
                   '\nWhen importing a manifest file, ensure that the path is '
                   'accurate to the manifest file.'
                   '\nWhen a path is imported as a directory, the dataset type can '
                   'only support image classification, object detection, text '
                   'classification, or sound classification.')
        )
        parser.add_argument(
            '--import_type',
            metavar='<import_type>',
            help=_('Import mode. The options are as follows:'
                   '\n0: Import by directory.'
                   '\n1: Import by manifest file.')
        )
        parser.add_argument(
            '--imported_sample_count',
            metavar='<imported_sample_count>',
            help=_('Number of imported samples.')
        )
        parser.add_argument(
            '--imported_sub_sample_count',
            metavar='<imported_sub_sample_count>',
            help=_('Number of imported subsamples.')
        )
        parser.add_argument(
            '--processor_task_id',
            metavar='<processor_task_id>',
            help=_('ID of a preprocessing task.')
        )
        parser.add_argument(
            '--processor_task_status',
            metavar='<processor_task_status>',
            help=_('Status of a preprocessing task.')
        )
        parser.add_argument(
            '--status',
            metavar='<status>',
            help=_('Status of an import task. The options are as follows:'
                   '\nQUEUING: queuing'
                   '\nSTARTING: execution started'
                   '\nRUNNING: running'
                   '\nCOMPLETED: completed'
                   '\nFAILED: failed'
                   '\nNOT_EXIST: not found')
        )
        parser.add_argument(
            '--task_id',
            metavar='<task_id>',
            help=_('Task ID.')
        )
        parser.add_argument(
            '--total_file_count',
            metavar='<total_file_count>',
            help=_('Total number of files.')
        )
        parser.add_argument(
            '--total_file_size',
            metavar='<total_file_size>',
            help=_('Total file size, in bytes.')
        )
        parser.add_argument(
            '--total_sample_count',
            metavar='<total_sample_count>',
            help=_('Total number of samples.')
        )
        parser.add_argument(
            '--total_sub_sample_count',
            metavar='<total_sub_sample_count>',
            help=_('Total number of subsamples generated from the parent samples.')
        )
        parser.add_argument(
            '--unconfirmed_sample_count',
            metavar='<unconfirmed_sample_count>',
            help=_('Number of samples to be confirmed.')
        )
        parser.add_argument(
            '--update_ms',
            metavar='<update_ms>',
            help=_('Time when a task is updated.')
        )
        # DataSource
        parser.add_argument(
            '--data_path',
            metavar='<data_path>',
            help=_('Data source path.')
        )
        parser.add_argument(
            '--data_type',
            metavar='<data_type>',
            help=_('Data type. The options are as follows:'
                   '\n0: OBS bucket (default value)'
                   '\n1: GaussDB(DWS)'
                   '\n2: DLI'
                   '\n3: RDS'
                   '\n4: MRS'
                   '\n5: AI Gallery'
                   '\n6: Inference service')
        )
        parser.add_argument(
            '--schema_maps',
            metavar='<schema_maps>',
            help=_('Schema mapping information corresponding to the table data.')
        )
        parser.add_argument(
            '--source_info',
            metavar='<source_info>',
            help=_('Information required for importing a table data source.')
        )
        parser.add_argument(
            '--with_column_header',
            metavar='<with_column_header>',
            help=_('Whether the first row in the file is a column name. This field is valid for '
                   'the table dataset. The options are as follows:'
                   '\ntrue: The first row in the file is the column name.'
                   '\nfalse: The first row in the file is not the column name.')
        )
        # SchemaMap
        parser.add_argument(
            '--dest_name',
            metavar='<dest_name>',
            help=_('Name of the destination column.')
        )
        parser.add_argument(
            '--src_name',
            metavar='<src_name>',
            help=_('Name of the source column.')
        )
        # SourceInfo
        parser.add_argument(
            '--cluster_id',
            metavar='<cluster_id>',
            help=_('ID of an MRS cluster.')
        )
        parser.add_argument(
            '--cluster_mode',
            metavar='<cluster_mode>',
            help=_('Running mode of an MRS cluster. The options are as follows:'
                   '\n0: normal cluster'
                   '\n1: security cluster')
        )
        parser.add_argument(
            '--cluster_name',
            metavar='<cluster_name>',
            help=_('Name of an MRS cluster.')
        )
        parser.add_argument(
            '--database_name',
            metavar='<database_name>',
            help=_('Name of the database to which the table dataset is imported.')
        )
        parser.add_argument(
            '--input',
            metavar='<input>',
            help=_('HDFS path of a table dataset.')
        )
        parser.add_argument(
            '--ip',
            metavar='<ip>',
            help=_('IP address of your GaussDB(DWS) cluster.')
        )
        parser.add_argument(
            '--port',
            metavar='<port>',
            help=_('Port number of your GaussDB(DWS) cluster.')
        )
        parser.add_argument(
            '--queue_name',
            metavar='<queue_name>',
            help=_('DLI queue name of a table dataset.')
        )
        parser.add_argument(
            '--subnet_id',
            metavar='<subnet_id>',
            help=_('Subnet ID of an MRS cluster.')
        )
        parser.add_argument(
            '--table_name',
            metavar='<table_name>',
            help=_('Name of the table to which a table dataset is imported.')
        )
        parser.add_argument(
            '--user_name',
            metavar='<user_name>',
            help=_('Username, which is mandatory for GaussDB(DWS) data.')
        )
        parser.add_argument(
            '--user_password',
            metavar='<user_password>',
            help=_('User password, which is mandatory for GaussDB(DWS) data.')
        )
        parser.add_argument(
            '--vpc_id',
            metavar='<vpc_id>',
            help=_('ID of the VPC where an MRS cluster resides.')
        )
        # FileCopyProgress
        parser.add_argument(
            '--file_num_finished',
            metavar='<file_num_finished>',
            help=_('Number of files that have been transferred.')
        )
        parser.add_argument(
            '--file_num_total',
            metavar='<file_num_total>',
            help=_('Total number of files.')
        )
        parser.add_argument(
            '--file_size_finished',
            metavar='<file_size_finished>',
            help=_('Size of the file that has been transferred, in bytes.')
        )
        parser.add_argument(
            '--file_size_total',
            metavar='<file_size_total>',
            help=_('Total file size, in bytes.')
        )

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.modelarts

        query = {}
        if parsed_args.dataset_id:
            query['dataset_id'] = parsed_args.dataset_id

        if parsed_args.project_id:
            query['project_id'] = parsed_args.project_id
        if parsed_args.limit:
            query['limit'] = parsed_args.limit
        if parsed_args.offset:
            query['offset'] = parsed_args.offset
        if parsed_args.import_tasks:
            query['import_tasks'] = parsed_args.import_tasks
        if parsed_args.total_count:
            query['total_count'] = parsed_args.total_count
        if parsed_args.annotated_sample_count:
            query['annotated_sample_count'] = parsed_args.annotated_sample_count
        if parsed_args.create_time:
            query['create_time'] = parsed_args.create_time
        if parsed_args.data_source:
            query['data_source'] = parsed_args.data_source
        if parsed_args.dataset_id:
            query['dataset_id'] = parsed_args.dataset_id
        if parsed_args.elapsed_time:
            query['elapsed_time'] = parsed_args.elapsed_time
        if parsed_args.error_code:
            query['error_code'] = parsed_args.error_code
        if parsed_args.error_msg:
            query['error_msg'] = parsed_args.error_msg
        if parsed_args.file_statistics:
            query['file_statistics'] = parsed_args.file_statistics
        if parsed_args.finished_file_count:
            query['finished_file_count'] = parsed_args.finished_file_count
        if parsed_args.finished_file_size:
            query['finished_file_size'] = parsed_args.finished_file_size
        if parsed_args.import_path:
            query['import_path'] = parsed_args.import_path
        if parsed_args.import_type:
            query['import_type'] = parsed_args.import_type
        if parsed_args.imported_sample_count:
            query['imported_sample_count'] = parsed_args.imported_sample_count
        if parsed_args.imported_sub_sample_count:
            query['imported_sub_sample_count'] = parsed_args.imported_sub_sample_count
        if parsed_args.processor_task_id:
            query['processor_task_id'] = parsed_args.processor_task_id
        if parsed_args.processor_task_status:
            query['processor_task_status'] = parsed_args.processor_task_status
        if parsed_args.status:
            query['status'] = parsed_args.status
        if parsed_args.task_id:
            query['task_id'] = parsed_args.task_id
        if parsed_args.total_file_count:
            query['total_file_count'] = parsed_args.total_file_count
        if parsed_args.total_file_size:
            query['total_file_size'] = parsed_args.total_file_size
        if parsed_args.total_sample_count:
            query['total_sample_count'] = parsed_args.total_sample_count
        if parsed_args.total_sub_sample_count:
            query['total_sub_sample_count'] = parsed_args.total_sub_sample_count
        if parsed_args.unconfirmed_sample_count:
            query['unconfirmed_sample_count'] = parsed_args.unconfirmed_sample_count
        if parsed_args.update_ms:
            query['update_ms'] = parsed_args.update_ms
        if parsed_args.data_path:
            query['data_path'] = parsed_args.data_path
        if parsed_args.data_type:
            query['data_type'] = parsed_args.data_type
        if parsed_args.schema_maps:
            query['schema_maps'] = parsed_args.schema_maps
        if parsed_args.source_info:
            query['source_info'] = parsed_args.source_info
        if parsed_args.with_column_header:
            query['with_column_header'] = parsed_args.with_column_header
        if parsed_args.dest_name:
            query['dest_name'] = parsed_args.dest_name
        if parsed_args.src_name:
            query['src_name'] = parsed_args.src_name
        if parsed_args.cluster_id:
            query['cluster_id'] = parsed_args.cluster_id
        if parsed_args.cluster_mode:
            query['cluster_mode'] = parsed_args.cluster_mode
        if parsed_args.cluster_name:
            query['cluster_name'] = parsed_args.cluster_name
        if parsed_args.database_name:
            query['database_name'] = parsed_args.database_name
        if parsed_args.input:
            query['input'] = parsed_args.input
        if parsed_args.ip:
            query['ip'] = parsed_args.ip
        if parsed_args.port:
            query['port'] = parsed_args.port
        if parsed_args.queue_name:
            query['queue_name'] = parsed_args.queue_name
        if parsed_args.subnet_id:
            query['subnet_id'] = parsed_args.subnet_id
        if parsed_args.table_name:
            query['table_name'] = parsed_args.table_name
        if parsed_args.user_name:
            query['user_name'] = parsed_args.user_name
        if parsed_args.user_password:
            query['user_password'] = parsed_args.user_password
        if parsed_args.vpc_id:
            query['vpc_id'] = parsed_args.vpc_id
        if parsed_args.file_num_finished:
            query['file_num_finished'] = parsed_args.file_num_finished
        if parsed_args.file_num_total:
            query['file_num_total'] = parsed_args.file_num_total
        if parsed_args.file_size_finished:
            query['file_size_finishedfile_size_finished'] = parsed_args.file_size_finished
        if parsed_args.file_size_total:
            query['file_size_total'] = parsed_args.file_size_total

        data = client.dataset_import_tasks(**query)

        table = (self.columns,
                 (utils.get_dict_properties(
                     _flatten_output(s), self.columns
                 ) for s in data))
        return table
