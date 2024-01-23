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
from openstack import proxy
from otcextensions.sdk.modelartsv1.v1 import clusters as _clusters
from otcextensions.sdk.modelartsv1.v1 import devenv as _devenv
from otcextensions.sdk.modelartsv1.v1 import model as _model
from otcextensions.sdk.modelartsv1.v1 import service as _service
from otcextensions.sdk.modelartsv1.v1 import \
    service_deployment_specification as _service_deployment_specification
from otcextensions.sdk.modelartsv1.v1 import \
    service_event_log as _service_event_log
from otcextensions.sdk.modelartsv1.v1 import \
    service_monitor_info as _service_monitor_info
from otcextensions.sdk.modelartsv1.v1 import \
    service_update_log as _service_update_log
from otcextensions.sdk.modelartsv1.v1 import trainingjob as _trainingjob
from otcextensions.sdk.modelartsv1.v1 import \
    trainingjob_config as _trainingjob_config
from otcextensions.sdk.modelartsv1.v1 import \
    trainingjob_version as _trainingjob_version
from otcextensions.sdk.modelartsv1.v1 import \
    visualization_job as _visualization_job
from otcextensions.sdk.modelartsv1.v1 import \
    service_configuration_update as _service_configuration_update


class Proxy(proxy.Proxy):
    skip_discovery = True

    def __init__(self, session, *args, **kwargs):
        super(Proxy, self).__init__(session=session, *args, **kwargs)
        self.additional_headers = {
            "Accept": "application/json",
            "Content-type": "application/json",
        }

    # ======== Model Management ========

    def models(self, **params):
        """List all Models.

        :returns: a generator of
            :class:`~otcextensions.sdk.modelartsv1.v1.models.Model` instances
        """
        return self._list(_model.Model, **params)

    def create_model(self, **attrs):
        """Create a model from attributes

        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.modelartsv1.v1.models.Model`,
            comprised of the properties on the Model class.
        :returns: The results of model creation
        :rtype: :class:`~otcextensions.modelartsv1.v1.model.Model`
        """
        return self._create(_model.Model, prepend_key=False, **attrs)

    def get_model(self, model):
        """Get the model by id

        :param model: key id or an instance of
            :class:`~otcextensions.sdk.modelartsv1.v1.model.Model`

        :returns: instance of
            :class:`~otcextensions.sdk.modelartsv1.v1.model.Model`
        """
        return self._get(_model.Model, model)

    def find_model(self, name_or_id, ignore_missing=False):
        """Find a single model

        :param name_or_id: The name or ID of a ModelArts model
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised
            if the model does not exist.
            When set to ``True``, no exception will be set when attempting
            to find a nonexistent cluster.

        :returns:
            One :class:`~otcextensions.sdk.modelartsv1.v1.model.Model`
            or ``None``
        """
        return self._find(
            _model.Model, name_or_id, ignore_missing=ignore_missing
        )

    def delete_model(self, model, ignore_missing=False):
        """Delete a model

        :param model: Thie value can be the id of a model
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised when
            the model does not exist.
            When set to ``True``, no exception will be set when attempting to
            delete a nonexistent model.
        """
        return self._delete(_model.Model, model, ignore_missing=ignore_missing)

    # ======== DevEnviron Management ========

    def devenv_instances(self, **params):
        """List all Devenv Instances.

        :returns: a generator of
            :class:`~otcextensions.sdk.modelartsv1.v1.devenv.Devenv` instances.
        """
        if params.get("limit"):
            params.update(paginated=False)
        return self._list(_devenv.Devenv, **params)

    def create_devenv_instance(self, **attrs):
        """Create a devenv instance from attributes.

        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.modelartsv1.v1.devenv.Devenv`,
            comprised of the properties on the Devenv class.
        :returns: The results of demanager creation
        :rtype: :class:`~otcextensions.sdk.modelartsv1.v1.devenv.Devenv`
        """
        return self._create(_devenv.Devenv, prepend_key=False, **attrs)

    def delete_devenv_instance(self, instance, ignore_missing=False):
        """Delete a Devenv instance.

        :param instance: key id or an instance of
            :class:`~otcextensions.sdk.modelartsv1.v1.devenv.Devenv`
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised when
            the group does not exist.
            When set to ``True``, no exception will be set when attempting to
            delete a nonexistent devenv.
        """
        return self._delete(
            _devenv.Devenv, instance, ignore_missing=ignore_missing
        )

    def get_devenv_instance(self, instance):
        """Get details of a Devenv Instance.

        :param instance: key id or an instance of
            :class:`~otcextensions.sdk.modelartsv1.v1.devenv.Devenv`

        :returns: instance of
            :class:`~otcextensions.sdk.modelartsv1.v1.devenv.Devenv`
        """
        return self._get(_devenv.Devenv, instance)

    def find_devenv_instance(self, name_or_id, ignore_missing=False):
        """Find a single Devenv instance by name or Id.

        :param name_or_id: The name or ID of a Devenv instance.

        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised
            if the devenv does not exist.
            When set to ``True``, no exception will be set when attempting
            to find a nonexistent devenv.

        :returns:
            One :class:`~otcextensions.sdk.modelartsv1.v1.devenv.Devenv`
            or ``None``
        """
        return self._find(
            _devenv.Devenv,
            name_or_id,
            ignore_missing=ignore_missing,
            de_type="Notebook",
        )

    def start_devenv_instance(self, instance):
        """Start a Devenv instance.

        :param instance: key id or an instance of
            :class:`~otcextensions.sdk.modelartsv1.v1.devenv.Devenv`
        :returns: instance of
            :class:`~otcextensions.sdk.modelartsv1.v1.devenv.Devenv`
        """
        devenv = self._get_resource(_devenv.Devenv, instance)
        return devenv.start(self)

    def stop_devenv_instance(self, instance):
        """Stop a Devenv instance.

        :param instance: key id or an instance of
            :class:`~otcextensions.sdk.modelartsv1.v1.devenv.Devenv`

        :returns: instance of
            :class:`~otcextensions.sdk.modelartsv1.v1.devenv.Devenv`
        """
        devenv = self._get_resource(_devenv.Devenv, instance)
        return devenv.stop(self)

    # Service Management

    def services(self, **attrs):
        """List all Services.

        :returns: a generator of
            :class:`~otcextensions.sdk.modelartsv1.v1.services.Services`
            instances
        """
        return self._list(_service.Service)

    def create_service(self, **attrs):
        """Deploy a model from attributes

        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.modelartsv1.v1.service.Service`,
            comprised of the properties on the Service class.
        :returns: The result of service creation.
        :rtype: :class:`~otcextensions.sdk.modelartsv1.v1.services.Services`
        """
        return self._create(_service.Service, prepend_key=False, **attrs)

    def delete_service(self, service, ignore_missing=False):
        """Delete a service
        :param service: key id or an instance of
            :class:`~otcextensions.sdk.modelartsv1.v1.service.Service`
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised when
            the service does not exist.
            When set to ``True``, no exception will be set when attempting to
            delete a nonexistent service.
        :returns: ``None``
        """
        return self._delete(
            _service.Service, service, ignore_missing=ignore_missing
        )

    def get_service(self, service):
        """Get the service by UUID

        :param service: key id or an instance of
            :class:`~otcextensions.sdk.modelartsv1.v1.service.Service`

        :returns: instance of
            :class:`~otcextensions.sdk.modelartsv1.v1.service.Service`
        """
        return self._get(_service.Service, service)

    def find_service(self, name_or_id, ignore_missing=False):
        """Find a single service

        :param name_or_id: The name or ID of a ModelArts service
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised
            if the service does not exist.
            When set to ``True``, no exception will be set when attempting
            to find a nonexistent service.

        :returns:
            One :class:`~otcextensions.sdk.modelartsv1.v1.service.Service`
            or ``None``
        """
        return self._find(
            _service.Service, name_or_id, ignore_missing=ignore_missing
        )

    def update_service_configurations(self, service_id, **attrs):
        """Get the dataset by id

        :param dataset: key id or an instance of
            :class:`~otcextensions.sdk.modelartsv2.v2.datasets.Datasets`

        :returns: instance of
            :class:`~otcextensions.sdk.modelartsv2.v2.datasets.Datasets`
        """
        return self._update(_service_configuration_update.ServiceConfigurationUpdate, service_id, **attrs)


    # Training Job Management

    def trainingjobs(self, **params):
        """List all training jobs.

        :returns: a generator of
            :class:`~otcextensions.sdk.modelartsv1.v1.trainjob.Trainjob`
            instances
        """
        return self._list(_trainingjob.TrainingJob, **params)

    def trainingjob_versions(self, job_id, **attrs):
        """List all training job versions.

        :returns: a generator of
            :class:`~otcextensions.sdk.modelartsv1.v1.trainjob_version.\
                    TrainjobVersion` instances
        """
        return self._list(
            _trainingjob_version.TrainingJobVersion, jobId=job_id, **attrs
        )

    def create_training_job(self, **attrs):
        """Create a training job from attributes

        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.modelartsv1.v1.trainjob.Trainjob`,
            comprised of the properties on the Trainjob class.

        :returns: The results of trainjobs creation
        :rtype: :class:`~otcextensions.sdk.modelartsv1.v1.trainjob.Trainjob`
        """
        return self._create(
            _trainingjob.TrainingJob, prepend_key=False, **attrs
        )

    def delete_trainingjob(self, job_id):
        """Delete a training job

        :param job_id: Thie value can be the id of a training job
        """
        return self._delete(_trainingjob.TrainingJob, job_id)

    def find_trainingjob(self, name_or_id, ignore_missing=False):
        """Find a single trainjob

        :param name_or_id: The name or ID of a ModelArts trainjob
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised
            if the trainjob does not exist.
            When set to ``True``, no exception will be set when attempting
            to find a nonexistent trainjob.

        :returns: One :class:
          `~otcextensions.sdk.modelartsv1.v1.trainjob.Trainjob` or ``None``
        """
        return self._find(
            _trainingjob.TrainingJob, name_or_id, ignore_missing=ignore_missing
        )

    def show_trainingjob_version(self, version_id, **attrs):
        """Get the trainjob version by id

        :param version_id: key id or an instance of
            :class:`~otcextensions.sdk.modelartsv1.v1.trainjob_version.TrainjobVersion`

        :returns: instance of
            :class:`~otcextensions.sdk.modelartsv1.v1.trainjob_version.TrainjobVersion`
        """
        return self._get(
            _trainingjob_version.TrainingJobVersion, version_id, **attrs
        )

    def modify_trainingjob_description(self, job_id, **attrs):
        """Get the dataset by id

        :param dataset: key id or an instance of
            :class:`~otcextensions.sdk.modelarts.v2.datasets.Datasets`

        :returns: instance of
            :class:`~otcextensions.sdk.modelarts.v2.datasets.Datasets`
        """
        return self._update(_trainingjob.TrainingJob, job_id, **attrs)

    def create_trainingjob_version(self, job_id, **attrs):
        """Create a training job from attributes

        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.modelartsv1.v1.trainjob.Trainjob`,
            comprised of the properties on the Trainjob class.

        :returns: The results of trainjobs creation
        :rtype: :class:`~otcextensions.sdk.modelartsv1.v1.trainjob.Trainjob`
        """
        print("****************", attrs)
        return self._create(
            _trainingjob_version.TrainingJobVersion,
            jobId=job_id,
            prepend_key=False,
            **attrs
        )

    def delete_trainingjob_version(self, version_id, *attrs):
        """Delete a training job version

        :param version_id: Thie value can be the id of a training job version
        """
        return self._delete(
            _trainingjob_version.TrainingJobVersion, version_id, **attrs
        )

    def trainingjob_configuration(self, **attrs):
        """List all Training Job Configurations.

        :returns: a generator of
            (:class:`~otcextensions.sdk.modelartsv1.v1.trainjob_configs.\
                TrainjobConfigs`) instances
        """
        return self._list(_trainingjob_config.TrainingjobConfig, **attrs)

    def create_trainingjob_config(self, **attrs):
        """Create a Training Job Configuration from attributes

        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.modelartsv1.v1.trainjob_configs.\
                TrainjobConfigs`, comprised of the properties on the
                Training Job Configuration class.
        :returns: The results of Training Job Configuration creation
        :rtype: :class:`~otcextensions.sdk.modelartsv1.v1.trainjob_configs.\
            TrainjobConfigs`
        """
        return self._create(
            _trainingjob_config.TrainingjobConfig, prepend_key=False, **attrs
        )

    def delete_trainingjob_config(self, config_name):
        """Delete a Training Job Configuration

        :param trainjob_config: Thie value can be the id of a trainjob_configs
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised when
            the group does not exist.
            When set to ``True``, no exception will be set when attempting to
            delete a nonexistent Training Job Configuration.
        """
        return self._delete(
            _trainingjob_config.TrainingjobConfig,
            config_name,
            ignore_missing=True,
        )

    def show_trainingjob_conf(self, trainingjob_config):
        """Get the Training Job Configuration by id

        :param trainjob_config: key id or an instance of
            :class:`~otcextensions.sdk.modelartsv1.v1.trainjob_config.TrainjobConfigs`

        :returns: instance of
            :class:`~otcextensions.sdk.modelartsv1.v1.trainjob_config.TrainjobConfigs`
        """
        return self._get(
            _trainingjob_config.TrainjobConfig, trainingjob_config
        )

    # Visualization Job Management

    def visualization_jobs(self):
        """List all Visualization Job.

        :returns: a generator of :class:
          `~otcextensions.sdk.modelartsv1.v1.visualization_job.VisualizationJob`
          instances
        """
        return self._list(_visualization_job.VisualizationJob)

    def create_visualizationjob(self, **attrs):
        """Create a Visualization Job from attributes

        :param dict attrs: Keyword arguments which will be used to create a
            :class:`~otcextensions.sdk.modelartsv1.v1.visualization_job.\
                VisualizationJob` comprised of the properties on
                the Visualization Job class.

        :returns: The results of Visualization Job creation

        :rtype:
            :class:`~otcextensions.sdk.modelartsv1.v1.visualization_job.\
                VisualizationJob`
        """
        return self._create(
            _visualization_job.VisualizationJob, prepend_key=False, **attrs
        )

    def delete_visualizationjob(self, visualization_job, ignore_missing=False):
        """Delete a Visualization Job

        :param visualization_job: Thie value can be the name of a
            Visualization Job
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised when
            the group does not exist.
            When set to ``True``, no exception will be set when attempting to
            delete a nonexistent Visualization Job.
        """
        return self._delete(
            _visualization_job.VisualizationJob,
            visualization_job,
            ignore_missing=ignore_missing,
        )

    def show_visualizationjob(self, visualization_job):
        """Get the Visualization Job by id

        :param visualization_job: key id or an instance of
            :class:`~otcextensions.sdk.modelartsv1.v1.visualization_jobs.\
                VisualizationJobs`

        :returns: instance of
            :class:`~otcextensions.sdk.modelartsv1.v1.visualization_jobs.\
                VisualizationJobs`
        """
        return self._get(
            _visualization_job.VisualizationJob, visualization_job
        )

    def stop_visualizationjob(self, visualization_job):
        """Stop a VisualizationJob

        :param instance: key id or an instance of
            :class:`~otcextensions.sdk.modelartsv1.v1.devenv.Devenv`

        :returns: instance of
            :class:`~otcextensions.sdk.modelartsv1.v1.devenv.Devenv`
        """
        visjob = self._get_resource(
            _visualization_job.VisualizationJob, visualization_job
        )
        return visjob.stop(self)

    def service_monitoring_info(self, **attrs):
        """List all service monitoring information.

        :returns: a generator of
            (:class:`~otcextensions.sdk.modelartsv1.v1.service_monitoring_info.\
                ServiceMonitoringInfo`) instances
        """
        return self._list(
            _service_monitor_info.ServiceMonitoringInformation, **attrs
        )

    def service_event_logs(self, **attrs):
        """List all service event logs.

        :returns: a generator of
            (:class:`~otcextensions.sdk.modelartsv1.v1.service_event_logs.\
                ServiceEventLogs`) instances
        """
        return self._list(_service_event_log.ServiceEventLog, **attrs)

    def service_update_logs(self, **attrs):
        """List all service update logs.

        :returns: a generator of
            (:class:`~otcextensions.sdk.modelartsv1.v1.service_update_logs.\
                ServiceUpdateLogs`) instances
        """
        return self._list(_service_update_log.ServiceUpdateLog, **attrs)

    def service_deploy_specs(self):
        """List all service update logs.

        :returns: a generator of
            (:class:`~otcextensions.sdk.modelartsv1.v1.clusters.\
                ServiceDeploySpecs`) instances
        """
        return self._list(_service_deployment_specification.ServiceUpdateLogs)

    def dedic_res_pools(self):
        return self._list(_clusters.DedicatedResourcePool)
