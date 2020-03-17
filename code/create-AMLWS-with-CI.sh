### This is for admin who sets up developer environment for users.
### Admin can list names of Azure ML Workspaces to create in file `workspaceNames.txt` 
### Run this from the Azure Cloud Shell.

### set common variables
region={REPLACE THIS}
subscription_id={REPLACE THIS}
resource_group_name={REPLACE THIS}
amlws_name={REPLACE THIS}
computeinstance_name={REPLACE THIS}
vm_size={REPLACE THIS}
ssh_public_access={REPLACE THIS} # `true` if needed
admin_user_ssh_public_key="{REPLACE THIS}"


for workspaceName in `cat workspaceNames.txt`; do
    # Step1: Create resource groups and Azure ML Workspaces (without Compute Instance) using ARM template.
    echo ==================================================
    echo Start creating resource group: $workspaceName
    az group create --name $workspaceName --location $region

    echo ==================================================
    echo Start deploying Azure ML Workspace: $workspaceName
    az deployment group create --resource-group $workspaceName --template-file ./azuredeploy.json -p workspaceName=$workspaceName -p location=koreacentral -p sku=basic

    # Step2: Create Compute Instances using Python SDK
    python ./computeInstanceClient.py --operation create --subscription-id $subscription_id --resource-group-name $resource_group_name --workspace-name $amlws_name --compute-instance-name $computeinstance_name --vm-size $vm_size --ssh-public-access $ssh_public_access --admin-user-ssh-public-key "$admin_user_ssh_public_key"
done

