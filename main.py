import argparse
import os
import requests
import json
import pandas as pd
import numpy as np
import permissions
from tqdm import tqdm

from pprint import pprint
from pathlib import Path
from configparser import ConfigParser
from person import Person
from access_group import AccessGroup

API_KEY, ACCOUNT_ID, ACCESS_TOKEN = (None, None, None)

def main():
    _create_access_token()

    parser = argparse.ArgumentParser()
    parser.add_argument('--permissions', dest='permissions', action='store_true')
    parser.add_argument('--read-csv', dest='feature', action='store_false')
    parser.set_defaults(feature=True)
    
    parser.add_argument('--non_premium', type=str)
    
    args = vars(parser.parse_args())
    permissions_mode = args['permissions']
    non_premium_fp = args['non_premium']
    
    if permissions_mode:
        permissions = _write_permissions()
        premium(permissions)
    
    if non_premium_fp:
        non_premium(non_premium_fp)

def _create_access_token():
    config = ConfigParser()
    config.read('config/keys.ini')

    global API_KEY
    global ACCOUNT_ID
    global ACCESS_TOKEN

    API_KEY = config['API_KEY']['api_key']
    ACCOUNT_ID = config['ACCOUNT_ID']['account_id']

    headers = {'Content-Type': 'application/x-www-form-urlencoded',}
    data = {
        'grant_type': 'urn:ibm:params:oauth:grant-type:apikey',
        'apikey': API_KEY
    }

    response = requests.post('https://iam.cloud.ibm.com/identity/token', headers=headers, data=data)
    response = json.loads(response.text)

    ACCESS_TOKEN = response['access_token']
    config['ACCESS_TOKEN'] = {}
    config['ACCESS_TOKEN']['access_token'] = ACCESS_TOKEN
    
    with open('config/keys.ini', 'w') as configfile:
        config.write(configfile)


def _does_file_exist(fp):
   if not Path(fp).is_file(): 
       raise FileNotFoundError('File not found at provided path.')
   
   return True 

def _is_csv(fp):
    split = fp.split(".")
    file_type = split[-1]
    
    if not file_type == "csv":
        raise TypeError("The file must be a CSV")
    
    return True

def _write_permissions():
    print("Extracting permissions...")
    headers = {
                'Authorization': ACCESS_TOKEN,
                'Content-Type': 'application/json',
                }

    params = (('account_id', ACCOUNT_ID),) 
    
    ########
    response = requests.get('https://iam.cloud.ibm.com/v1/policies', headers=headers, params=params)
    response = json.loads(response.text)
    
    policies = response['policies']
    target_service_name = "conversation"

    service_instances, iam_ids, viewers, operators, editors, admins, readers, \
        writers, managers, resource_types, regions, skills = [], [], [], [], [], [], [], [], [], [], [], []
    
    for policy in tqdm(policies):
        resources = policy['resources']
        roles = policy['roles']
        subjects = policy['subjects']

        SERVICE_INSTANCE = None
        IAM_ID = None
        VIEWER = 0 # role
        OPERATOR = 0 
        EDITOR = 0
        ADMIN = 0
        READER = 0
        WRITER = 0
        MANAGER = 0
        RESOURCE_TYPE = ""
        REGION = ""
        SKILL = "" # RESOURCE IN JSON
        SERVICE_NAME = ""

        ### parsing out the resources ### should be its own function
        for _, resource in enumerate(resources):
            attributes = resource['attributes']
            for attribute in attributes:
                if attribute['name'] == 'serviceInstance': SERVICE_INSTANCE = attribute['value']
                #if attribute['name'] == 'accountId': IAM_ID = attribute['value']
                if attribute['name'] == 'region': REGION = attribute['value']
                if attribute['name'] == 'resourceType': RESOURCE_TYPE = attribute['value']
                if attribute['name'] == 'resource': SKILL = attribute['value']
                if attribute['name'] == 'serviceName': SERVICE_NAME = attribute['value']
        
        #### parsing out the roles ### should be its own function
        for role in roles:
            if role['display_name'] == 'Reader': READER = 1
            if role['display_name'] == 'Viewer': VIEWER = 1
            if role['display_name'] == 'Writer': WRITER = 1
            if role['display_name'] == 'Editor': EDITOR = 1
            if role['display_name'] == 'Manager': MANAGER = 1
            if role['display_name'] == 'Administrator': ADMIN = 1
            
        if target_service_name == SERVICE_NAME:
                for subject in subjects:
                    subject_attributes = subject['attributes']
                    # there could be an instance where multplie iam_id are assigned to one attribute
                    # for every subject append the same policies 
                    for attr in subject_attributes:
                        IAM_ID = attr['value']

                        service_instances.append(SERVICE_INSTANCE)
                        iam_ids.append(IAM_ID)
                        viewers.append(VIEWER)
                        operators.append(OPERATOR) # see if i accessed the right json for this
                        editors.append(EDITOR)
                        admins.append(ADMIN)
                        readers.append(READER)
                        writers.append(WRITER)
                        managers.append(MANAGER)
                        resource_types.append(RESOURCE_TYPE)
                        regions.append(REGION)
                        skills.append(SKILL)
    
    conversation = ["conversation"] * len(service_instances)
    df = {"ibm_id": iam_ids, "service_name": conversation, "service_instance": service_instances, 
            "platform_viewer": viewers, "platform_operator": operators, "platform_editor": editors,
                "platform_admin": admins, "service_reader": readers, "service_writer": writers, "service_manager": managers, 
                    "resourceType": resource_types, "region": regions, "resource": skills}
    
    print("Finished extracting permissions")
    print("Writing to existing_permissions_output.csv")

    df = pd.DataFrame(df)
    df.to_csv('existing_permissions_output.csv')

    print("Finished writing to existing_permissions_output.csv")
    print()
    print("Reading the configurations for the new instance")

    config = ConfigParser()
    config.read('config/permissions.ini')

    target_service_inst = config['CONFIGURATION']['service_instance']
    target_resource_type = config['CONFIGURATION']['resourceType']
    target_region = config['CONFIGURATION']['region']
    target_resource = config['CONFIGURATION']['resource']

    def preprocess(target):
        if target == "\"\"" or target == "None" or target == None:
            target = ""

        return target

    print("Reading Permissions.ini file to assign users to new instance")
    df['service_instance'] = preprocess(target_service_inst)
    df['resource_type'] = preprocess(target_resource_type)
    df['region'] = preprocess(target_region)
    df['resource'] = preprocess(target_resource)

    df.to_csv('new_permissions_configuration.csv')

    return df


def non_premium(fp):
    if _does_file_exist(fp) and _is_csv(fp):
        print("Starting the process for assigning permissions in non-premium offerings...")
        people_df = pd.read_csv(fp)
        
        for _, people in people_df.iterrows():
            ibm_id = people['ibm_id']
            service_name = None 
            service_inst = None
            
            platform_viewer = people['platform_viewer']
            platform_editor = people['platform_editor']
            platform_admin = people['platform_admin']
            
            service_reader = people['service_reader']
            service_writer = people['service_writer']
            service_manager = people['service_manager']
            
            resource_group_id = people['resource_group_id']
            resource_group_viewer = people['rg_viewer']
            resource_group_operator = people['rg_operator']
            resource_group_editor = people['rg_editor']
            resource_group_admin = people['rg_admin']
            
            # creating a Person object with these attributes
            person = Person(ibm_id,
                            service_name,
                            service_inst,
                            platform_viewer,
                            platform_editor,
                            platform_admin,
                            service_reader,
                            service_writer,
                            service_manager,
                            resource_group_id,
                            resource_group_viewer,
                            resource_group_operator,
                            resource_group_editor,
                            resource_group_admin)
            
            Person.person_list.append(person)
            
            single_users = AccessGroup.create_access_groups(Person.person_list, "non premium") 
            if len(single_users): # now assign permissions to a single group of users
                headers = {
                        'Authorization': ACCESS_TOKEN,
                        'Content-Type': 'application/json',
                    }

                params = (
                        ('account_id', ACCOUNT_ID), 
                        ) 
            
                for single_user in single_users:
                    single_user = single_user[0]
                    permissions.assign_policies(single_user, headers, params, "non premium")
        

def premium(permissions_df):
    print("Starting the process for assigning permissions in premium offerings...")
    
    for _, people in permissions_df.iterrows():
        ibm_id = people['ibm_id']
        service_name = people['service_name']
        service_inst = people['service_instance']
        
        platform_viewer = people['platform_viewer']
        platform_editor = people['platform_editor']
        platform_admin = people['platform_admin']
        
        service_reader = people['service_reader']
        service_writer = people['service_writer']
        service_manager = people['service_manager']

        region = people['region']
        resource_type = people['resourceType']
        resource = people['resource']
        
        # creating a Person object with these attributes
        person = Person(ibm_id=ibm_id,
                        service_name=service_name,
                        service_inst=service_inst,
                        platform_viewer=platform_viewer,
                        platform_editor=platform_editor,
                        platform_admin=platform_admin,
                        service_reader=service_reader,
                        service_writer=service_writer,
                        service_manager=service_manager,
                        region=region,
                        resource=resource,
                        resource_type=resource_type
                        )
        
        Person.person_list.append(person)
    
    # Create the access groups 
    #single_users = AccessGroup.create_access_groups(Person.person_list, "premium")
    headers = {
            'Authorization': ACCESS_TOKEN,
            'Content-Type': 'application/json',
            }

    params = (('account_id', ACCOUNT_ID),)

    for person in Person.person_list:
        permissions.assign_policies(person, headers, params, "premium")
                
if __name__ == "__main__":
    main()