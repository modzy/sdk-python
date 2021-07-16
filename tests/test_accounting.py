import os
import dotenv
import pytest
from modzy import ApiClient
import logging

dotenv.load_dotenv()

BASE_URL = os.getenv('MODZY_BASE_URL')
API_KEY = os.getenv('MODZY_API_KEY')


@pytest.fixture()
def client():
    return ApiClient(base_url=BASE_URL, api_key=API_KEY)


@pytest.fixture()
def logger():
    return logging.getLogger(__name__)


def test_list_entitlements(client):
    client.accounting.list_entitlements()


# def test_has_entitlement(client):
#     assert client.accounting.has_entitlement("CAN_PATCH_PROCESSING_MODEL_VERSION")
