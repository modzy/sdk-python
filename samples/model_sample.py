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
# You can config those params as is described in the readme file (as environment variables, or by using the .env file),
# or you can just set BASE_URL and API_KEY vars on this sample code (not recommended for production environments).

dotenv.load_dotenv()

# The MODZY_BASE_URL should point to the API services route, it may be different from the Modzy page URL.
# (ie: https://modzy.example.com/api).
BASE_URL = os.getenv('MODZY_BASE_URL')
# The MODZY_API_KEY is your own personal API key. It is composed by a public part, a dot character and a private part
# (ie: AzQBJ3h4B1z60xNmhAJF.uQyQh8putLIRDi1nOldh).
API_KEY = os.getenv('MODZY_API_KEY')

# Client initialization
#   Initialize the ApiClient instance with the BASE_URL and the API_KEY to store those arguments
#   for the following API calls.
client = ApiClient(base_url=BASE_URL, api_key=API_KEY)

# Get all models
# You can get the full list of models from Modzy by using get_all method, this call will return just the identifier
# and the latest version of each model
models = client.models.get_all()
logger.info("all models: %s", len(models))
# Also, you can do more interesting search by the get_models method:
# Search by author
params = {'author': 'Open Source'}
models = client.models.get_models(**params)
logger.info("Open Source models: %s", len(models))
# Active models
params = {'is_active': True}
models = client.models.get_models(**params)
logger.info("Active models: %s", len(models))
# Search by name (and limiting the results)
params = {'name': "Image", 'per_page':5}
models = client.models.get_models(**params)
logger.info("Models with name start with 'Image': %s", len(models))
# Combined search
params = {'name': "Image", 'author': 'Open Source', 'is_active': True}
models = client.models.get_models(**params)
logger.info("Active open source models which name starts with 'Image': %s", len(models))
# Get model details
# the models route didn't return much info about the models, just modelId, latestVersion and versions:
for model in models:
    logger.info(", ".join("{} :: {}".format(key, value) for key, value in model.items()))
    # In order to get more info about the models you need to get the details by identifier
    model = client.models.get(model.modelId)
    # then you'll get all the details about the model
    logger.info("Model detail keys: %s", model.keys())
    # In order to get information about the input/output keys and types you need to get the model version details as
    # follows:
    modelVersion = client.models.get_version(model, model.latestVersion)
    # then you'll get all the details about the specific model version
    logger.info("Model Version detail keys: %s", model.keys())
    # Probably the more interesting are the ones related with the inputs and outputs of the model
    logger.info("  inputs: ")
    for input in modelVersion.inputs:
        logger.info(
            "    key {}, type {}, description: {}".format(input.name, input.acceptedMediaTypes, input.description))
    logger.info("  outputs: ")
    for output in modelVersion.outputs:
        logger.info("    key {}, type {}, description: {}".format(output.name, output.mediaType, output.description.replace('\n', '')))

# Get model by name
# If you aren't familiar with the models ids, you can find the model by name as follows
model = client.models.get_by_name("Dataset Joining")
# the method will return the first coincidence and return the details
logger.info("Dataset Joining: id:%s, author: %s, is_active: %s, description: %s",
            model.modelId, model.author, model.is_active, model.description)
# Finally, you can find the models related with this search
models = client.models.get_related(model.modelId)
logger.info("related models")
for model in models:
    logger.info("    %s :: %s (%s)", model.modelId, model.name, model.author)


