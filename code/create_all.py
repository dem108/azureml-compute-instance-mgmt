### This is for admin who sets up developer environment for users.
### Admin can list names of Azure ML Workspaces to create in file `config.json` 
### Run this from the Azure Cloud Shell.

## Read config
import json
import pathlib
script_path = pathlib.Path(__file__).parent.absolute()
settings = None
with open('{}/common/config.json'.format(script_path)) as config_json:
    settings = json.load(config_json)
    print(settings['workspace_names'], settings['vm_size'])

from helper.compute_instance_client import ComputeInstanceClient

import os

for workspaceName in settings['workspace_names']:
    # Step1: Create resource groups and Azure ML Workspaces (without Compute Instance) using ARM template.
    print("==================================================")
    print("Start creating resource group: {}".format(workspaceName))
    os.system("az group create --name {} --location {}".format(workspaceName, settings['region']))

    print("==================================================")
    print("Start deploying Azure ML Workspace: {}".format(workspaceName))
    template_path = "{}/azuredeploy.json".format(script_path)
    os.system("az deployment group create --resource-group {} --template-file {} -p workspaceName={} -p location={} -p sku={}".format(workspaceName, template_path, workspaceName, "koreacentral", "basic"))

    # Step2: Create Compute Instances using Python SDK
    print("==================================================")
    print("Start creating Compute Instance: {}, under Azure ML Workspace: {}".format(settings['computeinstance_name'], workspaceName))
    client = ComputeInstanceClient()
    client.create(subscription_id=settings['subscription_id'], resource_group_name=workspaceName, \
        workspace_name=workspaceName, compute_instance_name=workspaceName+"-"+settings['computeinstance_name'],
        vm_size=settings['vm_size'], ssh_public_access=settings['ssh_public_access'],
        admin_user_ssh_public_key=settings['admin_user_ssh_public_key'])


