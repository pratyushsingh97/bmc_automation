
import json
import logging
import requests
import math

from person import Person

logging.getLogger('ag')

def _read_all_permissions(params, headers): # read the permissions from all of the Watson Assistant permissions
    response = requests.get('https://iam.cloud.ibm.com/v1/policies', headers=headers, params=params)


def _platform_role_crn(role):
    mapping_role = {"_platform_viewer": "Viewer",
                    "_platform_editor": "Editor",
                    "_platform_administrator": "Administrator"}
    mapped_role = mapping_role[role]
    crn = f"crn:v1:bluemix:public:iam::::role:{mapped_role}"
    
    return crn

def _service_role_crn(role):
    mapping_role = {"_service_reader": "Reader",
                    "_service_writer": "Writer",
                    "_service_manager": "Manager"}
    mapped_role = mapping_role[role]
    crn = f"crn:v1:bluemix:public:iam::::serviceRole:{mapped_role}" 
    
    return crn


def assign_policies(person, headers, params, option):
    print("Assigning Permission....")
    logging.info("Assigning Permissions")
        
    service_name = person.service_name # none in non premium
    service_instance = person.service_inst # none in non premium
    region = person.region
    resource_type = person.resource_type # "assistant" for assistant id or "skill" for skill id
    resource = person.resource # @TODO: figure this part completely out or add some filter for only assistants 
    resource_group_id = person.rg_id
    
    person_attributes = person.__dict__
    
    # get only the permissions that have ones 
    roles = []
    permissions = {key:value for key, value in person_attributes.items() if value == 1}
    platform_crns = [_platform_role_crn(key) for key in permissions.keys() if "platform" in key]
    service_crns = [_service_role_crn(key) for key in permissions.keys() if "service" in key]

    if len(service_crns):
        for service_crn in service_crns:
             serv_dict = {"role_id": service_crn}
             roles.append(serv_dict)
    
    if len(platform_crns):
       for platform_crn in platform_crns:
             plat_dict = {"role_id": platform_crn}
             roles.append(plat_dict)
   
    _, acct_id = params[0]
    account_attr = {"name": "accountId", "value": acct_id}
    resource_attributes = None
    
    if option == 'premium':
        service_name_attr = {"name": "serviceName", "value": service_name}
        service_inst_attr = {"name": "serviceInstance", "value": service_instance}
        service_region_attr = {"name": "region", "value": region}
        resource_type_attr = {"name": "resourceType", "value": resource_type}
        resource_attr = {"name": "resource", "value": resource}
        
        resource_attributes = [account_attr, service_name_attr, service_inst_attr, 
                               service_region_attr, resource_type_attr, resource_attr]
        
        resource_attributes = [element for element in resource_attributes if type(element['value']) != float]
        
    else:
        rg_id_attr = {"name": "resourceGroupId", "value": resource_group_id}
        resource_attributes = [account_attr, rg_id_attr]
    
    resource = [{"attributes": resource_attributes}]
    
    subject_attributes = [{"name": "iam_id", "value": person.ibm_id}]
    subjects = [{"attributes": subject_attributes}]
    
    data = {"type": "access", "subjects": subjects, 
            "roles": roles, "resources": resource}

    data = json.dumps(data)
    response = requests.post('https://iam.cloud.ibm.com/v1/policies', headers=headers, data=data)
    
    if response.status_code != 201:
        logging.critical(f"Assigining permissions failed for {person.ibm_id}")
        raise Exception(response.text)
    
    logging.info(f"Permissions sucessfully assigned for {person.ibm_id}")
    print(f"Permissions sucessfully assigned for {person.ibm_id}")
 
    
   

    