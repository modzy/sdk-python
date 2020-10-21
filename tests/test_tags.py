#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
import dotenv
import pytest

from modzy import ApiClient

dotenv.load_dotenv()

BASE_URL = os.getenv('MODZY_BASE_URL')
API_KEY = os.getenv('MODZY_API_KEY')


@pytest.fixture()
def client():
    return ApiClient(base_url=BASE_URL, api_key=API_KEY)


@pytest.fixture()
def logger():
    return logging.getLogger(__name__)


def test_get_all_tags(client, logger):
    tags = client.tags.get_all()
    logger.debug("tags: %s", len(tags))
    for tag in tags:
        logger.debug("tag: %s", tag)
        assert tag.identifier
        assert tag.name
        assert tag.data_type
    assert len(tags)


def test_get_tags_and_models(client, logger):
    tags, models = client.tags.get_tags_and_models('computer_vision')  # by identifier
    logger.debug("tags by computer_vision: %d", len(models))
    for tag in tags:
        logger.debug("tag: %s", tag)
        assert tag.identifier
        assert tag.name
        assert tag.data_type
    assert len(tags)
    logger.debug("models by computer_vision: %d", len(models))
    for model in models:
        logger.debug("model: %s", model)
        assert model.identifier
        assert model.name
        assert model.tags
    assert len(models)


def test_get_tags_and_models_by_tags(client, logger):
    tags, models = client.tags.get_tags_and_models(['computer_vision', 'enhance_or_preprocess'])  # by identifier
    logger.debug("tags by computer_vision, enhance_or_preprocess: %d", len(models))
    for tag in tags:
        logger.debug("tag: %s", tag)
        assert tag.identifier
        assert tag.name
        assert tag.data_type
    assert len(tags)
    logger.debug("models by computer_vision: %d", len(models))
    for model in models:
        logger.debug("model: %s", model)
        assert model.identifier
        assert model.name
        assert model.tags
    assert len(models)


def test_get_tags_and_models_invalid_tag(client, logger):
    tags, models = client.tags.get_tags_and_models('not-existing-tag')
    logger.debug("tags by not-existing-tag: %d", len(tags))
    logger.debug("models by not-existing-tag: %d", len(models))
    assert len(tags) == 0
    assert len(models) == 0
