# ReadMe for BMC Automation Script


## Background

The *Automatic IAM Manager* assigns permissions to resources and resource groups. Given a CSV, the templates are attached, the program will iterate through each candidate, form access groups if several users have the same permissions, and assign the appropriate permissions to that access group. 

If a user shares **no** shared policies then the program will just assign the permissions to that user. The script has logging and catches exceptions if any step of the program fails (creating an access group, assigning permissions, etc.). The logs are there to help debug at which point did the service fail.

There are two types of CSV - *premium.csv* and *non_premium.csv.* The *premium.csv* is for assigning access to server instances. The *non_premium.csv* is for assigning permissions to resource groups.

## Requirements:

- python 3.x
- ibmcloud cli

## Issue Being Investigated

For some reason, the *IBM IAM Policy Manager API*, the backbone of this program, only seems to accept raw string auth tokens. If a variable is passed, then the call seems to fail. The issue is currently being investigated, and the ReadMe will be updated once a fix is found. In the meantime, in the section **How to Use** I have shown the places that a raw string auth-tokens needs to be placed. 

## Installation

- Python 3 install guide can be found [here](https://www.python.org/downloads/). For the development of this project was python 3.6.8
- The guide to install the IBM Cloud CLI can be found [here](https://cloud.ibm.com/docs/cli?topic=cloud-cli-getting-started)

## Usage

1. Login into your IBM Cloud account via the terminal: `ibmcloud login --sso`
2. Follow the steps on the screen and choose the account that will be assigning the permissions to resources inside of it.
3. Note down the account id. The account id is an alphanumeric string that is in parentheses following the account name. Kind of like `Bob Marley (ae345345)`. The account number is one of the raw string that will be required.
4. Next, we will obtain the *IAM Token.* In the terminal, type the following command: `ibmcloud iam ouath-tokens`. Copy & paste the token (only the string starting at *Bearer:xxxx* onwards is required). This is the other token that will be used as raw input. 
5. For premium instances, open up *premium.csv.* 
    1. Enter the *ibm_id.* It can be found by the following navigation path on [cloud.ibm.com](http://cloud.ibm.com):
        1. Manage → Access (IAM) → Users → *Select the Use*r → *User Details → IAM ID*
    2. The service name is for example "watson-assistant" or "natural-language-understanding"
        1. I have found that putting the service name in lowercase with dashes works better
    3. The service instance is an alphanumeric string that identifies the instance
    4. After these fields are defined, the remaining columns (i.e. *platform_viewer)* define the level of access to provide. Place a "1" if you would like to grant this particular user that level of access. You can leave the column blank or assign a "0" if you **do not** wish to assign any access. 
        1. **Note, not all resources offer service-level access. If you provide service-level access for a resource that does not have it, the API will return an error.**
6.  Now it is time to place the raw tokens, the *IAM-Token* and the *account id* into our code. As a reminder, the issue is being investigated and will be fixed as soon as possible.
    1. Place the tokens starting at **line 86** and **line 138** in *main.py.* I have placed a placeholder where the text should be copy & pasted. 
    2. Place the tokens starting at **line 245** in *access_group.py*
7. Follow the same steps as above for *non-premium* instances except the *non-premium.csv* requires the resource group id.
8. The program can be run with the following commands:
    1. `python [main.py](http://main.py) --premium premium.csv` for premium instances
    2. `python [main.py](http://main.py) --non_premium non_premium.csv` for non-premium instances
