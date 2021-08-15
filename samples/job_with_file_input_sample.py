import json
import pathlib
import sys
import os
import logging
import dotenv

from modzy.error import ResultsError
from modzy.jobs import Jobs

sys.path.insert(0, '..')
from modzy import ApiClient
from modzy._util import file_to_bytes


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

# Create a Job with a file input, wait, and retrieve results:

# Get the model object:
# If you already know the model identifier (i.e.: you got it from the URL of the model details page or from the input sample),
# you can skip this step. If you don't, you can find the model identifier by using its name as follows:
model = client.models.get_by_name("Multi-Language OCR")
# Or if you already know the model id and want to know more about the model, you can use this instead:
# model = client.models.get("c60c8dbd79")
# You can find more information about how to query the models on the model_sample.py file.

# The model identifier is under the modelId key. You can take a look at the other keys by uncommenting the following line
# logger.info(", ".join("{} :: {}".format(key, value) for key, value in model.items()))
# Or just log the model identifier and the latest version
logger.info("The model identifier is {} and the latest version is {}".format(model.modelId, model.latest_version))

# Get the model version object:
# If you already know the model version and the input key(s) of the model version you can skip this step. Also, you can
# use the following code block to know about the inputs keys and skip the call on future job submissions.
modelVersion = client.models.get_version(model, model.latest_version)
# The info stored in modelVersion provides insights about the amount of time that the model can spend processing,
# the inputs, and output keys of the model.
logger.info("This model version is {}".format(modelVersion))
logger.info("  timeouts: status {}ms, run {}ms ".format(modelVersion.timeout.status, modelVersion.timeout.run))
logger.info("  inputs: ")
for input in modelVersion.inputs:
    logger.info("    key {}, type {}, description: {}".format(input.name, input.acceptedMediaTypes, input.description))
logger.info("  outputs: ")
for output in modelVersion.outputs:
    logger.info("    key {}, type {}, description: {}".format(output.name, output.mediaType, output.description))

# Send the job:
# A file input can be a byte array or any file path. This input type fits for any size files.
image_path = pathlib.Path('./samples/image.png')
config_path = pathlib.Path('./samples/config.json')
# With the info about the model (identifier), the model version (version string, input/output keys), you are ready to
# submit the job. Just prepare the source dictionary:
sources = {"source-key": {"input": image_path.resolve(), "config.json": config_path.resolve()}}
# An inference job groups input data that you send to a model. You can send any amount of inputs to
# process and you can identify and refer to a specific input by the key that you assign, for example we can add:
sources["second-key"] = {"input": image_path, "config.json": config_path}
# You don't need to load all the inputs from files, you can just convert the files to bytes as follows:
image_bytes = file_to_bytes(image_path.resolve())
config_bytes = json.dumps({"languages":["spa"]}).encode('utf-8')
sources["another-key"] = {"input": image_bytes, "config.json": config_bytes}
# If you send a wrong input key, the model fails to process the input.
sources["wrong-key"] = {"a.wrong.key": image_bytes, "config.json":config_bytes}
# If you send a correct input key but some wrong values, the model fails too.
sources["wrong-value"] = {"input": config_bytes, "config.json":image_bytes}
# When you have all your inputs ready, you can use our helper method to submit the job as follows:
job = client.jobs.submit_file(model.modelId, modelVersion.version, sources)
# Modzy creates the job and queue for processing. The job object contains all the info that you need to keep track
# of the process, the most important being the job identifier and the job status.
logger.info("job: %s", job)
# The job moves to SUBMITTED, meaning that Modzy acknowledged the job and sent it to the queue to be processed.
# We provide a helper method to listen until the job finishes processing. Its a good practice to set a max timeout
# if you're doing a test (ie: 2*status+run). Otherwise, if the timeout is set to None, it will listen until the job
# finishes and moves to COMPLETED, CANCELED, or TIMEOUT.
job.block_until_complete(timeout=None)

# Get the results:
# Check the status of the job. Jobs may be canceled or may reach a timeout.
if job.status == Jobs.status.COMPLETED:
    # A completed job means that all the inputs were processed by the model. Check the results for each
    # input key provided in the source dictionary to see the model output.
    result = job.get_result()
    # The result object has some useful info:
    logger.info("Result: finished: {}, total: {}, completed: {}, failed: {}"
                .format(result.finished, result.total, result.completed, result.failed))
    # Notice that we are iterating through the same input source keys
    for key in sources:
        # The result object has the individual results of each job input. In this case the output key is called
        # results.json, so we can get the results as follows:
        try:
            model_res = result.get_source_outputs(key)['results.json']
            # The output for this model comes in a JSON format, so we can directly log the model results:
            logger.info(
                "    {}: ".format(key) + ", ".join(
                    "{}: {}".format(key, str(value).replace('\n', '')) for key, value in model_res.items()))
        except ResultsError as failure:
            # If the model raises an error, we can get the specific error message:
            logger.warning("    {}: failure: {}".format(key, failure));

else:
    logger.warning("The job ends with status {}".format(job))
