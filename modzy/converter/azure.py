import os
import shutil
from azureml.core.model import InferenceConfig
from azureml.core.environment import Environment
from azureml.core import Workspace
from azureml.core.model import Model

def prepare_azure_model(registered_model_name,subscription_id,resource_group,
                        workspace_name,env_name,entry_script_path,output_path,
                        overwrite=False):

    if os.path.isdir(output_path):
        if overwrite:
            shutil.rmtree(output_path)
        else:
            raise OSError("Output directory already exists and overwrite==False.")
    os.makedirs(output_path)

    ws = Workspace.get(name=workspace_name,
               subscription_id=subscription_id,
               resource_group=resource_group)
    
    model = Model(ws, registered_model_name)

    myenv = Environment.get(workspace=ws, name=env_name, version="1")
    myenv.inferencing_stack_version = "latest"
    inference_config = InferenceConfig(entry_script=entry_script_path, environment=myenv)

    package = Model.package(ws, [model], inference_config, generate_dockerfile=True)
    package.wait_for_creation(show_output=True)
    package.save(output_path)
    
    acr=package.get_container_registry()
    registry_info = {
        "base_image_registry": acr.address,
        "base_image_user": acr.username,
        "base_image_pass": acr.password
    }
    
    return registry_info