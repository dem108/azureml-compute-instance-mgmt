from azureml.core import Workspace
from azureml.core.authentication import MsiAuthentication
from azureml.core.compute.computeinstance import ComputeInstance, ComputeInstanceProvisioningConfiguration

msi_auth = MsiAuthentication()

class ComputeInstanceClient():
    def __init__(self):
        pass

    def create(self, subscription_id, resource_group_name, workspace_name, compute_instance_name, vm_size, ssh_public_access, admin_user_ssh_public_key):
        ws = Workspace(subscription_id=subscription_id, resource_group=resource_group_name, workspace_name=workspace_name, auth=msi_auth)
        # print(ws.name, ws.location)

        provision_config = ComputeInstance.provisioning_configuration(vm_size=vm_size, ssh_public_access=ssh_public_access, admin_user_ssh_public_key=admin_user_ssh_public_key)
        compute_instance = ComputeInstance.create(ws, compute_instance_name, provision_config)
        return compute_instance

    def get(self, subscription_id, resource_group_name, workspace_name, compute_instance_name):
        ws = Workspace(subscription_id=subscription_id, resource_group=resource_group_name, workspace_name=workspace_name, auth=msi_auth)
        return ComputeInstance(ws, name=compute_instance_name)

    def get_status(self, subscription_id, resource_group_name, workspace_name, compute_instance_name):
        ws = Workspace(subscription_id=subscription_id, resource_group=resource_group_name, workspace_name=workspace_name, auth=msi_auth)
        return ComputeInstance(ws, name=compute_instance_name).get_status()
        
    def report(self, subscription_id, resource_group_name, workspace_name, compute_instance_name, summary=False):
        ws = Workspace(subscription_id=subscription_id, resource_group=resource_group_name, workspace_name=workspace_name, auth=msi_auth)
        ci = ComputeInstance(ws, name=compute_instance_name).get()
        if summary==False:
            return ci
        else:
            properties = ci['properties']['properties']
            id_split = ci['id'].split('/')
            resource_group_name = id_split[4]
            workspace_name = id_split[8]
            return "rg_name: {}, ws_name: {}. ci_name: {}, state: {}, vm_size: {}, ssh_admin_user_name: {}, ssh_public_access: {}, public_ip_address: {}, error: {}".format(resource_group_name, workspace_name, ci['name'], properties['state'], properties['vmSize'], properties['sshSettings']['adminUserName'], properties['sshSettings']['sshPublicAccess'], properties['connectivityEndpoints']['publicIpAddress'], properties['errors'])

    def start(self, subscription_id, resource_group_name, workspace_name, compute_instance_name):
        ws = Workspace(subscription_id=subscription_id, resource_group=resource_group_name, workspace_name=workspace_name, auth=msi_auth)
        ComputeInstance(ws, name=compute_instance_name).start()

    def stop(self, subscription_id, resource_group_name, workspace_name, compute_instance_name):
        ws = Workspace(subscription_id=subscription_id, resource_group=resource_group_name, workspace_name=workspace_name, auth=msi_auth)
        ComputeInstance(ws, name=compute_instance_name).stop()

    def delete(self, subscription_id, resource_group_name, workspace_name, compute_instance_name):
        ws = Workspace(subscription_id=subscription_id, resource_group=resource_group_name, workspace_name=workspace_name, auth=msi_auth)
        ComputeInstance(ws, name=compute_instance_name).delete()



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
    parser.add_argument('--subscription-id', type=str, dest='subscription_id', help='Subscription ID to use')
    parser.add_argument('--resource-group-name', type=str, dest='resource_group_name', help='Resource Group name to use')
    parser.add_argument('--workspace-name', type=str, dest='workspace_name', help='Azure ML Workspace name to use')
    parser.add_argument('--compute-instance-name', type=str, dest='compute_instance_name', help='Compute Instance name to use')
    parser.add_argument('--vm-size', type=str, dest='vm_size', help='VM Size (needed when creating Compute Instance)')
    parser.add_argument('--ssh-public-access', type=str, dest='ssh_public_access', help='SSH Public Access (needed when creating Compute Instance). If this value is \'true\', then SSH is enabled.')
    parser.add_argument('--admin-user-ssh-public-key', type=str, dest='admin_user_ssh_public_key', help='Pass SSH public key (required only when ssh-public-access is true)')
    args = parser.parse_args()

    if args.operation is None:
        print("You must specify operation. Suppored operations are: {}".format(supported_operations))
        print("example: python ./this.py --operation get_status --subscription-id \"1234567890\" --resource-group-name rgname1 --workspace-name wsname1 --compute-instance-name ci1 ")
        print("example: python ./this.py --operation create --subscription-id \"1234567890\" --resource-group-name rgname1 --workspace-name wsname1 --compute-instance-name ci1 --vm-size STANDARD_D2_v2 --ssh-public-access True --admin-user-ssh-public-key \"abcdefg\"")
        print("example: python ./this.py --help")
        exit(1)

    operation = args.operation
    subscription_id = args.subscription_id
    resource_group_name = args.resource_group_name
    workspace_name = args.workspace_name
    compute_instance_name = args.compute_instance_name
    vm_size = args.vm_size
    ssh_public_access = args.ssh_public_access
    admin_user_ssh_public_key = args.admin_user_ssh_public_key

    client = ComputeInstanceClient()
    if operation=="create":
        ssh_flag = False
        if ssh_public_access.lower()=="true":
            ssh_flag = True
        client.create(subscription_id, resource_group_name, workspace_name, compute_instance_name, vm_size, ssh_flag, admin_user_ssh_public_key)
    elif operation=="get":
        print(client.get(subscription_id, resource_group_name, workspace_name, compute_instance_name))
    elif operation=="stop":
        client.stop(subscription_id, resource_group_name, workspace_name, compute_instance_name)
    elif operation=="get_status":
        print(client.get_status(subscription_id, resource_group_name, workspace_name, compute_instance_name))
    elif operation=="report":
        print(client.report(subscription_id, resource_group_name, workspace_name, compute_instance_name))
    elif operation=="start":
        client.start(subscription_id, resource_group_name, workspace_name, compute_instance_name)
    elif operation=="delete":
        client.delete(subscription_id, resource_group_name, workspace_name, compute_instance_name)
    else:
        print("Unaccepeted operation: {}".format(operation))
        print("Suppored operations are: {}".format(supported_operations))
        print("Try with --help")
    
    
