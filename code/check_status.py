from helper.compute_instance_client import ComputeInstanceClient

## Read config
import json
import pathlib
script_path = pathlib.Path(__file__).parent.absolute()
settings = None
with open('{}/common/config.json'.format(script_path)) as config_json:
    settings = json.load(config_json)
    print(settings['workspace_names'], settings['vm_size'])

client = ComputeInstanceClient()

import os

for workspaceName in settings['workspace_names']:
    print ("==================================================")
    print ("Check Compute Instance: {}, under Azure ML Workspace: {}".format(settings['computeinstance_name'], workspaceName))
    print (client.report(subscription_id=settings['subscription_id'], resource_group_name=workspaceName, workspace_name=workspaceName, compute_instance_name=workspaceName+'-'+settings['computeinstance_name'], summary=True))


