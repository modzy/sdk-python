# -*- coding: utf-8 -*-
"""Classes for interacting with models."""

import logging

from ._api_object import ApiObject


class Models:
    """The `Models` object.

    This object is used to retreive information about models from the API.

    Note:
        This class should not be instantiated directly but rather accessed through the `models`
        attribute of an `ApiClient` instance.
    """

    _base_route = '/models'

    def __init__(self, api_client):
        """Creates a `Models` instance.

        Args:
            api_client (ApiClient): An `ApiClient` instance.
        """
        self._api_client = api_client
        self.logger = logging.getLogger(__name__)

    def get(self, model):
        """Gets a `Model` instance.

        Args:
            model (Union[str, Model]): The model identifier or a `Model` instance.

        Returns:
            Model: The `Model` instance.

        Raises:
            ApiError: A subclass of ApiError will be raised if the API returns an error status,
                or the client is unable to connect.
        """
        modelId = Model._coerce_identifier(model)
        self.logger.debug("getting model %s", model)
        json_obj = self._api_client.http.get('{}/{}'.format(self._base_route, modelId))
        return Model(json_obj, self._api_client)

    def get_related(self, model):
        """Gets a list of all the models associated with the model provided, together with the model’s details.

        Returns:
            List[Model]: A list of `Model` instances.

        Raises:
            ApiError: A subclass of ApiError will be raised if the API returns an error status,
                or the client is unable to connect.
        """
        self.logger.debug("getting models related to model %s", model)
        identifier = Model._coerce_identifier(model)
        json_list = self._api_client.http.get('{}/{}/related-models'.format(self._base_route, identifier))
        return list(Model(json_obj, self._api_client) for json_obj in json_list)

    def get_versions(self, model):
        """Gets a list of all the versions associated with the model provided.

        Returns:
            List[ModelVersion]: A list of `Version` instances.

        Raises:
            ApiError: A subclass of ApiError will be raised if the API returns an error status,
                or the client is unable to connect.
        """
        self.logger.debug("getting versions related to model %s", model)
        identifier = Model._coerce_identifier(model)
        json_list = self._api_client.http.get('{}/{}/versions'.format(self._base_route, identifier))
        return list(ModelVersion(json_obj, self._api_client) for json_obj in json_list)

    def get_version(self, model, version):
        """Gets a versions associated with the model provided.

        Returns:
            ModelVersion: A instance of `ModelVersion` instances.

        Raises:
            ApiError: A subclass of ApiError will be raised if the API returns an error status,
                or the client is unable to connect.
        """
        self.logger.debug("getting versopm model %s version %s", model, version)
        modelId = Model._coerce_identifier(model)
        versionId = ModelVersion._coerce_identifier(version)
        json_obj = self._api_client.http.get('{}/{}/versions/{}'.format(self._base_route, modelId, versionId))
        return ModelVersion(json_obj, self._api_client)

    def get_all(self):
        """Gets a list of all `Model` instances.

        Returns:
            List[Model]: A list of `Model` instances.

        Raises:
            ApiError: A subclass of ApiError will be raised if the API returns an error status,
                or the client is unable to connect.
        """
        self.logger.debug("getting all models")
        json_list = self._api_client.http.get(self._base_route)
        return list(Model(json_obj, self._api_client) for json_obj in json_list)


class Model(ApiObject):
    """A model object.

    This object contains a parsed copy of the information returned from the server about a certain model.

    Attributes:
        identifier (str): The model identifier.

    Note:
        This class should not be instantiated directly. Instead, it is returned by various package
        functions.
        This object is a `dict` subclass that also supports attribute access. Information can be
        accessed through dotted attribute notation using "snake_case" or the original "camelCase" JSON
        key name (``model.long_description`` or ``model.longDescription``). Alternatively, the original
        "camelCase" JSON key can be used with bracketed key access notation (``model['longDescription']``).
    """
    def __init__(self, json_obj, api_client=None):
        super().__init__(json_obj, api_client)
        if "identifier" in self.keys():  # Temporal fix for the duplicity between modelId and identifier results
            self["modelId"] = self["identifier"]

    @classmethod
    def _coerce_identifier(cls, maybe_model):
        modelId = getattr(maybe_model, 'modelId', maybe_model)
        if not isinstance(modelId, str):
            raise TypeError('the identifier must be {} or str, not {}'
                            .format(cls.__name__, type(maybe_model).__name__))
        return modelId

    def sync(self):
        """Updates the `Model` instance's data in-place with new data from the API.

        Returns:
            Model: The `Model` instance (self).

        Raises:
            ApiError: A subclass of ApiError will be raised if the API returns an error status,
                or the client is unable to connect.
        """
        updated = self._api_client.models.get(self.modelId)
        self.update(updated)  # is updating in place a bad idea?
        return self

    def get_versions(self):
        """Gets a list of all the versions associated with this model.

        Returns:
            List[Version]: A list of `Version` instances.

        Raises:
            ApiError: A subclass of ApiError will be raised if the API returns an error status,
                or the client is unable to connect.
        """
        return self._api_client.models.get_versions(self.modelId)

    def get_related(self):
        """Gets a list of all the models associated with this model.

        Returns:
            List[Model]: A list of `Model` instances.

        Raises:
            ApiError: A subclass of ApiError will be raised if the API returns an error status,
                or the client is unable to connect.
        """
        return self._api_client.models.get_related(self.modelId)

    def submit_text(self, version, source, source_name='job'):
        """Submits text data for a single source `Job`.

        See:
            :py:meth:`modzy.jobs.Jobs.submit_text`
        """
        return self._api_client.jobs.submit_text(self.modelId, version, source, source_name=source_name)

    def submit_text_bulk(self, version, sources):
        """Submits text data for a multiple source `Job`.

        See:
            :py:meth:`modzy.jobs.Jobs.submit_text_bulk`
        """
        return self._api_client.jobs.submit_text_bulk(self.modelId, version, sources)

    def submit_bytes(self, version, source, source_name='job'):
        """Submits bytes-like data for a single source `Job`.

        See:
            :py:meth:`modzy.jobs.Jobs.submit_bytes`
        """
        return self._api_client.jobs.submit_bytes(self.modelId, version, source, source_name=source_name)

    def submit_bytes_bulk(self, version, sources):
        """Submits bytes-like data for a multiple source `Job`.

        See:
            :py:meth:`modzy.jobs.Jobs.submit_bytes_bulk`
        """
        return self._api_client.jobs.submit_bytes_bulk(self.modelId, version, sources)

    def submit_files(self, version, source, source_name='job'):
        """Submits a filepath or file-like data for a single source `Job`.

        See:
            :py:meth:`modzy.jobs.Jobs.submit_files`
        """

        return self._api_client.jobs.submit_files(self.modelId, version, source, source_name=source_name)

    def submit_files_bulk(self, version, sources):
        """Submits a filepath or file-like data for a multiple source `Job`.

        See:
            :py:meth:`modzy.jobs.Jobs.submit_files_bulk`
        """
        return self._api_client.jobs.submit_files_bulk(self.modelId, version, sources)

    def submit_aws_s3(self, version, source, access_key_id, secret_access_key, region, source_name='job'):
        """Submits AwS S3 hosted data for a single source `Job`.

        See:
            :py:meth:`modzy.jobs.Jobs.submit_aws_s3`
        """
        return self._api_client.jobs.submit_aws_s3(self.modelId, version, source,
                                                   access_key_id, secret_access_key, region, source_name=source_name)

    def submit_aws_s3_bulk(self, version, sources, access_key_id, secret_access_key, region):
        """Submits AwS S3 hosted data for a multiple source `Job`.

        See:
            :py:meth:`modzy.jobs.Jobs.submit_aws_s3_bulk`
        """
        return self._api_client.jobs.submit_aws_s3_bulk(self.modelId, version, sources, access_key_id,
                                                        secret_access_key, region)

    def submit_jdbc(self, version, url, username, password, driver, query):
        """Submits jdbc query as input for a `Job`, each row is interpreted as a input.

        See:
            :py:meth:`modzy.jobs.Jobs.submit_jdbc`
        """
        return self._api_client.jobs.submit_jdbc(self.modelId, version, url, username, password, driver, query)

    def __str__(self):
        return "Model(modelId='{}')".format(self.modelId)


class ModelVersion(ApiObject):
    """A model version object.

    This object contains a parsed copy of the information returned from the server about a certain model version.

    Attributes:
        version (str): The model version identifier.

    Note:
        This class should not be instantiated directly. Instead, it is returned by various package
        functions.
        This object is a `dict` subclass that also supports attribute access. Information can be
        accessed through dotted attribute notation using "snake_case" or the original "camelCase" JSON
        key name (``model.long_description`` or ``model.longDescription``). Alternatively, the original
        "camelCase" JSON key can be used with bracketed key access notation (``model['longDescription']``).
    """

    @classmethod
    def _coerce_identifier(cls, maybe_model_version):
        versionId = getattr(maybe_model_version, 'version', maybe_model_version)
        if not isinstance(versionId, str):
            raise TypeError('the identifier must be {} or str, not {}'
                            .format(cls.__name__, type(maybe_model_version).__name__))
        return versionId

    def __str__(self):
        return "ModelVersion(version='{}')".format(self.version)
