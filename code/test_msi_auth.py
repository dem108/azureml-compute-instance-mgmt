from azureml.core.authentication import MsiAuthentication
from azureml.core import Workspace
from azureml.core.compute.computeinstance import ComputeInstance, ComputeInstanceProvisioningConfiguration

## Read config
import json
import pathlib
script_path = pathlib.Path(__file__).parent.absolute()
settings = None
with open('{}/common/config.json'.format(script_path)) as config_json:
    settings = json.load(config_json)
    # print(settings['workspace_names'], settings['vm_size'])

## Override some parameters for individual testing
workspaceName = "amlws006"
computeinstance_name = "amlci000"

msi_auth = MsiAuthentication()

ws = Workspace(subscription_id=settings['subscription_id'], resource_group=workspaceName, workspace_name=workspaceName, auth=msi_auth)
print(ws)

name = workspaceName + "-" + computeinstance_name
# ci = ComputeInstance(ws, name=name).get()

# properties = ci['properties']['properties']
# id_split = ci['id'].split('/')
# resource_group_name = id_split[4]
# workspace_name = id_split[8]
# "rg_name: {}, ws_name: {}. ci_name: {}, state: {}, vm_size: {}, ssh_admin_user_name: {}, ssh_public_access: {}, public_ip_address: {}, error: {}".format(resource_group_name, workspace_name, ci['name'], properties['state'], properties['vmSize'], properties['sshSettings']['adminUserName'], properties['sshSettings']['sshPublicAccess'], properties['connectivityEndpoints']['publicIpAddress'], properties['errors'])



