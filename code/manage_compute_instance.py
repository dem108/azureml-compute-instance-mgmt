### This is for admin who sets up developer environment for users.
### Admin can create, get, get_status, stop, start, delete Compute Instance under Azure ML Workspace using this commands. 
### Run this from the Azure Cloud Shell.

## Read config
import json
import pathlib
script_path = pathlib.Path(__file__).parent.absolute()
script_filename = pathlib.Path(__file__)
settings = None
with open('{}/setting/config.json'.format(script_path)) as config_json:
    settings = json.load(config_json)
    # print(settings['workspace_names'], settings['vm_size'])

## Override some parameters for individual testing
# workspaceName = "amlws006"
# computeinstance_name = "amlci000"

from helper.compute_instance_client import ComputeInstanceClient
client = ComputeInstanceClient()


if __name__=='__main__':
    supported_operations = [
        "create",
        "get",
        "get_status",
        "report",
        "start",
        "stop",
        "delete"
    ]

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--operation', type=str, dest='operation', help='Supported operations are: {}'.format(supported_operations))
    args = parser.parse_args()

    if args.operation is None or args.operation not in supported_operations:
        print("You must specify operation. Suppored operations are: {}".format(supported_operations))
        print("example: python ./{} --operation report".format(script_filename))
        print("example: python ./{} --operation create".format(script_filename))
        print("example: python ./{} --operation stop".format(script_filename))
        print("example: python ./{} --help".format(script_filename))
        exit(1)

    operation = args.operation

    client = ComputeInstanceClient()

    for workspaceName in settings['workspace_names']:
    
        if operation=="create":
            # python ./computeInstanceClient.py --operation create --subscription-id $subscription_id --resource-group-name $resource_group_name --workspace-name $amlws_name --compute-instance-name $amlws_name-$computeinstance_name --vm-size $vm_size --ssh-public-access $ssh_public_access --admin-user-ssh-public-key "$admin_user_ssh_public_key"
            client.create(subscription_id=settings['subscription_id'], resource_group_name=workspaceName, \
                workspace_name=workspaceName, compute_instance_name=workspaceName+"-"+settings['computeinstance_name'],
                vm_size=settings['vm_size'], ssh_public_access=settings['ssh_public_access'],
                admin_user_ssh_public_key=settings['admin_user_ssh_public_key'])
        elif operation=="get":
            # python ./computeInstanceClient.py --operation get --subscription-id $subscription_id --resource-group-name $resource_group_name --workspace-name $amlws_name --compute-instance-name $amlws_name-$computeinstance_name
            print(client.get(subscription_id=settings['subscription_id'], resource_group_name=workspaceName, \
                workspace_name=workspaceName, compute_instance_name=workspaceName+"-"+settings['computeinstance_name']))
        elif operation=="get_status":
            # python ./computeInstanceClient.py --operation get_status --subscription-id $subscription_id --resource-group-name $resource_group_name --workspace-name $amlws_name --compute-instance-name $amlws_name-$computeinstance_name
            print(client.get_status(subscription_id=settings['subscription_id'], resource_group_name=workspaceName, \
                workspace_name=workspaceName, compute_instance_name=workspaceName+"-"+settings['computeinstance_name']))
        elif operation=="report":
            print(client.report(subscription_id=settings['subscription_id'], resource_group_name=workspaceName, \
            workspace_name=workspaceName, compute_instance_name=workspaceName+"-"+settings['computeinstance_name'], summary=True))
        elif operation=="start":
            # python ./computeInstanceClient.py --operation start --subscription-id $subscription_id --resource-group-name $resource_group_name --workspace-name $amlws_name --compute-instance-name $amlws_name-$computeinstance_name
            client.start(subscription_id=settings['subscription_id'], resource_group_name=workspaceName, \
                workspace_name=workspaceName, compute_instance_name=workspaceName+"-"+settings['computeinstance_name'])
        elif operation=="stop":
            # python ./computeInstanceClient.py --operation stop --subscription-id $subscription_id --resource-group-name $resource_group_name --workspace-name $amlws_name --compute-instance-name $amlws_name-$computeinstance_name
            client.stop(subscription_id=settings['subscription_id'], resource_group_name=workspaceName, \
                workspace_name=workspaceName, compute_instance_name=workspaceName+"-"+settings['computeinstance_name'])
        elif operation=="delete":
            # python ./computeInstanceClient.py --operation delete --subscription-id $subscription_id --resource-group-name $resource_group_name --workspace-name $amlws_name --compute-instance-name $amlws_name-$computeinstance_name
            client.delete(subscription_id=settings['subscription_id'], resource_group_name=workspaceName, \
                workspace_name=workspaceName, compute_instance_name=workspaceName+"-"+settings['computeinstance_name'])
        else:
            pass
        
    

