#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Test for Models & Model classes."""

import os
import dotenv
import pytest
from modzy import ApiClient, error
import logging

dotenv.load_dotenv()

BASE_URL = os.getenv('MODZY_BASE_URL')
API_KEY = os.getenv('MODZY_API_KEY')


MODEL_ID = 'ed542963de'  # sentiment-analysis


@pytest.fixture()
def client():
    return ApiClient(base_url=BASE_URL, api_key=API_KEY)


@pytest.fixture()
def logger():
    return logging.getLogger(__name__)


def test_get_all_model_objects(client, logger):
    models = client.models.get_all()
    logger.debug("models: %s", len(models))
    for model in models:
        logger.debug("model: %s", model)
        logger.debug("model keys: %s", model.keys())
        assert model.modelId
        logger.debug("latestVersion: %s", model.latestVersion)
        assert "latestVersion" in model.keys()
        logger.debug("versions: %s", model.versions)
        assert hasattr(model, 'versions')

    assert len(models)  # just going to assume there should be some models


def test_get_single_model(client, logger):
    model = client.models.get(MODEL_ID)  # by id
    logger.debug("model_modelId: %s", model.modelId)
    assert model.modelId
    logger.debug("model_latestVersion: %s", model.latestVersion)
    assert model.latestVersion
    logger.debug("model_versions: %s", model.versions)
    assert len(model.versions) >= 0

    model_copy = client.models.get(model)  # from object
    assert model.modelId == model_copy.modelId

def test_get_model_by_name(client, logger):
    model = client.models.get_by_name("Military Equipment Classification")  # by name
    logger.debug("model_modelId: %s", model.modelId)
    assert model.modelId
    logger.debug("model_latestVersion: %s", model.latestVersion)
    assert model.latestVersion
    logger.debug("model_versions: %s", model.versions)
    assert len(model.versions) >= 0


def test_get_single_model_invalid(client, logger):
    api_error = None
    try:
        client.models.get('notamodelidentifier')
    except error.NotFoundError as ae:
        api_error = ae
    assert api_error.message
    assert api_error.url
    assert api_error.response.status_code == 404


def test_get_related_models(client, logger):
    models = client.models.get_related(MODEL_ID)
    logger.debug("models related to sentiment-analysis: %s", len(models))
    for model in models:
        logger.debug("model: %s", model)
        assert model.modelId
    assert len(models)  # just going to assume there should be some models


def test_model_sync(client, logger):
    model = client.models.get(MODEL_ID)  # by id
    logger.debug("models sentiment-analysis: %s", model)
    original_latestVersion = model.latestVersion
    model.latestVersion = 'Not.The.Latest'
    model.sync()
    logger.debug("models sentiment-analysis sync: %s", model)
    assert model.latestVersion == original_latestVersion


def test_get_model_versions(client, logger):
    versions = client.models.get_versions(MODEL_ID)
    logger.debug("versions related to sentiment-analysis: %s", len(versions))
    for version in versions:
        logger.debug("version: %s", version)
        assert version.version
    assert len(version)  # just going to assume there should be some versions


def test_get_model_version(client, logger):
    version = client.models.get_version(MODEL_ID, '0.0.27')
    logger.debug("version: %s", version)
    assert version.version


def test_get_model_version_input_sample(client, logger):
    input_sample = client.models.get_version_input_sample(MODEL_ID, '0.0.27')
    logger.debug("version: %s", input_sample)
    assert input_sample


def test_get_model_version_output_sample(client, logger):
    output_sample = client.models.get_version_output_sample(MODEL_ID, '0.0.27')
    logger.debug("version: %s", output_sample)
    assert output_sample


def test_get_model_processing_details(client):
    client.models.get_model_processing_details(MODEL_ID, "0.0.27")


def test_get_minimum_engines(client):
    client.models.get_minimum_engines()


def test_update_processing_state(client):
    client.models.update_processing_engines(MODEL_ID, "0.0.27", 0, 1)


def test_update_processing_state_wait(client):
    client.models.update_processing_engines(MODEL_ID, "0.0.27", 2, 2, None)


@pytest.mark.parametrize("engine_min_max", [(100, 200), (1, 0)])
def test_processing_state_errors(client, engine_min_max):
    min_engines, max_engines = engine_min_max
    with pytest.raises(ValueError):
        client.models.update_processing_engines(MODEL_ID, "0.0.27", min_engines, max_engines)
