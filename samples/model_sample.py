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

client = ApiClient(base_url=BASE_URL, api_key=API_KEY)

# Get all models

models = client.models.get_all()

logger.info("all models: %s", len(models))
for model in models:
    logger.info(", ".join("{} :: {}".format(key, value) for key, value in model.items()))


# Get model by identifier
logger.info("model by id ed542963de")
model = client.models.get('ed542963de')  # sentiment-analysis
logger.info("When you get the model by id, you get the following model keys: %s", model.keys())


# Get related models

logger.info("related models by id ed542963de")
models = client.models.get_related('ed542963de')
for model in models:
    logger.info("related model %s", model)

# Get versions of a model

versions = client.models.get_versions('ed542963de')
for version in versions:
    logger.info("version %s", version)


