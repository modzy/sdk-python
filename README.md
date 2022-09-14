<div align="center">

![GitHub contributors](https://img.shields.io/github/contributors/modzy/sdk-python?logo=GitHub&style=flat-square)
![GitHub last commit](https://img.shields.io/github/last-commit/modzy/sdk-python?logo=GitHub&style=flat-square)
![GitHub issues](https://img.shields.io/github/issues-raw/modzy/sdk-python?logo=github&style=flat-square)
![GitHub](https://img.shields.io/github/license/modzy/sdk-python?logo=apache&style=flat-square)

![PyPI](https://img.shields.io/pypi/v/modzy-sdk?logo=pypi&style=flat-square)
![PyPI - Downloads](https://img.shields.io/pypi/dm/modzy-sdk?logo=pypi&style=flat-square)

**[Python SDK Documentation Page](https://docs.modzy.com)**

![Modzy Python SDK Banner](https://github.com/modzy/sdk-python/blob/main/python-sdk-github-banner.png)

</div>

# Installation

Install Modzy's Python SDK with PIP

```bash
  pip install modzy-sdk
```
    
# Usage/Examples

## Initializing the SDK
Initialize your client by authenticating with an API key. You can [download an API Key](https://docs.modzy.com/docs/view-and-manage-api-keys#download-team-api-key) from your instance of Modzy.

```python
from modzy import ApiClient

# Sets BASE_URL and API_KEY values
# Best to set these as environment variables
BASE_URL = "Valid Modzy URL" # e.g., "https://trial.modzy.com"
API_KEY = "Valid Modzy API Key" # e.g., "JbFkWZMx4Ea3epIrxSgA.a2fR36fZi3sdFPoztAXT"

client = ApiClient(base_url=BASE_URL, api_key=API_KEY)
```
## Running Inferences
### Raw Text Inputs
Submit an inference job to a text-based model by providing the model ID, version, and raw input text:

```python
# Creates a dictionary for text input(s)
sources = {}

# Adds any number of inputs
sources["first-phone-call"] = {
    "input.txt": "Mr Watson, come here. I want to see you.",
}

# Submit the text to v1.0.1 of a Sentiment Analysis model, and to make the job explainable, change explain=True
job = client.jobs.submit_text("ed542963de", "1.0.1", sources, explain=False)
```
### File inputs
Pass a file from your local directory to a model by providing the model ID, version, and the filepath of your sample data:

```python
# Generate a mapping of your local file (nyc-skyline.jpg) to the input filename the model expects
sources = {"nyc-skyline": {"image": "./images/nyc-skyline.jpg"}}

# Submit the image to v1.0.1 of an Image-based Geolocation model
job = client.jobs.submit_file("aevbu1h3yw", "1.0.1", sources)
```
### Embedded inputs
Convert images and other large inputs to base64 embedded data and submit to a model by providing a model ID, version number, and dictionary with one or more base64 encoded inputs:
```python
from modzy._util import file_to_bytes

# Embed input as a string in base64
image_bytes = file_to_bytes('./images/tower-bridge.jpg')
# Prepare the source dictionary
sources = {"tower-bridge": {"image": image_bytes}}

# Submit the image to v1.0.1 of an Imaged-based Geolocation model
job = client.jobs.submit_embedded("aevbu1h3yw", "1.0.1", sources)
```
### Inputs from databases
Submit data from a SQL database to a model by providing a model ID, version, a SQL query, and database connection credentials:
```python
# Add database connection and query information
db_url = "jdbc:postgresql://db.bit.io:5432/bitdotio"
db_username = DB_USER_NAME
db_password = DB_PASSWORD
db_driver = "org.postgresql.Driver"
# Select as "input.txt" becase that is the required input name for this model
db_query = "SELECT \"mailaddr\" as \"input.txt\" FROM \"user/demo_repo\".\"atl_parcel_attr\" LIMIT 10;"

# Submit the database query to v0.0.12 of a Named Entity Recognition model
job = client.jobs.submit_jdbc("a92fc413b5","0.0.12",db_url, db_username, db_password, db_driver, db_query)
```
### Inputs from Cloud Storage
Submit data directly from your cloud storage bucket (Amazon S3, Azure Blob, NetApp StorageGrid supported) by providing a model ID, version, and storage-blob-specific parameters.

#### AWS S3
```python
# Define sources dictionary with bucket and key that points to the correct file in your s3 bucket
sources = {
  "first-amazon-review": {
    "input.txt": {
      "bucket": "s3-bucket-name",
      "key": "key-to-file.txt"
    }
  }
}

AWS_ACCESS_KEY = "aws-acces-key"
AWC_SECRET_ACCESS_KEY = "aws-secret-access-key"
AWS_REGION = "us-east-1"

# Submit s3 input to v1.0.1 of a Sentiment Analysis model
job = client.jobs.submit_aws_s3("ed542963de", "1.0.1", sources, AWS_ACCESS_KEY, AWS_SECRET_ACCESS_KEY, AWS_REGION)
```

#### Azure Blob
```python
# Define sources dictionary with container name and filepath that points to the correct file in your Azure Blob container
sources = {
  "first-amazon-review": {
    "input.txt": {
      "container": "azure-blob-container-name",
      "filePath": "key-to-file.txt"
    }
  }
}

AZURE_STORAGE_ACCOUNT = "Azure-Storage-Account"
AZURE_STORAGE_ACCOUNT_KEY = "cvx....ytw=="

# Submit Azure Blob input to v1.0.1 of a Sentiment Analysis model
job = client.jobs.submit_azure_blob("ed542963de", "1.0.1", sources, AZURE_STORAGE_ACCOUNT, AZURE_STORAGE_ACCOUNT_KEY)
```

#### NetApp StorageGRID
```python
# Define sources dictionary with bucket name and key that points to the correct file in your NetApp StorageGRID bucket
sources = {
  "first-amazon-review": {
    "input.txt": {
      "bucket": "bucket-name",
      "key": "key-to-file.txt"
    }
  }
}

ACCESS_KEY = "access-key"
SECRET_ACCESS_KEY = "secret-access-key"
STORAGE_GRID_ENDPOINT = "https://endpoint.storage-grid.example"

# Submit StorageGRID input to v1.0.1 of a Sentiment Analysis model
job = client.jobs.submit_storagegrid("ed542963de", "1.0.1", sources, ACCESS_KEY, SECRET_ACCESS_KEY, STORAGE_GRID_ENDPOINT)
```
## Getting Results
Modzy's APIs are asynchronous by nature, which means you can use the `results` API to query available results for all completed inference jobs at any point in time. There are two ways you might leverage this Python SDK to query results:

### Block Job until it completes 
This method provides a mechanism to mimic a sycnchronous API by using two different APIs subsequently and a utility function.

```python
# Define sources dictionary with input data
sources = {"my-input": {"input.txt": "Today is a beautiful day!"}}
# Submit the text to v1.0.1 of a Sentiment Analysis model, and to make the job explainable, change explain=True
job = client.jobs.submit_text("ed542963de", "1.0.1", sources, explain=False)
# Use block until complete method to periodically ping the results API until job completes
results = client.results.block_until_complete(job, timeout=None, poll_interval=5)
```

### Query a Job's Result 
This method simply queries the results for a job at any point in time and returns the status of the job, which includes the results if the job has completed.

```python
#  Query results for a job at any point in time
results = client.results.get(job)
```
## Deploying Models
Deploy a model to a your private model library in Modzy

```Python
from modzy import ApiClient

# Sets BASE_URL and API_KEY values
# Best to set these as environment variables
BASE_URL = "Valid Modzy URL" # e.g., "https://trial.modzy.com"
API_KEY = "Valid Modzy API Key" # e.g., "JbFkWZMx4Ea3epIrxSgA.a2fR36fZi3sdFPoztAXT"

client = ApiClient(base_url=BASE_URL, api_key=API_KEY)

model_data = client.models.deploy(
    container_image="modzy/grpc-echo-model:1.0.0",
    model_name="Echo Model",
    model_version="0.0.1",
    sample_input_file="./test.txt",
    run_timeout="60",
    status_timeout="60",
    short_description="This model returns the same text passed through as input, similar to an 'echo.'",
    long_description="This model returns the same text passed through as input, similar to an 'echo.'",
    technical_details="This section can include any technical information abot your model. Include information about how your model was trained, any underlying architecture details, or other pertinant information an end-user would benefit from learning.",
    performance_summary="This is the performance summary."
)

print(model_data)
```
To use **`client.models.deploy()`** there are 4 fields that are required:
* `container_image (str)`: This parameter must represent a container image repository & tag name, or in other words, the string you would include after a docker pull command. For example, if you were to download this container image using docker pull modzy/grpc-echo-model:1.0.0, include just modzy/grpc-echo-model:1.0.0 for this parameter
* `model_name`: The name of your model you would like to deploy
* `model_version`: The version of your model you would like to deploy
* `sample_input_file`: Filepath to a sample piece of data that your model is expected to process and perform inference against.

## Running Inferences at the Edge

The SDK provides support for running inferences on edge devices through Modzy's Edge Client. The inference workflow is almost identical to the previously outlined workflow:

### Initialize *Edge* Client

```python
from modzy.edge.client import EdgeClient

# initialize edge client
client = EdgeClient('localhost',55000)
```

### Submit Inference Job
All input types defined above are supported on Modzy Edge.

```python
# Submit text job to Sentiment Analysis model deployed on edge device by providing a model ID, version, and raw text data, wait for completion
job = client.submit_text("ed542963de","1.0.27",{"input.txt": "this is awesome"})
# Block until results are ready
final_job_details = client.block_until_complete(job)
results = client.get_results(job)
```

### Query Details about Edge Jobs
```python
# get job details for a particular job
job_details = client.get_job_details(job)

# get job details for all jobs run on your Modzy Edge instance
all_job_details = client.get_all_job_details()
```

# SDK Code Examples

View examples of practical workflows:

* [Image-Based Geolocation Inference Notebook](https://github.com/modzy/modzy-jupyter-notebook-samples/blob/main/python-sdk-inference/Submitting%20Jobs%20with%20Python%20SDK%20-%20Image-Based%20Geolocation.ipynb)
* [Automobile Classification Inference Notebook with Explainability](https://github.com/modzy/modzy-jupyter-notebook-samples/blob/main/python-sdk-inference/Submitting%20Jobs%20with%20Python%20SDK%20-%20Automobile%20Classification.ipynb)
* [Batch Inference with Sentiment Analysis](https://github.com/modzy/modzy-jupyter-notebook-samples/blob/main/python-sdk-inference/Submitting%20Batch%20Jobs%20with%20Python%20SDK%20-%20Sentiment%20Analysis.ipynb)

# Documentation

Modzy's SDK is built on top of the [Modzy HTTP/REST API](https://docs.modzy.com/reference/introduction). For a full list of features and supported routes visit [Python SDK on docs.modzy.com](https://docs.modzy.com/docs/python)

# API Reference

| Feature | Code |Api route
| ---     | ---  | ---
|Deploy new model|client.models.deploy()|[api/models](https://docs.modzy.com/reference/model-deployment)
|Get all models|client.models.get_all()|[api/models](https://docs.modzy.com/reference/get-all-models)|
|List models|client.models.get_models()|[api/models](https://docs.modzy.com/reference/list-models)|
|Get model details|client.models.get()|[api/models/:model-id](https://docs.modzy.com/reference/list-model-details)|
|List models by name|client.models.get_by_name()|[api/models](https://docs.modzy.com/reference/list-models)|
|List models by tag|client.tags.get_tags_and_models()|[api/models/tags/:tag-id](https://docs.modzy.com/reference/list-models-by-tag) |
|Get related models|client.models.get_related()|[api/models/:model-id/related-models](https://docs.modzy.com/reference/get-related-models)|
|List a model's versions|client.models.get_versions()|[api/models/:model-id/versions](https://docs.modzy.com/reference/list-versions)|
|Get a version's details|client.models.get_version()|[api/models/:model-id/versions/:version-id](https://docs.modzy.com/reference/get-version-details)|
|Update processing engines|client.models.update_processing_engines()|[api/resource/models](https://docs.modzy.com/reference/update-a-version-1)|
|Get minimum engines|client.models.get_minimum_engines()|[api/models/processing-engines](https://docs.modzy.com/reference/get-minimum-engines)|
|List tags|client.tags.get_all()|[api/models/tags](https://docs.modzy.com/reference/list-tags)|
|Submit a Job (Text)|client.jobs.submit_text()|[api/jobs](https://docs.modzy.com/reference/create-a-job-1)|
|Submit a Job (Embedded)|client.jobs.submit_embedded()|[api/jobs](https://docs.modzy.com/reference/create-a-job-1)|
|Submit a Job (File)|client.jobs.submit_file()|[api/jobs](https://docs.modzy.com/reference/create-a-job-1)|
|Submit a Job (AWS S3)|client.jobs.submit_aws_s3()|[api/jobs](https://docs.modzy.com/reference/create-a-job-1)|
|Submit a Job (JDBC)|client.jobs.submit_jdbc()|[api/jobs](https://docs.modzy.com/reference/create-a-job-1)|
|Cancel job|job.cancel()|[api/jobs/:job-id](https://docs.modzy.com/reference/cancel-a-job)  |
|Hold until inference is complete|job.block_until_complete()|[api/jobs/:job-id](https://docs.modzy.com/reference/get-job-details)  |
|Get job details|client.jobs.get()|[api/jobs/:job-id](https://docs.modzy.com/reference/get-job-details)  |
|Get results|job.get_result()|[api/results/:job-id](https://docs.modzy.com/reference/get-results)  |
|Get the job history|client.jobs.get_history()|[api/jobs/history](https://docs.modzy.com/reference/list-the-job-history)  |

# Support

For support, email opensource@modzy.com or join our [Slack](https://www.modzy.com/slack).
# Contributing

Contributions are always welcome!

See [`contributing.md`](https://github.com/modzy/sdk-python/tree/main/contributing.adoc) for ways to get started.

Please adhere to this project's `code of conduct`.

We are happy to receive contributions from all of our users. Check out our contributing file to learn more.

[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-v2.0%20adopted-ff69b4.svg)](https://github.com/modzy/sdk-python/tree/main/CODE_OF_CONDUCT.md)
