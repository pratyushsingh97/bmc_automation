# Watson Assistant Migration Tool
![Rocket](https://media.giphy.com/media/dJezVlwfVulTykjRQj/giphy.gif) <br>
by: [Pratyush Singh](pratyushsingh@ibm.com) <br> 
date: 11/11/2020

## Background 
The Watson Assistant Migration Tool takes the permissions assigned to various instances of **Watson Assistant**, and assigns them to a single instance of Watson Assistant specified under the `config/permissions.ini` file. **Note, this tool does not delete the old permissions.** 

The Migration tool is best run by the account owner, or by someone who has equivalent permissions such as administrator on the account. Additionally, to run this tool `python 3.7` is required along with `pip3` installed on the machine. The libraries required are found in `requirements.txt`, and more detail on the assets needed to run the tool are found in the *Prerequisite* section.  The Migration tool requires minor configuration before use which is detailed in the *Configuration* section.

## Prerequisites 
1. [Install the `ibmcloud cli` ](https://cloud.ibm.com/docs/cli)
2. `python 3.*`, preferably `python 3.7`
3. `pip3`
4. *Administrator* IAM Services privileges on the account

## Configuration
### IAM API Key 
1. Navigate to [IBM Cloud](cloud.ibm.com)
2. Click on "Manage"  > "Access (IAM)" 
3. Scroll down to "My IBM Cloud API Keys" > click on "View all" > "Create API Key"
4. Copy the newly created "API Key" and paste it into `api_key` field in the `config/keys.ini`
5.  The `account_id` is listed in "My user details" box under the "Access (IAM)". Copy and paste the account id in the `account_id` field in `config/keys.ini`
6.  **Leave `access_token` blank. The tool will fill that in.**

### permissions.ini
 **Note: the specifications listed in `permissions.ini` are applied to all users.**
The `permissions.ini` file contains the specifications for the Watson Assistant instance that the permissions are being transferred to.
1. The `service_instance` is the name of the Watson Assistant instance. This is equivalent to the name of Watson Assistant under the "Resource List" in [cloud.ibm.com](cloud.ibm.com).
2. *(Optional)* You can specify "assistant" or "skill" under `resourceType` if you would like to narrow the permissions down to the Assistant or Skill level.
3. *(Optional)* If `resourceType` is "skill", then `resource` is the skill id. If `resourceType` is "assistant", then `resource` is the assistant id.

## Run the Migration Script 
`python main.py --permissions`
1. The script will output  "existing_permissions_output.csv" that lists the existing permissions for Watson Assistant. Additionally, the script will output "new_permissions_configuration.csv" that lists the new permissions based on the specifications in `config/permissions.ini`.
