![GitHub contributors](https://img.shields.io/github/contributors/modzy/sdk-python?logo=GitHub&style=flat-square)
![GitHub last commit](https://img.shields.io/github/last-commit/modzy/sdk-python?logo=GitHub&style=flat-square)
![GitHub issues](https://img.shields.io/github/issues-raw/modzy/sdk-python?logo=github&style=flat-square)
![GitHub](https://img.shields.io/github/license/modzy/sdk-python?logo=apache&style=flat-square)

![PyPI](https://img.shields.io/pypi/v/modzy-sdk?logo=pypi&style=flat-square)
![PyPI - Downloads](https://img.shields.io/pypi/dm/modzy-sdk?logo=pypi&style=flat-square)

![Modzy Python SDK Banner](https://github.com/modzy/sdk-python/blob/main/python-sdk-github-banner.png)
## Installation

Install Modzy's Python SDK with PIP

```bash
  pip install modzy-sdk
```
    
## Usage/Examples

### Initializing the SDK
Initialize your client by authenticating with an API key. You can [download an API Key](https://docs.modzy.com/docs/view-and-manage-api-keys#download-team-api-key) from your instance of Modzy.

```python
from modzy import ApiClient, error

# Sets BASE_URL and API_KEY values
# Best to set these as environment variables
BASE_URL = "Valid Modzy URL"
API_KEY = "Valid Modzy API Key"

mdz = ApiClient(base_url=BASE_URL, api_key=API_KEY)
```

### Running Inferences
#### Text-based models
Submit an inference job to a text-based model by providing the model ID, version number, and input text:

```python
# Creates a dictionary for text input(s)
sources = {}

# Adds any number of inputs
sources["first-phone-call"] = {
    "input.txt": "Mr Watson, come here. I want to see you.",
}

# Submit the text to v1.0.1 of a Sentiment Analysis model
job = mdzy.jobs.submit_text("ed542963de", "1.0.1", sources)
```

#### Embedded inputs

Submit images and other larger inputs as embedded files to a model by providing a model ID, version number, and dictionary with one or more base64 encoded inputs
```python
from modzy._util import file_to_bytes

# Embeds input as a string in Base64
image_bytes = file_to_bytes('images/tower-bridge.jpg')
# Prepares the source dictionary
sources = {"tower-bridge": {"image": image_bytes}}

# Submits the image to v1.0.1 of an Imaged-based Geolocation model
job = mdz.jobs.submit_embedded("aevbu1h3yw", "1.0.1", sources)
```

#### Inputs from databases

Submit data from a SQL database to a model by providing a model ID, version number, a SQL query, and database connection credentials.
```python
# Adds database connection and query information
db_url = "jdbc:postgresql://db.bit.io:5432/bitdotio"
db_username = DB_USER_NAME
db_password = DB_PASSWORD
db_driver = "org.postgresql.Driver"
# Selects as "input.txt" becase that is the required input name for this model
db_query = "SELECT \"mailaddr\" as \"input.txt\" FROM \"user/demo_repo\".\"atl_parcel_attr\" LIMIT 10;"

# Submits the database query to v0.0.12 of a Named Entity Recognition model
job = client.jobs.submit_jdbc("a92fc413b5","0.0.12",db_url, db_username, db_password, db_driver, db_query)
```
### Getting Results

### Running Inferences at the Edge

The SDK provides the support for Modzy Edge:

### Deploying Models
Deploy a model to a your private model library in Modzy

```Python
from modzy import ApiClient, error

# Sets BASE_URL and API_KEY values
# Best to set these as environment variables
BASE_URL = "Valid Modzy URL"
API_KEY = "Valid Modzy API Key"

mdz = ApiClient(base_url=BASE_URL, api_key=API_KEY)

model_data = mdz.models.deploy(
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
To use **`mdz.models.deploy()`** there are 4 fields that are required:
* `container_image (str)`: This parameter must represent a container image repository & tag name, or in other words, the string you would include after a docker pull command. For example, if you were to download this container image using docker pull modzy/grpc-echo-model:1.0.0, include just modzy/grpc-echo-model:1.0.0 for this parameter
* `model_name`: The name of your model you would like to deploy
* `model_version`: The version of your model you would like to deploy
* `sample_input_file`: Filepath to a sample piece of data that your model is expected to process and perform inference against.

### Trying Out Sample Code

Explor other code examples in our [samples](https://github.com/modzy/sdk-python/tree/main/samples) folder

To run samples, set the ***`BASE_URL`*** and ***`API_KEY`*** in each sample file:

```python
client = ApiClient(base_url=BASE_URL, api_key=API_KEY)
```

Then you can run:

```bash
$ python3 samples/job_with_text_input_sample.py
```
## Documentation

Modzy's SDK is built on top of the [Modzy HTTP/REST API](https://docs.modzy.com/reference/introduction). For a full list of features and supported routes visit [Python SDK on docs.modzy.com](https://docs.modzy.com/docs/python)


## Support

For support, email opensource@modzy.com or join our [Slack](https://www.modzy.com/slack).


## Contributing

Contributions are always welcome!

See [`contributing.md`](https://github.com/modzy/sdk-python/tree/main/contributing.adoc) for ways to get started.

Please adhere to this project's `code of conduct`.

We are happy to receive contributions from all of our users. Check out our contributing file to learn more.

[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-v2.0%20adopted-ff69b4.svg)](https://github.com/modzy/sdk-python/tree/main/CODE_OF_CONDUCT.md)
