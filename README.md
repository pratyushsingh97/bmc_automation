# ReadMe for BMC Automation Script

Created By: Pratyush Singh
Last Edited: Nov 27, 2019 1:04 PM

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
4. Next, we will obtain the *IAM Token.* In the terminal, type the following command: `ibmcloud iam ouath-tokens`. Copy & paste the token (only the string starting at *Bearer:xxxx* onwards is required. This is the other token that will be used as raw input. 
5. For premium instances, open up *premium.csv.* 
    1. Enter the *ibm_id.* It can be found by the following navigation path on [cloud.ibm.com](http://cloud.ibm.com):

    Manage → Access (IAM) → Users → *Select the Use*r → *User Details → IAM ID*
