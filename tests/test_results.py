#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
import dotenv
import pytest
from datetime import datetime, timedelta
from modzy import ApiClient, error

dotenv.load_dotenv()

BASE_URL = os.getenv('MODZY_BASE_URL')
API_KEY = os.getenv('MODZY_API_KEY')

MODEL_ID = 'ed542963de'  # sentiment-analysis
BLOCK_TIMEOUT = 600  # how long to wait until giving up on real api

@pytest.fixture()
def client():
    return ApiClient(base_url=BASE_URL, api_key=API_KEY)

@pytest.fixture()
def logger():
    return logging.getLogger(__name__)

def test_get_results(client, logger):
    job = client.jobs.submit_text(MODEL_ID, '0.0.27', {'input.txt': 'Modzy is great!'})
    logger.debug("job %s", job)
    job.block_until_complete(timeout=BLOCK_TIMEOUT)
    logger.debug("job after block %s", job)
    result = client.results.get(job.job_identifier)   # by id
    logger.debug("job results by id %s: %s", job, result)
    result_copy = client.results.get(job)   # by object
    logger.debug("job results by object %s: %s", job, result_copy)
    assert result is not result_copy
    assert result.job_identifier == result_copy.job_identifier
