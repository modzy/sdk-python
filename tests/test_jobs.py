#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
import dotenv
import pytest
import time
from datetime import datetime, timedelta
from modzy import ApiClient, error
from modzy.jobs import Jobs

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


def test_get_job_history(client, logger):
    jobs = client.jobs.get_history()
    logger.debug("jobs history: %d", len(jobs))
    for job in jobs:
        logger.debug("job: %s", job)
        assert job.job_identifier
        assert job.submitted_by
        assert job.model
        assert job.model.identifier
        assert job.model.version
        assert job.model.name
        assert job.status
    assert len(jobs)


def test_get_job_history_by_user(client, logger):
    params = {'user': 'a'}
    jobs = client.jobs.get_history(**params)
    logger.debug("jobs history: by %s %d", params, len(jobs))
    for job in jobs:
        assert job.job_identifier
        assert job.submitted_by
        assert job.model
        assert job.model.identifier
        assert job.model.version
        assert job.model.name
        assert job.status
    assert len(jobs)


def test_get_job_history_by_access_key(client, logger):
    params = {'access_key': API_KEY.split('.')[0]}
    jobs = client.jobs.get_history(**params)
    logger.debug("jobs history: by %s %d", params, len(jobs))
    for job in jobs:
        assert job.job_identifier
        assert job.submitted_by
        assert job.model
        assert job.model.identifier
        assert job.model.version
        assert job.model.name
        assert job.status
    assert len(jobs)


def test_get_job_history_by_date(client, logger):
    # by start date
    params = {'start_date': datetime.now() - timedelta(weeks=1)}
    jobs = client.jobs.get_history(**params)
    logger.debug("jobs history: by %s %d", params, len(jobs))
    assert len(jobs)
    # by end date (Should return a 400)
    params = {'end_date': datetime.now()}
    api_error = None
    try:
        client.jobs.get_history(**params)
    except error.ApiError as ae:
        logger.debug("jobs history: by %s %s", params, ae)
        api_error = ae
    assert api_error
    # by start and end date
    params = {'start_date': datetime(2019, 1, 1), 'end_date': datetime.now()}
    jobs = client.jobs.get_history(**params)
    logger.debug("jobs history: by %s %d", params, len(jobs))
    assert len(jobs)
    # by invalid start date
    params = {'start_date': datetime.now() + timedelta(days=1)}
    api_error = None
    try:
        client.jobs.get_history(**params)
    except error.ApiError as ae:
        logger.debug("jobs history: by %s %s", params, ae)
        api_error = ae
    assert api_error


def test_get_job_history_by_model(client, logger):
    # by model
    params = {'model': 'Sentiment Analysis'}
    jobs = client.jobs.get_history(**params)
    logger.debug("jobs history: by %s %d", params, len(jobs))
    logger.debug("jobs history: by %s %d", params, len(jobs))
    assert len(jobs)

def test_get_job_history_by_status(client, logger):
    # by all
    params = {'status': "all"}
    jobs = client.jobs.get_history(**params)
    logger.debug("jobs history: by %s %d", params, len(jobs))
    assert len(jobs)
    # by pending
    params = {'status': "pending"}
    client.jobs.submit_text(MODEL_ID, '0.0.27', {'input.txt': 'Modzy is great!'})
    time.sleep(5)
    jobs = client.jobs.get_history(**params)
    logger.debug("jobs history: by %s %d", params, len(jobs))
    assert len(jobs)
    # by terminated
    params = {'status': "terminated"}
    jobs = client.jobs.get_history(**params)
    logger.debug("jobs history: by %s %d", params, len(jobs))
    assert len(jobs)


def test_get_job_history_by_sort(client, logger):
    # order by status (default order direction)
    params = {'sort_by': "status"}
    jobs = client.jobs.get_history(**params)
    logger.debug("jobs history: by %s %d", params, len(jobs))
    assert len(jobs)
    # order by status asc
    params = {'sort_by': "status", 'direction': "asc"}
    jobs = client.jobs.get_history(**params)
    logger.debug("jobs history: by %s %d", params, len(jobs))
    assert len(jobs)
    # order by status desc
    params = {'sort_by': "status", 'direction': "desc"}
    jobs = client.jobs.get_history(**params)
    logger.debug("jobs history: by %s %d", params, len(jobs))
    assert len(jobs)


def test_submit_job(client, logger):
    job = client.jobs.submit_text(MODEL_ID, '0.0.27', {'input.txt': 'Modzy is great!'})
    logger.debug("job %s", job)
    assert job.job_identifier
    assert job.status == client.jobs.status.SUBMITTED


def test_get_job(client, logger):
    job = client.jobs.submit_text(MODEL_ID, '0.0.27', {'input.txt': 'Modzy is great!'})
    logger.debug("job %s", job)
    time.sleep(5)
    job = client.jobs.get(job.job_identifier)  # by id
    logger.debug("job copy by id %s", job)
    assert job.job_identifier
    assert job.status


def test_cancel_job(client, logger):
    job = client.jobs.submit_text(MODEL_ID, '0.0.27', {
        str(i): {'input.txt': 'Modzy is great!'}
        for i in range(2)
    })
    time.sleep(5)
    job = client.jobs.get(job.job_identifier)  # by id
    logger.debug("job %s", job)
    if job.status != Jobs.status.COMPLETED:
        logger.debug("job before cancel %s", job)
        job = client.jobs.cancel(job.job_identifier)
        logger.debug("job after cancel %s", job)

    assert job.status == client.jobs.status.CANCELED or job.status == client.jobs.status.COMPLETED

