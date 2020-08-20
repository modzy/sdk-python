import sys
import os
import logging
import dotenv
sys.path.insert(0, '..')
from modzy import ApiClient


# Basic configuration of logger (level setted in debug)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# dotenv variables

dotenv.load_dotenv()

BASE_URL = os.getenv('MODZY_BASE_URL')
API_KEY = os.getenv('MODZY_API_KEY')

# Client initialization
# TODO: set the base url of modzy api and you api key
client = ApiClient(base_url=BASE_URL, api_key=API_KEY)

# Create a Job with a text input, wait and retrieve results

model = client.models.get_by_name("Facial Embedding")
logger.info("Model {}".format(model))

modelVersion = client.models.get_version(model, model.latest_version)
logger.info("ModelVersion {}".format(modelVersion))

job = client.jobs.submit_aws_s3(model.modelId, modelVersion.version, {'image': {
        'bucket': 'the-bucket',
        'key': '/the/path/to/the/input_image.png'
    }},
        access_key_id='MyAccessKeyID',
        secret_access_key='MySecretAccessKey',
        region='us-east-1',
    ) # Facial Embedding

logger.info("job: %s", job)

job.block_until_complete(timeout=None)
logger.info("job: %s", job)

result = job.get_result()
logger.info("result: %s", result)

results_json = result.get_first_outputs()['results.json']
logger.info("results_json: %s", results_json)

# Create a job with more than one input

job = client.jobs.submit_aws_s3_bulk(model.modelId, modelVersion.version, {
        'image-1': {'image': {
                'bucket': 'the-bucket',
                'key': '/the/path/to/the/input_image_1.png'
            }
        },
        'other-id': {'image': {
                'bucket': 'the-bucket',
                'key': '/the/path/to/the/input_image_2.png'
            }
        }},
        access_key_id='MyAccessKeyID',
        secret_access_key='MySecretAccessKey',
        region='us-east-1',
)
logger.info("job: %s", job)

job.block_until_complete(timeout=None)
logger.info("job: %s", job)

result = job.get_result()
logger.info("result: %s", result)

results_json = result.get_first_outputs()['results.json']
logger.info("results_json: %s", results_json)
