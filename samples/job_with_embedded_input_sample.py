import sys
import os
import logging
import dotenv
sys.path.insert(0, '..')
from modzy import ApiClient
from modzy._util import file_to_bytes


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
image_bytes = file_to_bytes('../samples/image.png')

model = client.models.get_by_name("NSFW Image Detection")
logger.info("Model {}".format(model))

modelVersion = client.models.get_version(model, model.latest_version)
logger.info("ModelVersion {}".format(modelVersion))

job = client.jobs.submit_bytes(model.modelId, modelVersion.version, {'image': image_bytes})
logger.info("job: %s", job)

job.block_until_complete(timeout=None)
logger.info("job: %s", job)

result = job.get_result()
logger.info("result: %s", result)

results_json = result.get_first_outputs()['results.json']
logger.info("results_json: %s", results_json)

# Create a job with more than one input

job = client.jobs.submit_bytes_bulk(model.modelId, modelVersion.version, {
        'image-1': {'image': image_bytes},
        'other-id': {'image': image_bytes},
})

logger.info("job: %s", job)

job.block_until_complete(timeout=None)
logger.info("job: %s", job)

result = job.get_result()
logger.info("result: %s", result)

results_json = result.get_first_outputs()['results.json']
logger.info("results_json: %s", results_json)
