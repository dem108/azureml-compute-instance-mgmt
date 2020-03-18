from azureml.core import Workspace
from azureml.core.authentication import MsiAuthentication
from azureml.core.compute.computeinstance import ComputeInstance, ComputeInstanceProvisioningConfiguration
import traceback
from helper.common import exception_to_string
from azureml.exceptions import ProjectSystemException, ComputeTargetException

import json
import pathlib
script_path = pathlib.Path(__file__).parent.absolute()
script_filename = pathlib.Path(__file__)

msi_auth = MsiAuthentication()

class ComputeInstanceClient():
    
    def __init__(self):    
        """Initialize this client for Compute Instance
        """        
        pass

    def create(self, subscription_id, resource_group_name, workspace_name, compute_instance_name, vm_size, ssh_public_access, admin_user_ssh_public_key):
        """Create Compute Instance under specified Azure ML workspace.
        
        :param subscription_id: Subscription ID to use
        :type subscription_id: str
        :param resource_group_name: Resource Group name to use
        :type resource_group_name: str
        :param workspace_name: Azure ML workspace name to use
        :type workspace_name: str
        :param compute_instance_name: Azure ML Compute Instance name to use
        :type compute_instance_name: str
        :param vm_size: VM size to use
        :type vm_size: str
        :param ssh_public_access: Whether to allow SSH Public Access
        :type ssh_public_access: boolean
        :param admin_user_ssh_public_key: SSH Public Key to use for the Compute Instance
        :type admin_user_ssh_public_key: str
        :return: Created Compute Instance object
        :rtype: azureml.core.compute.computeinstance.ComputeInstance
        """        
        compute_instance = None

        try:
            ws = Workspace(subscription_id=subscription_id, resource_group=resource_group_name, workspace_name=workspace_name, auth=msi_auth)
            # print(ws.name, ws.location)
            provision_config = ComputeInstance.provisioning_configuration(vm_size=vm_size, ssh_public_access=ssh_public_access, admin_user_ssh_public_key=admin_user_ssh_public_key)
            compute_instance = ComputeInstance.create(ws, compute_instance_name, provision_config)
        except ProjectSystemException as ex:
            print("ProjectSystemException: {}".format(ex.message))
        except ComputeTargetException as ex:
            print("ComputeTargetException: {}".format(ex.message))
        except Exception as ex:
            print("Error caught at: {}\n{}".format(self, exception_to_string(ex)))

        return compute_instance

    def get(self, subscription_id, resource_group_name, workspace_name, compute_instance_name):
        """Retrieve Compute Instance object.
        
        :param subscription_id: Subscription ID to use
        :type subscription_id: str
        :param resource_group_name: Resource Group name to use
        :type resource_group_name: str
        :param workspace_name: Azure ML workspace name to use
        :type workspace_name: str
        :param compute_instance_name: Azure ML Compute Instance name to use
        :type compute_instance_name: str
        :return: Compute Instance object that is retrieve by specified parameters.
        :rtype: azureml.core.compute.computeinstance.ComputeInstance
        """        
        compute_instance = None

        try:
            ws = Workspace(subscription_id=subscription_id, resource_group=resource_group_name, workspace_name=workspace_name, auth=msi_auth)
            compute_instance = ComputeInstance(ws, name=compute_instance_name)
        except ProjectSystemException as ex:
            print("ProjectSystemException: {}".format(ex.message))
        except ComputeTargetException as ex:
            print("ComputeTargetException: {}".format(ex.message))
        except Exception as ex:
            print("Error caught at: {}\n{}".format(self, exception_to_string(ex)))

        return compute_instance

    def get_status(self, subscription_id, resource_group_name, workspace_name, compute_instance_name):
        """Retrieve status of specified Compute Instance.
        
        :param subscription_id: Subscription ID to use
        :type subscription_id: str
        :param resource_group_name: Resource Group name to use
        :type resource_group_name: str
        :param workspace_name: Azure ML workspace name to use
        :type workspace_name: str
        :param compute_instance_name: Azure ML Compute Instance name to use
        :type compute_instance_name: str
        :return: Compute Instance status.
        :rtype: azureml.core.compute.computeinstance.ComputeInstanceStatus
        """        
        compute_instance = None

        try:
            ws = Workspace(subscription_id=subscription_id, resource_group=resource_group_name, workspace_name=workspace_name, auth=msi_auth)
            compute_instance = ComputeInstance(ws, name=compute_instance_name).get_status()
        except ProjectSystemException as ex:
            print("ProjectSystemException: {}".format(ex.message))
        except ComputeTargetException as ex:
            print("ComputeTargetException: {}".format(ex.message))
        except Exception as ex:
            print("Error caught at: {}\n{}".format(self, exception_to_string(ex)))

        return compute_instance

    def report(self, subscription_id, resource_group_name, workspace_name, compute_instance_name, summary=False):
        """Reports current status of Compute Instance
        
        :param subscription_id: Subscription ID to use
        :type subscription_id: str
        :param resource_group_name: Resource Group name to use
        :type resource_group_name: str
        :param workspace_name: Azure ML workspace name to use
        :type workspace_name: str
        :param compute_instance_name: Azure ML Compute Instance name to use
        :type compute_instance_name: str
        :param summary: [TODO], defaults to False
        :type summary: bool, optional
        :return: [TODO]
        :rtype: [TODO]
        """        
        ws = None
        ci = None
        status = None
        
        try:
            ws = Workspace(subscription_id=subscription_id, resource_group=resource_group_name, workspace_name=workspace_name, auth=msi_auth)
            ci = ComputeInstance(ws, name=compute_instance_name).get()
            if summary==False:
                status = ci
            else:
                properties = ci['properties']['properties']
                id_split = ci['id'].split('/')
                resource_group_name = id_split[4]
                workspace_name = id_split[8]
                status = "rg_name: {}, ws_name: {}. ci_name: {}, state: {}, vm_size: {}, ssh_admin_user_name: {}, ssh_public_access: {}, public_ip_address: {}, error: {}".format(resource_group_name, workspace_name, ci['name'], properties['state'], properties['vmSize'], properties['sshSettings']['adminUserName'], properties['sshSettings']['sshPublicAccess'], properties['connectivityEndpoints']['publicIpAddress'], properties['errors'])
        except ProjectSystemException as ex:
            print("ProjectSystemException: {}".format(ex.message))
        except ComputeTargetException as ex:
            print("ComputeTargetException: {}".format(ex.message))
        except Exception as ex:
            print("Error caught at: {}\n{}".format(self, exception_to_string(ex)))

        return status

    def start(self, subscription_id, resource_group_name, workspace_name, compute_instance_name):
        """Starts the Compute Instance
        
        :param subscription_id: Subscription ID to use
        :type subscription_id: str
        :param resource_group_name: Resource Group name to use
        :type resource_group_name: str
        :param workspace_name: Azure ML workspace name to use
        :type workspace_name: str
        :param compute_instance_name: Azure ML Compute Instance name to use
        :type compute_instance_name: str
        """        
        try:
            ws = Workspace(subscription_id=subscription_id, resource_group=resource_group_name, workspace_name=workspace_name, auth=msi_auth)
            ComputeInstance(ws, name=compute_instance_name).start()
        except ProjectSystemException as ex:
            print("ProjectSystemException: {}".format(ex.message))
        except ComputeTargetException as ex:
            print("ComputeTargetException: {}".format(ex.message))
        except Exception as ex:
            print("Error caught at: {}\n{}".format(self, exception_to_string(ex)))


    def stop(self, subscription_id, resource_group_name, workspace_name, compute_instance_name):
        """Stops the Compute Instance
        
        :param subscription_id: Subscription ID to use
        :type subscription_id: str
        :param resource_group_name: Resource Group name to use
        :type resource_group_name: str
        :param workspace_name: Azure ML workspace name to use
        :type workspace_name: str
        :param compute_instance_name: Azure ML Compute Instance name to use
        :type compute_instance_name: str
        """        
        try:
            ws = Workspace(subscription_id=subscription_id, resource_group=resource_group_name, workspace_name=workspace_name, auth=msi_auth)
            ComputeInstance(ws, name=compute_instance_name).stop()
        except ProjectSystemException as ex:
            print("ProjectSystemException: {}".format(ex.message))
        except ComputeTargetException as ex:
            print("ComputeTargetException: {}".format(ex.message))
        except Exception as ex:
            print("Error caught at: {}\n{}".format(self, exception_to_string(ex)))

    def delete(self, subscription_id, resource_group_name, workspace_name, compute_instance_name):
        """Deletes the Compute Instance
        
        :param subscription_id: Subscription ID to use
        :type subscription_id: str
        :param resource_group_name: Resource Group name to use
        :type resource_group_name: str
        :param workspace_name: Azure ML workspace name to use
        :type workspace_name: str
        :param compute_instance_name: Azure ML Compute Instance name to use
        :type compute_instance_name: str
        """        
        try:
            ws = Workspace(subscription_id=subscription_id, resource_group=resource_group_name, workspace_name=workspace_name, auth=msi_auth)
            ComputeInstance(ws, name=compute_instance_name).delete()
        except ProjectSystemException as ex:
            print("ProjectSystemException: {}".format(ex.message))
        except ComputeTargetException as ex:
            print("ComputeTargetException: {}".format(ex.message))
        except Exception as ex:
            print("Error caught at: {}\n{}".format(self, exception_to_string(ex)))

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
        print("example: python ./{} --operation get_status --subscription-id \"1234567890\" --resource-group-name rgname1 --workspace-name wsname1 --compute-instance-name ci1".format(script_filename))
        print("example: python ./{} --operation create --subscription-id \"1234567890\" --resource-group-name rgname1 --workspace-name wsname1 --compute-instance-name ci1 --vm-size STANDARD_D2_v2 --ssh-public-access True --admin-user-ssh-public-key \"abcdefg\"".format(script_filename))
        print("example: python ./{} --help".format(script_filename))
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
    
    
