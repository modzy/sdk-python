import time
import shutil
import os
import ntpath
import tarfile
from libcloud.storage.types import Provider
from libcloud.storage.providers import get_driver


SUPPORTED_STORAGE_PROVIDERS = {
    "S3": Provider.S3,
    "AZURE_BLOBS": Provider.AZURE_BLOBS,
    "GOOGLE_STORAGE": Provider.GOOGLE_STORAGE
}


def get_authenticated_storage_provider_client(storage_provider, access_key, secret_key):
    """Initialize the libcloud driver"""
    if storage_provider not in SUPPORTED_STORAGE_PROVIDERS:
        raise ValueError(f"Storage provider must be one of: {', '.join(SUPPORTED_STORAGE_PROVIDERS)}")

    storage_driver = get_driver(SUPPORTED_STORAGE_PROVIDERS[storage_provider])
    authenticated_storage_client = storage_driver(access_key, secret_key)
    return authenticated_storage_client


def upload_resources(model_yaml_path, container, resources_key,
                     storage_key, storage_secret, storage_provider, additional_filepaths=[]):
    """ Creates resources archive expected by model converter, uploads to storage provider.
    
    Args:
        model_yaml_path (str): Path to model.yaml file to be included.
        container (str): Storage provider container name (e.g. Bucket name in S3).
        resources_key (str): Desired key for resource archive once uploaded to storage provider.
        storage_key (str): Storage provider access key.
        storage_secret (str): Storage provider secret key.
        storage_provider (str): Storage provider name (must be one of "S3", "AZURE_BLOBS", or "GOOGLE_STORAGE").
        additional_filepaths (list): List of filepaths of additional files to be included.
    """
    driver = get_authenticated_storage_provider_client(storage_provider, storage_key, storage_secret)
    container = driver.get_container(container_name=container)

    # TODO: Probably set these outside of this helper function
    RESOURCES_TAR_NAME = "resources.tar.gz"
    MODEL_YAML_NAME = "model.yaml"

    # Create temp dir
    tmp_dir_path = os.path.join(os.getcwd(), f".tmp_{time.time()}")
    os.mkdir(tmp_dir_path)

    # Move the local resources that you have prepared for your model into an archive
    resources_tar_path = os.path.join(tmp_dir_path, RESOURCES_TAR_NAME)
    tar = tarfile.open(resources_tar_path, "w:gz")
    tar.add(model_yaml_path, arcname=MODEL_YAML_NAME)
    for filepath in additional_filepaths:
        tar.add(filepath, arcname=ntpath.split(filepath)[1])
    tar.close()

    # This method blocks until all the parts have been uploaded.
    extra = {'content_type': 'application/octet-stream'}

    # Upload archive to storage provider
    with open(resources_tar_path, 'rb') as iterator:
        obj = driver.upload_object_via_stream(iterator=iterator,
                                              container=container,
                                              object_name=resources_key,
                                              extra=extra)

    # Remove temp dir
    shutil.rmtree(tmp_dir_path)


def upload_model_dir(model_dir, container, model_key,
                        storage_key, storage_secret, storage_provider):
    """ Creates resources archive expected by model converter, uploads to storage provider.

    Args:
        model_dir (str): Path to saved model directory 
        container (str): Storage provider container name (e.g. Bucket name in S3).
        resources_key (str): Desired key for model archive once uploaded to storage provider.
        storage_key (str): Storage provider access key.
        storage_secret (str): Storage provider secret key.
        storage_provider (str): Storage provider name (must be one of "S3", "AZURE_BLOBS", or "GOOGLE_STORAGE").
    """
    driver = get_authenticated_storage_provider_client(storage_provider, storage_key, storage_secret)
    container = driver.get_container(container_name=container)

    # TODO: Probably set this outside of this helper function
    MODEL_TAR_NAME = "weights.tar.gz"

    # Create temp dir
    tmp_dir_path = os.path.join(os.getcwd(), ".tmp_" + str(time.time()))
    os.mkdir(tmp_dir_path)

    # Move the local model artifacts into an archive
    model_tar_path = os.path.join(tmp_dir_path, MODEL_TAR_NAME)
    tar = tarfile.open(model_tar_path, "w:gz")
    model_filenames = os.listdir(model_dir)
    for filename in model_filenames:
        if not filename.startswith('.'):
            full_path = os.path.join(model_dir, filename)
            tar.add(full_path, arcname=os.path.join('imagefiles/',filename))
    tar.close()

    # This method blocks until all the parts have been uploaded.
    extra = {'content_type': 'application/octet-stream'}

    # Upload archive to storage provider
    with open(model_tar_path, 'rb') as iterator:
        obj = driver.upload_object_via_stream(iterator=iterator,
                                              container=container,
                                              object_name=model_key,
                                              extra=extra)

    # Remove temp dir
    shutil.rmtree(tmp_dir_path)