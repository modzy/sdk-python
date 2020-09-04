import sys
import os
import logging
import dotenv
sys.path.insert(0, '..')
from modzy import ApiClient


# Always configure the logger level (ie: DEBUG, INFO, WARNING, ERROR, CRITICAL)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# The system admin can provide the right base API URL, the API key can be downloaded from your profile page on Modzy.
# You can configure those params as is described in the README file (as environment variables, or by using the .env file),
# or you can just update the BASE_URL and API_KEY variables and use this sample code (not recommended for production environments).

dotenv.load_dotenv()

# The MODZY_BASE_URL should point to the API services route which may be different from the Modzy page URL.
# (ie: https://modzy.example.com/api).
BASE_URL = os.getenv('MODZY_BASE_URL')
# The MODZY_API_KEY is your own personal API key. It is composed by a public part, a dot character, and a private part
# (ie: AzQBJ3h4B1z60xNmhAJF.uQyQh8putLIRDi1nOldh).
API_KEY = os.getenv('MODZY_API_KEY')

# Client initialization:
#   Initialize the ApiClient instance with the BASE_URL and the API_KEY to store those arguments
#   for the following API calls.
client = ApiClient(base_url=BASE_URL, api_key=API_KEY)

# Create a Job with a text input, wait, and retrieve results:

# Get all models:
# You can get the full list of models from Modzy by using the get_all method to retrieve the identifier
# and the latest version of each model
models = client.models.get_all()
logger.info("all models: %s", len(models))
# Also, use the get_models method to search for specific models:
# Search by author:
params = {'author': 'Open Source'}
models = client.models.get_models(**params)
logger.info("Open Source models: %s", len(models))
# Search for active models:
params = {'is_active': True}
models = client.models.get_models(**params)
logger.info("Active models: %s", len(models))
# Search by name (and paginate the results):
params = {'name': "Image", 'per_page':5}
models = client.models.get_models(**params)
logger.info("Models with name start with 'Image': %s", len(models))
# Combined search:
params = {'name': "Image", 'author': 'Open Source', 'is_active': True}
models = client.models.get_models(**params)
logger.info("Active open source models which name starts with 'Image': %s", len(models))

# Get model details:
# The models route only returns the modelId, latestVersion, and versions:
for model in models:
    logger.info(", ".join("{} :: {}".format(key, value) for key, value in model.items()))
    # Use the model identifier to get model details
    model = client.models.get(model.modelId)
    # get model keys
    logger.info("Model detail keys: %s", model.keys())
    # use the version identifier to get version details such as input and output details
    modelVersion = client.models.get_version(model, model.latestVersion)
    logger.info("Model Version detail keys: %s", model.keys())
    # get inputs and outputs
    logger.info("  inputs: ")
    for input in modelVersion.inputs:
        logger.info(
            "    key {}, type {}, description: {}".format(input.name, input.acceptedMediaTypes, input.description))
    logger.info("  outputs: ")
    for output in modelVersion.outputs:
        logger.info("    key {}, type {}, description: {}".format(output.name, output.mediaType, output.description.replace('\n', '')))

# Get model by name:
# You can also find models by name
model = client.models.get_by_name("Dataset Joining")
# this method returns the first matching model and its details
logger.info("Dataset Joining: id:%s, author: %s, is_active: %s, description: %s",
            model.modelId, model.author, model.is_active, model.description)

# Finally, you can find related models related with this search:
models = client.models.get_related(model.modelId)
logger.info("related models")
for model in models:
    logger.info("    %s :: %s (%s)", model.modelId, model.name, model.author)


