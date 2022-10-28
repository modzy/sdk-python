# -*- coding: utf-8 -*-
import json
import pathlib
import time
from .error import NetworkError, InternalServerError
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from base64 import b64encode

def encode_data_uri(bytes_like, mimetype='application/octet-stream'):
    encoded = b64encode(bytes_like).decode('ascii')
    data_uri = 'data:{};base64,{}'.format(mimetype, encoded)
    return data_uri

def file_to_bytes(file_like):
    if hasattr(file_like, 'read'):  # File-like object
        if hasattr(file_like, 'seekable') and file_like.seekable():
            file_like.seek(0)
        maybe_bytes = file_like.read()
        if not isinstance(maybe_bytes, bytes):
            raise TypeError("the file object's 'read' function must return bytes not {}; "
                            "files should be opened using binary mode 'rb'"
                            .format(type(maybe_bytes).__name__))
        return maybe_bytes

    # should we just pass the object directly to `open` instead of trying to find the path ourselves?
    # would break pathlib.Path support on Python<3.6, but would be consistent with the Python version...
    if hasattr(file_like, '__fspath__'):  # os.PathLike
        path = file_like.__fspath__()
    elif isinstance(file_like, pathlib.Path):  # Python 3.4-3.5
        path = str(file_like)
    else:
        path = file_like

    with open(path, 'rb') as file:
        return file.read()

def file_to_chunks(file_like, chunk_size):
    file = None
    should_close = False
    if not hasattr(file_like, 'read'):
        if hasattr(file_like, '__fspath__'):  # os.PathLike
            path = file_like.__fspath__()
        elif isinstance(file_like, pathlib.Path):  # Python 3.4-3.5
            path = str(file_like)
        else:
            path = file_like
        file = open(path, 'rb')
        should_close = True
    else:
        file = file_like

    if hasattr(file, 'seekable') and file.seekable():
        file.seek(0)

    while True:
        chunk = file.read(chunk_size)
        if not chunk:
            break
        elif not isinstance(chunk, bytes):
            raise TypeError("the file object's 'read' function must return bytes not {}; "
                            "files should be opened using binary mode 'rb'"
                            .format(type(chunk).__name__))
        else:
            yield chunk

    if should_close:
        file.close()

def bytes_to_chunks(byte_array, chunk_size):
    for i in range(0, len(byte_array), chunk_size):
        yield byte_array[i:i + chunk_size]

def depth(d):
    if d and isinstance(d, dict):
        return max(depth(v) for k, v in d.items()) + 1
    return 0

'''
Model Deployment (models.deploy()) specific utilities
'''
def load_model(client, logger, identifier, version):

    start = time.time()
    # Before loading the model we need to ensure that it has been pulled.
    percentage = -1
    while percentage < 100:
        try:
            res = client.http.get(f"/models/{identifier}/versions/{version}/container-image")
            new_percentage = res.get("percentage")
        except NetworkError:
            continue      
        except InternalServerError:
            continue      

        if new_percentage != percentage:
            logger.info(f'Loading model at {new_percentage}%')
            print(f'Loading model at {new_percentage}%')
            percentage = new_percentage

        time.sleep(1)

    retry_strategy = Retry(
        total=10,
        backoff_factor=0.3,
        status_forcelist=[400],
        allowed_methods=frozenset(['POST']),
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    client.http.session.mount('https://', adapter)

    try:
        res = client.http.post(f"/models/{identifier}/versions/{version}/load-process")
    except NetworkError:
        return      
    except InternalServerError:
        return          

    logger.info(f'Loading container image took [{1000*(time.time()-start)} ms]')

def upload_input_example(client, logger, identifier, version, model_data_metadata, input_sample_path):

    start = time.time()

    input_filename = model_data_metadata['inputs'][0]['name']
    files = {'file': open(input_sample_path, 'rb')}
    params = {'name': input_filename}
    res = client.http.post(f"/models/{identifier}/versions/{version}/testInput", params=params, file_data=files)

    logger.info(f'Uploading sample input took [{1000*(time.time()-start)} ms]')

def run_model(client, logger, identifier, version):

    start = time.time()
    res = client.http.post(f"/models/{identifier}/versions/{version}/run-process")

    percentage = -1
    while percentage < 100:
        try:
            res = client.http.get(f"/models/{identifier}/versions/{version}/run-process")
            new_percentage = res.get('percentage')
        except NetworkError:
            continue

        if new_percentage != percentage:
            logger.info(f'Running model at {new_percentage}%')
            print(f'Running model at {new_percentage}%')
            percentage = new_percentage

        time.sleep(1)

    test_output = res['result']
    # perform validation check on test_output and raise error if error exists
    if test_output["status"] == "FAILED":
        raise ValueError(f'Sample inference test failed with error {test_output["error"]}. Check model container and try again.')

    sample_input = {'input': {'accessKeyID': '<accessKeyID>',
                                    'region': '<region>',
                                    'secretAccessKey': '<secretAccessKey>',
                                    'sources': {'0001': {'input': {'bucket': '<bucket>',
                                                        'key': '/path/to/s3/input'}}},
                                                        'type': 'aws-s3'},
                                'model': {'identifier': identifier, 'version':version}
                    }
    
    formatted_sample_output = {'jobIdentifier': '<uuid>',
                                'total': '<number of inputs>',
                                'completed': '<total number of completed inputs>',
                                'failed': '<number of failed inputs>',
                                'finished': '<true or false>',
                                'submittedByKey': '<api key>',
                                'results': {'<input-id>': {'model': None,
                                'userIdentifier': None,
                                'status': test_output['status'],
                                'engine': test_output['engine'],
                                'error': test_output['error'],
                                'startTime': test_output['startTime'],
                                'endTime': test_output['endTime'],
                                'updateTime': test_output['updateTime'],
                                'inputSize': test_output['inputSize'],
                                'accessKey': None,
                                'teamIdentifier': None,
                                'accountIdentifier': None,
                                'timeMeters': None,
                                'datasourceCompletedTime': None,
                                'elapsedTime': test_output['elapsedTime'],
                                'results.json': test_output['results.json']}
                                }
                            }

    sample_input_res = client.http.put(f"/models/{identifier}/versions/{version}/sample-input", json_data=sample_input)
    sample_output_res = client.http.put(f"/models/{identifier}/versions/{version}/sample-output", json_data=formatted_sample_output)

    logger.info(f'Inference test took [{1000*(time.time()-start)} ms]')

def deploy_model(client, logger, identifier, version):

    start = time.time()
    status = {'status': 'active'}

    res = client.http.patch(f"/models/{identifier}/versions/{version}", status)

    logger.info(f'Model Deployment took [{1000*(time.time()-start)} ms]')

