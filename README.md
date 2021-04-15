# Modzy Python SDK

![Modzy Logo](https://www.modzy.com/wp-content/uploads/2020/06/MODZY-RGB-POS.png)

<div align="center">

Modzy's Python SDK queries models, submits inference jobs, and returns results directly to your editor.


![GitHub contributors](https://img.shields.io/github/contributors/modzy/sdk-python)
![GitHub last commit](https://img.shields.io/github/last-commit/modzy/sdk-python)
![GitHub Release Date](https://img.shields.io/github/issues-raw/modzy/sdk-python)

[The job lifecycle](https://models.modzy.com/docs/how-to-guides/job-lifecycle) | [API Keys](https://models.modzy.com/docs/how-to-guides/api-keys) | [Samples](https://github.com/modzy/sdk-python/tree/main/samples) | [Documentation](https://models.modzy.com/docs)

</div>


## Installation

[![installation](install.gif)](https://asciinema.org/a/0lHaPxvXTrPTp1Bb6bNea1ZCG)

Use the package manager [pip](https://pip.pypa.io/en/stable/) install the SDK:

- `$ pip install modzy-sdk`

## Usage

### Initialize

Once you have a `model` and `version` identified, authenticate to Modzy with your API key:

```python
from modzy import ApiClient, error
client = ApiClient(base_url='https://modzy.example.com/api', api_key='my_key.modzy')
```

### Basic usage

The code below is applicable for `text/plain` input type.

![Basic Usage](python.gif)

Submit a job providing the model, version, and input file:

```python
job = client.jobs.submit_files('ed542963de', '0.0.27', {'input.txt': './some-file.txt'})
```

Hold until the inference is complete and results become available:

```python
result = client.results.block_until_complete(job, timeout=None)
```

Get the output results:

```python
results_json = result.get_first_outputs()['results.json']
print(results_json)
```

## Fetch errors

Errors may arise for different reasons. Fetch errors to know what is their cause and how to fix them.

Error      | Description
---------- | ---------
`NetworkError` | The SDK is unable to connect.
`ResponseError` | The API returned an error code.
`Timeout` | The model is not finished running before the timeout elapsed.
`ResultsError` | The model returns an error during the inference job.

Submitting jobs: `NetworkError`, `ResponseError`

```python
try:
    job = client.jobs.submit_files('ed542963de', '0.0.27', {'input.txt': './some-file.txt'})
except error.NetworkError as ex:
    print('Could not connect to the API:', ex)
    raise
except error.ResponseError as ex:
    print('We got an error response from the API:', ex)
    raise
```

While the model completes inference:
`NetworkError`, `ResponseError`, `Timeout`
```python
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
```

Retrieving results:
`ResultsError`
```python
try:
    outputs = result.get_first_outputs()
except error.ResultsError as ex:
    print('the model returned an error:', ex)
    raise

results_json = outputs['results.json']
print(results_json)
```

## Features

Currently we support the following API routes:


| Feature | Code |Api route
| ---     | ---  | ---
|Retrieve all models|client.models.get_all()|[api/models](https://models.modzy.com/docs/models/marketplace/retrieve-all-models-versions)|
|Retrieve some models|client.models.get_models()|[api/models](https://models.modzy.com/docs/models/marketplace/retrieve-models)|
|Retrieve model details|client.models.get()|[api/models/:model-id](https://models.modzy.com/docs/models/marketplace/retrieve-model-details)|
|Retrieve model by name|client.models.get_by_name()|[api/models](https://models.modzy.com/docs/models/marketplace/retrieve-models)|
|Retrieve related models|client.models.get_related()|[api/models/:model-id/related-models](https://models.modzy.com/docs/models/marketplace/retrieve-related-models)|
|Retrieve model versions|client.models.get_versions()|[api/models/:model-id/versions](https://models.modzy.com/docs/versions/marketplace/retrieve-versions)|
|Retrieve model version details|client.models.get_version()|[api/models/:model-id/versions/:version-id](https://models.modzy.com/docs/versions/marketplace/retrieve-version-details)|
|Retrieve all tags|client.tags.get_all()|[api/models/tags](https://models.modzy.com/docs/tags/marketplace/retrieve-tags)|
|Retrieve Tags and Models|client.tags.get_tags_and_models()|[api/models/tags/:tag-id](https://models.modzy.com/docs/tags/marketplace/retrieve-models-by-tags) |
|Submit a Job (Single Text)|client.jobs.submit_text()|[api/jobs](https://models.modzy.com/docs/jobs/job-inputs/submit-job)|
|Submit a Job (Multiple Text)|client.jobs.submit_text_bulk()|[api/jobs](https://models.modzy.com/docs/jobs/job-inputs/submit-job)|
|Submit a Job (Single Embedded)|client.jobs.submit_bytes()|[api/jobs](https://models.modzy.com/docs/jobs/job-inputs/submit-job)|
|Submit a Job (Multiple Embedded)|client.jobs.submit_bytes_bulk()|[api/jobs](https://models.modzy.com/docs/jobs/job-inputs/submit-job)|
|Submit a Job (Single File)|client.jobs.submit_files()|[api/jobs](https://models.modzy.com/docs/jobs/job-inputs/submit-job)|
|Submit a Job (Multiple Files)|client.jobs.submit_files_bulk()|[api/jobs](https://models.modzy.com/docs/jobs/job-inputs/submit-job)|
|Submit a Job (Single AWS S3)|client.jobs.submit_aws_s3()|[api/jobs](https://models.modzy.com/docs/jobs/job-inputs/submit-job)|
|Submit a Job (Multiple AWS S3)|client.jobs.submit_aws_s3_bulk()|[api/jobs](https://models.modzy.com/docs/jobs/job-inputs/submit-job)|
|Submit a Job (JDBC)|client.jobs.submit_jdbc()|[api/jobs](https://models.modzy.com/docs/jobs/job-inputs/submit-job)|
|Cancel job|job.cancel()|[api/jobs/:job-id](https://models.modzy.com/docs/jobs/jobs/cancel-pending-job)  |
|Hold until inference is complete|job.block_until_complete()|[api/jobs](https://models.modzy.com/docs/jobs/jobs/retrieve-job-details)  |
|Get Job details|client.jobs.get()|[api/jobs/:job-id](https://models.modzy.com/docs/jobs/jobs/retrieve-job-details)  |
|Retrieve results|job.get_result()|[api/jobs/:job-id](https://models.modzy.com/docs/jobs/results/retrieve-results)  |
|Retrieve Job History|client.jobs.get_history()|[api/jobs/history](https://models.modzy.com/docs/jobs/jobs/retrieve-job-history)  |

## Samples

Check out our [samples](https://github.com/modzy/sdk-python/tree/main/samples) for details on specific use cases.

To run samples:

Set the base url and api key in each sample file:

```python
# TODO: set the base url of modzy api and you api key
client = ApiClient(base_url=BASE_URL, api_key=API_KEY)
```

Or follow the instructions [here](https://github.com/modzy/sdk-python/tree/main/contributing.adoc#set-environment-variables-in-bash) to learn more.

And then, you can:

```bash
`$ py samples/job_with_text_input_sample.py`
```
## Contributing

We are happy to receive contributions from all of our users. Check out our [contributing file](https://github.com/modzy/sdk-python/tree/main/contributing.adoc) to learn more.

## Code of conduct

[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-v2.0%20adopted-ff69b4.svg)](https://github.com/modzy/sdk-python/tree/main/CODE_OF_CONDUCT.md)
