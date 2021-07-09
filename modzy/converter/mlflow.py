from modzy.converter.utils import get_authenticated_storage_provider_client
import time
import shutil
import os
import ntpath
import tarfile


def upload_mlflow_model(mlflow_model_dir, container, model_key,
                        storage_key, storage_secret, storage_provider):
    """ Creates resources archive expected by model converter, uploads to storage provider.
    Args:
        mlflow_model_dir (str): Path to saved MLFlow model directory (e.g. using mlflow.sklearn.save_model())
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

    # Move the local mlflow model artifacts that were saved out by MLFlow into an archive
    model_tar_path = os.path.join(tmp_dir_path, MODEL_TAR_NAME)
    tar = tarfile.open(model_tar_path, "w:gz")
    mlflow_model_filenames = os.listdir(mlflow_model_dir)
    for filename in mlflow_model_filenames:
        full_path = os.path.join(mlflow_model_dir, filename)
        tar.add(full_path, arcname=filename)
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
