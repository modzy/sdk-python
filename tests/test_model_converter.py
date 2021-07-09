from modzy.converter.model_converter import ModelConverter
import os
import pytest
from modzy.client import ApiClient

BASE_URL = os.getenv('MODZY_BASE_URL')
API_KEY = os.getenv('MODZY_API_KEY')


@pytest.fixture()
def converter():
    return ModelConverter(ApiClient(base_url=BASE_URL, api_key=API_KEY))


def test_model_converter_env_status(converter):
    response = converter.env_status()
    assert response


def test_model_converter_check_endpoints(converter):
    response = converter.check_endpoints(
        "AKIAUX272I2XFHORFQ7D",
        "35exOPRUPxNn5FPdY8h43uF5cWSVEfzw9JfheVnF",
        "modzy-engineering-tests",
        "ds/model-converter/sagemaker/image-classification/weights.tar.gz",
        "ds/model-converter/sagemaker/image-classification/resources.tar.gz",
        "image-classification",
        "sagemaker"
    )
    assert response


def test_model_converter_run(converter):
    status_code, succes_entry = converter.run(
        "AKIAUX272I2XFHORFQ7D",
        "35exOPRUPxNn5FPdY8h43uF5cWSVEfzw9JfheVnF",
        "modzy-engineering-tests",
        "ds/model-converter/sagemaker/image-classification/weights.tar.gz",
        "ds/model-converter/sagemaker/image-classification/resources.tar.gz",
        "image-classification",
        "sagemaker",
        "S3"
    )
    assert status_code == 200
