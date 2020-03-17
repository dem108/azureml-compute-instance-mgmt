### This is for admin who sets up developer environment for users.
### Admin can create, get, get_status, stop, start, delete Compute Instance under Azure ML Workspace using this individual commands. 
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

## create
python ./computeInstanceClient.py --operation create --subscription-id $subscription_id --resource-group-name $resource_group_name --workspace-name $amlws_name --compute-instance-name $computeinstance_name --vm-size $vm_size --ssh-public-access $ssh_public_access --admin-user-ssh-public-key "$admin_user_ssh_public_key"

## get
python ./computeInstanceClient.py --operation get --subscription-id $subscription_id --resource-group-name $resource_group_name --workspace-name $amlws_name --compute-instance-name $computeinstance_name

## get_status
python ./computeInstanceClient.py --operation get_status --subscription-id $subscription_id --resource-group-name $resource_group_name --workspace-name $amlws_name --compute-instance-name $computeinstance_name

## stop
python ./computeInstanceClient.py --operation stop --subscription-id $subscription_id --resource-group-name $resource_group_name --workspace-name $amlws_name --compute-instance-name $computeinstance_name

## start
python ./computeInstanceClient.py --operation start --subscription-id $subscription_id --resource-group-name $resource_group_name --workspace-name $amlws_name --compute-instance-name $computeinstance_name

## delete
python ./computeInstanceClient.py --operation delete --subscription-id $subscription_id --resource-group-name $resource_group_name --workspace-name $amlws_name --compute-instance-name $computeinstance_name




