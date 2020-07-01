=====
Usage
=====

Basic usage of Modzy Python in a project::

    from modzy import ApiClient, error

    client = ApiClient(base_url='https://modzy.example.com/api', api_key='my-api-key')

    # submit a job using the model identifier and version and with an input file for data
    job = client.jobs.submit_files('ed542963de', '0.0.27', {'input.txt': './some-file.txt'})
    # wait forever for the results of the job to finish
    result = client.results.block_until_complete(job, timeout=None)
    # get the the first (and only) outputs for the job and select the output file of interest
    results_json = result.get_first_outputs()['results.json']
    print(results_json)

    # or
    model = client.models.get('ed542963de')
    job = model.submit_files('0.0.27', {'input.txt': './some-file.txt'})
    job.block_until_complete(timeout=None)
    result = job.get_result()
    results_json = result.get_first_outputs()['results.json']
    print(results_json)

Handling errors::

    from modzy import ApiClient, error

    client = ApiClient(base_url='https://modzy.example.com/api', api_key='my-api-key')

    # Any functions that work with the API may raise a `NetworkError` indicating that the client was
    # unable to connect or a `ResponseError` to indicate that the API returned an error code. You may
    # handle both by catching the `ApiError` base class.
    try:
        job = client.jobs.submit_files('ed542963de', '0.0.27', {'input.txt': './some-file.txt'})
    except error.NetworkError as ex:
        print('Could not connect to the API:', ex)
        raise
    except error.ResponseError as ex:
        print('We got an error response from the API:', ex)
        raise

    # Blocking functions will additionally raise a `Timeout` exception if they do not finish before
    # the configurable timeout has elapsed.
    timeout = 600
    try:
        result = client.results.block_until_complete(job, timeout=timeout)
    except error.Timeout as ex:
        print('Job still not finished after %d seconds' % timeout)
        raise
    except error.NetworkError as ex:
        print('Could not connect to the API:', ex)
        raise
    except error.ResponseError as ex:
        print('We got an error response from the API:', ex)
        raise

    # The utility functions to retrieve outputs will raise `ResultsError` if the model returned
    # an error during the job run.
    try:
        outputs = result.get_first_outputs()
    except error.ResultsError as ex:
        print('the model returned an error:', ex)
        raise

    results_json = outputs['results.json']
    print(results_json)


Submitting arbitrary Python objects::

    import io
    from PIL import Image
    from modzy import ApiClient, error

    client = ApiClient(base_url='https://modzy.example.com/api', api_key='my-api-key')
    image = Image.open('my-car-picture.jpg')

    # you must submit file paths or file-like objects using `submit_files`; the following won't work:
    try:
        client.jobs.submit_files('car-classifier', '0.0.1', {'image': image})
    except TypeError as ex:
        print('Client does not know how to read PIL Image object:', ex)

    # convert to file-like object
    def pil_image_to_bytesio(image, format='PNG'):
        buff = io.BytesIO()
        image.save(buff, format=format)
        buff.seek(0)
        return buff

    job = client.jobs.submit_files('car-classifier', '0.0.1', {'image': pil_image_to_bytesio(image)})

    # alternatively, convert the object to raw bytes and use `submit_bytes`
    def pil_image_to_bytes(image, format='PNG'):
        buff = io.BytesIO()
        image.save(buff, format=format)
        return buff.getvalue()

    job = client.jobs.submit_bytes('car-classifier', '0.0.1', {'image': pil_image_to_bytes(image)})


In depth usage examples::

    import io
    import json
    import os
    import pathlib

    from modzy import ApiClient, error

    BASE_URL = os.environ.get('MODZY_BASE_URL', 'https://modzy.example.com/api')
    API_KEY = os.environ.get('MODZY_API_KEY', 'modzy-api-key')

    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', 'NOT A REAL ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', 'NOT A REAL KEY')
    AWS_DEFAULT_REGION = os.environ.get('AWS_DEFAULT_REGION', 'us-east-1')

    client = ApiClient(base_url=BASE_URL, api_key=API_KEY)

    # get all model objects
    models = client.models.get_all()
    print('%d models' % len(models))

    # get single model
    model = client.models.get('ed542963de')  # by id

    print('model name:', model.name)
    version_ids = [v.version for v in model.versions]
    print('available versions:', version_ids)
    some_version = model.versions[0]
    for input_file in some_version.inputs:
        print('input name:', input_file.name)
    for output_file in some_version.outputs:
        print('input name:', output_file.name)

    model_copy = client.models.get(model)  # from object
    assert model.identifier == model_copy.identifier

    # resync model
    original_name = model.name
    model.name = 'Not My Name'
    model.sync()
    assert model.name == original_name

    # get related models
    related_models = client.models.get_related('ed542963de')
    print('%d related models' % len(related_models))

    # get related models through a model object
    model = client.models.get('ed542963de')
    related_models = model.get_related()
    print('%d related models' % len(related_models))

    # get all tags
    tags = client.tags.get_all()
    print('%d tags' % len(tags))

    # get all tags and models for one or more tags
    tags, models = client.tags.get_tags_and_models('computer_vision')
    print('%d tags and %d models' % (len(tags), len(models)))
    tags, models = client.tags.get_tags_and_models(['computer_vision', 'enhance_or_preprocess'])
    print('%d tags and %d models' % (len(tags), len(models)))

    # submit single inference jobs through a model object
    model = client.models.get('ed542963de')
    job = model.submit_text('0.0.27', {'input.txt': 'it is great'})
    job = model.submit_bytes('0.0.27', {'input.txt': b'it is great'})
    job = model.submit_files('0.0.27', {'input.txt': './input.txt'})
    job = model.submit_files('0.0.27', {'input.txt': pathlib.Path('./input.txt')})
    job = model.submit_files('0.0.27', {'input.txt': open('./input.txt', 'rb')})
    job = model.submit_files('0.0.27', {'input.txt': io.BytesIO(b'it is great')})
    job = model.submit_aws_s3('0.0.27', {'input.txt': {
        'bucket': 'my-data-bucket',
        'key': 'independence-recipes.txt'
    }},
        access_key_id=AWS_ACCESS_KEY_ID,
        secret_access_key=AWS_SECRET_ACCESS_KEY,
        region=AWS_DEFAULT_REGION
    )

    # optionally, specify your own source name for a single inference job through a model object
    model = client.models.get('ed542963de')
    job = model.submit_text('0.0.27', {'input.txt': 'it is great'}, source_name='my-source-1')
    ...

    # submit bulk inference jobs through a model object
    model = client.models.get('ed542963de')
    job = model.submit_text_bulk('0.0.27', {
        'happy': {'input.txt': 'it is great'},
        'sad': {'input.txt': 'it is terrible'}
    })
    job = model.submit_bytes_bulk('0.0.27', {
        'happy': {'input.txt': b'it is great'},
        'sad': {'input.txt': b'it is terrible'}
    })
    job = model.submit_files_bulk('0.0.27', {
        'happy': {'input.txt': './input.txt'},
        'happy2': {'input.txt': open('./input.txt', 'rb')},
        'sad': {'input.txt': pathlib.Path('./input.txt')},
        'sad2': {'input.txt': io.BytesIO(b'it is terrible')}
    })
    job = model.submit_aws_s3_bulk('0.0.27', {
        'happy': {'input.txt': {
            'bucket': 'my-data-bucket',
            'key': 'independence-recipes.txt'
        }},
        'sad': {'input.txt': {
            'bucket': 'my-data-bucket',
            'key': 'independence-recipes.txt'
        }}
    },
        access_key_id=AWS_ACCESS_KEY_ID,
        secret_access_key=AWS_SECRET_ACCESS_KEY,
        region=AWS_DEFAULT_REGION
    )

    # submit single inference jobs with a model id
    job = client.jobs.submit_text('ed542963de', '0.0.27', {'input.txt': 'it is great'})
    job = client.jobs.submit_bytes('ed542963de', '0.0.27', {'input.txt': b'it is great'})
    job = client.jobs.submit_files('ed542963de', '0.0.27', {'input.txt': './input.txt'})
    job = client.jobs.submit_files('ed542963de', '0.0.27', {'input.txt': pathlib.Path('./input.txt')})
    job = client.jobs.submit_files('ed542963de', '0.0.27', {'input.txt': open('./input.txt', 'rb')})
    job = client.jobs.submit_files('ed542963de', '0.0.27', {'input.txt': io.BytesIO(b'it is great')})
    job = client.jobs.submit_aws_s3('ed542963de', '0.0.27', {'input.txt': {
        'bucket': 'my-data-bucket',
        'key': 'independence-recipes.txt'
    }},
        access_key_id=AWS_ACCESS_KEY_ID,
        secret_access_key=AWS_SECRET_ACCESS_KEY,
        region=AWS_DEFAULT_REGION
    )

    # optionally, specify your own source name for a single inference job with a model id
    model = client.models.get('ed542963de')
    job = client.jobs.submit_text('ed542963de', '0.0.27', {'input.txt': 'it is great'}, source_name='my-source-1')
    ...

    # submit bulk inference jobs with a model id
    job = client.jobs.submit_text_bulk('ed542963de', '0.0.27', {
        'source-1': {'input.txt': 'it is great'},
        'source-2': {'input.txt': 'it is terrible'}
    })
    job = client.jobs.submit_bytes_bulk('ed542963de', '0.0.27', {
        'source-1': {'input.txt': b'it is great'},
        'source-2': {'input.txt': b'it is terrible'}
    })
    job = client.jobs.submit_files_bulk('ed542963de', '0.0.27', {
        'source-1': {'input.txt': './input.txt'},
        'source-2': {'input.txt': pathlib.Path('./input.txt')},
        'source-3': {'input.txt': open('./input.txt', 'rb')},
        'source-4': {'input.txt': io.BytesIO(b'it is terrible')}
    })
    job = client.jobs.submit_aws_s3_bulk('ed542963de', '0.0.27', {
        'source-1': {'input.txt': {
            'bucket': 'my-data-bucket',
            'key': 'independence-recipes.txt'
        }},
        'source-2': {'input.txt': {
            'bucket': 'my-data-bucket',
            'key': 'independence-recipes.txt'
        }}
    },
        access_key_id=AWS_ACCESS_KEY_ID,
        secret_access_key=AWS_SECRET_ACCESS_KEY,
        region=AWS_DEFAULT_REGION
    )

    # submit single inference jobs with a model
    model = client.models.get('ed542963de')
    job = client.jobs.submit_text(model, '0.0.27', {'input.txt': 'it is great'})
    job = client.jobs.submit_bytes(model, '0.0.27', {'input.txt': b'it is great'})
    job = client.jobs.submit_files(model, '0.0.27', {'input.txt': './input.txt'})
    job = client.jobs.submit_files(model, '0.0.27', {'input.txt': pathlib.Path('./input.txt')})
    job = client.jobs.submit_files(model, '0.0.27', {'input.txt': open('./input.txt', 'rb')})
    job = client.jobs.submit_files(model, '0.0.27', {'input.txt': io.BytesIO(b'it is great')})
    job = client.jobs.submit_aws_s3(model, '0.0.27', {'input.txt': {
        'bucket': 'my-data-bucket',
        'key': 'independence-recipes.txt'
    }},
        access_key_id=AWS_ACCESS_KEY_ID,
        secret_access_key=AWS_SECRET_ACCESS_KEY,
        region=AWS_DEFAULT_REGION
    )

    # optionally, specify your own source name for a single inference job with a model
    model = client.models.get('ed542963de')
    job = client.jobs.submit_text(model, '0.0.27', {'input.txt': 'it is great'}, source_name='my-source-1')
    ...

    # submit bulk inference jobs with a model
    model = client.models.get('ed542963de')
    job = client.jobs.submit_text_bulk(model, '0.0.27', {
        'source-1': {'input.txt': 'it is great'},
        'source-2': {'input.txt': 'it is terrible'}
    })
    job = client.jobs.submit_bytes_bulk(model, '0.0.27', {
        'source-1': {'input.txt': b'it is great'},
        'source-2': {'input.txt': b'it is terrible'}
    })
    job = client.jobs.submit_files_bulk(model, '0.0.27', {
        'source-1': {'input.txt': './input.txt'},
        'source-2': {'input.txt': pathlib.Path('./input.txt')},
        'source-3': {'input.txt': open('./input.txt', 'rb')},
        'source-4': {'input.txt': io.BytesIO(b'it is terrible')}
    })
    job = client.jobs.submit_aws_s3_bulk(model, '0.0.27', {
        'source-1': {'input.txt': {
            'bucket': 'my-data-bucket',
            'key': 'independence-recipes.txt'
        }},
        'source-2': {'input.txt': {
            'bucket': 'my-data-bucket',
            'key': 'independence-recipes.txt'
        }}
    },
        access_key_id=AWS_ACCESS_KEY_ID,
        secret_access_key=AWS_SECRET_ACCESS_KEY,
        region=AWS_DEFAULT_REGION
    )

    # get job history
    jobs = client.jobs.get_history()
    print('%d jobs' % len(jobs))

    # get single job
    job = client.jobs.submit_text('ed542963de', '0.0.27', {'input.txt': 'it is great'})
    job = client.jobs.get(job.job_identifier)  # by id
    job_copy = client.jobs.get(job)  # by object
    assert job.job_identifier == job_copy.job_identifier

    # sync job object with server-side state
    job = client.jobs.submit_text('ed542963de', '0.0.27', {'input.txt': 'it is great'})
    orig_model = job.model.identifier
    job.model.identifier = 'Not Me'
    job.sync()
    assert job.model.identifier == orig_model

    # (attempt to) cancel a job
    job = client.jobs.submit_text('ed542963de', '0.0.27', {'input.txt': 'it is great'})
    try:
        job.cancel()
    except error.HttpError as ex:  # why does API return 500 here?
        print('job can not be canceled:', ex)
    else:
        print('job was canceled')

    # block until job object complete
    job = client.jobs.submit_text('ed542963de', '0.0.27', {'input.txt': 'it is great'})
    assert job.status != client.jobs.status.COMPLETED
    try:
        timeout = 60
        same_job_obj = job.block_until_complete(timeout=timeout)
    except error.Timeout:
        print('job still not finished after %d seconds' % timeout)
    else:
        assert same_job_obj is job
        assert job.status == client.jobs.status.COMPLETED

    # block until job id is complete
    job = client.jobs.submit_text('ed542963de', '0.0.27', {'input.txt': 'it is great'})
    assert job.status != client.jobs.status.COMPLETED
    try:
        timeout = 60
        new_job_obj = client.jobs.block_until_complete(job.job_identifier, timeout=timeout)  # by id
    except error.Timeout:
        print('job still not finished after %d seconds' % timeout)
    else:
        assert new_job_obj is not job
        assert new_job_obj.status == client.jobs.status.COMPLETED

    job = client.jobs.submit_text('ed542963de', '0.0.27', {'input.txt': 'it is great'})
    assert job.status != client.jobs.status.COMPLETED
    try:
        timeout = 60
        new_job_obj = client.jobs.block_until_complete(job, timeout=timeout)  # by object
    except error.Timeout:
        print('job still not finished after %d seconds' % timeout)
    else:
        assert new_job_obj is not job
        assert new_job_obj.status == client.jobs.status.COMPLETED

    # get result from a job object
    job = client.jobs.submit_text('ed542963de', '0.0.27', {'input.txt': 'it is great'})
    job.block_until_complete(timeout=None)  # you should set a timeout
    result = job.get_result()

    # get result from a job id
    job = client.jobs.submit_text('ed542963de', '0.0.27', {'input.txt': 'it is great'})
    job.block_until_complete(timeout=None)  # you should set a timeout
    result = client.results.get(job.job_identifier)   # by id
    result_copy = client.results.get(job)   # by object
    assert result is not result_copy
    assert result.job_identifier == result_copy.job_identifier

    # block until result for job id are complete
    job = client.jobs.submit_text('ed542963de', '0.0.27', {'input.txt': 'it is great'})
    result = client.results.block_until_complete(job.job_identifier, timeout=None)   # by id, you should set a timeout

    job = client.jobs.submit_text('ed542963de', '0.0.27', {'input.txt': 'it is great'})
    result = client.results.block_until_complete(job, timeout=None)   # by object, you should set a timeout

    # sync result object with server-side state
    job = client.jobs.submit_text('ed542963de', '0.0.27', {'input.txt': 'it is great'})
    result = client.results.block_until_complete(job, timeout=None)  # you should set a timeout

    orig_model = job.model.identifier
    job.model.identifier = 'Not Me'
    job.sync()
    assert job.model.identifier == orig_model

    # get first (or only) outputs from a result
    job = client.jobs.submit_text('ed542963de', '0.0.27', {'input.txt': 'it is great'})
    result = client.results.block_until_complete(job, timeout=None)  # you should set a timeout
    try:
        outputs = result.get_first_outputs()
    except error.ResultsError as ex:
        print('the model run failed:', ex)  # should not hit here
    else:
        results_json = outputs['results.json']
        print(json.dumps(results_json))

    # get named outputs from a result
    job = client.jobs.submit_text('ed542963de', '0.0.27', {'input.txt': 'it is great'}, source_name='my-name')
    result = client.results.block_until_complete(job, timeout=None)  # you should set a timeout
    try:
        outputs = result.get_source_outputs('my-name')
    except error.ResultsError as ex:
        print('the model run failed:', ex)  # should not hit here
    else:
        results_json = outputs['results.json']
        print(json.dumps(results_json))

    # handle result failures
    job = client.jobs.submit_bytes('ed542963de', '0.0.27', {'input.txt': b'invalid utf-8:\xf0\x28\x8c\xbc'})
    result = client.results.block_until_complete(job, timeout=None)  # you should set a timeout
    try:
        outputs = result.get_first_outputs()
    except error.ResultsError as ex:
        print('the model run failed:', ex)  # should hit here
    else:
        results_json = outputs['results.json']
        print(json.dumps(results_json))
