# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#
# Code generated by Microsoft (R) AutoRest Code Generator 1.0.0.0
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class DataDriftRunDto(Model):
    """DataDriftRunDto.

    :param data_drift_id:
    :type data_drift_id: str
    :param execution_run_id:
    :type execution_run_id: str
    :param run_type: Possible values include: 'None', 'Adhoc', 'Scheduler',
     'BackFill'
    :type run_type: str or ~_restclient.models.enum
    :param start_time:
    :type start_time: datetime
    :param end_time:
    :type end_time: datetime
    :param id:
    :type id: str
    :param name:
    :type name: str
    :param type: Possible values include: 'ModelBased', 'DatasetBased'
    :type type: str or ~_restclient.models.enum
    :param model_name:
    :type model_name: str
    :param model_version:
    :type model_version: int
    :param base_dataset_id:
    :type base_dataset_id: str
    :param target_dataset_id:
    :type target_dataset_id: str
    :param services:
    :type services: list[str]
    :param compute_target_name:
    :type compute_target_name: str
    :param features:
    :type features: list[str]
    :param drift_threshold:
    :type drift_threshold: float
    :param job_latency:
    :type job_latency: int
    """

    _attribute_map = {
        'data_drift_id': {'key': 'dataDriftId', 'type': 'str'},
        'execution_run_id': {'key': 'executionRunId', 'type': 'str'},
        'run_type': {'key': 'runType', 'type': 'str'},
        'start_time': {'key': 'startTime', 'type': 'iso-8601'},
        'end_time': {'key': 'endTime', 'type': 'iso-8601'},
        'id': {'key': 'id', 'type': 'str'},
        'name': {'key': 'name', 'type': 'str'},
        'type': {'key': 'type', 'type': 'str'},
        'model_name': {'key': 'modelName', 'type': 'str'},
        'model_version': {'key': 'modelVersion', 'type': 'int'},
        'base_dataset_id': {'key': 'baseDatasetId', 'type': 'str'},
        'target_dataset_id': {'key': 'targetDatasetId', 'type': 'str'},
        'services': {'key': 'services', 'type': '[str]'},
        'compute_target_name': {'key': 'computeTargetName', 'type': 'str'},
        'features': {'key': 'features', 'type': '[str]'},
        'drift_threshold': {'key': 'driftThreshold', 'type': 'float'},
        'job_latency': {'key': 'jobLatency', 'type': 'int'},
    }

    def __init__(self, **kwargs):
        super(DataDriftRunDto, self).__init__(**kwargs)
        self.data_drift_id = kwargs.get('data_drift_id', None)
        self.execution_run_id = kwargs.get('execution_run_id', None)
        self.run_type = kwargs.get('run_type', None)
        self.start_time = kwargs.get('start_time', None)
        self.end_time = kwargs.get('end_time', None)
        self.id = kwargs.get('id', None)
        self.name = kwargs.get('name', None)
        self.type = kwargs.get('type', None)
        self.model_name = kwargs.get('model_name', None)
        self.model_version = kwargs.get('model_version', None)
        self.base_dataset_id = kwargs.get('base_dataset_id', None)
        self.target_dataset_id = kwargs.get('target_dataset_id', None)
        self.services = kwargs.get('services', None)
        self.compute_target_name = kwargs.get('compute_target_name', None)
        self.features = kwargs.get('features', None)
        self.drift_threshold = kwargs.get('drift_threshold', None)
        self.job_latency = kwargs.get('job_latency', None)
