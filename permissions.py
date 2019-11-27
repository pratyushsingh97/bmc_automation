
import json
import logging
import requests

from person import Person

logging.getLogger('ag')

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


def assign_permissions_premium(person, params, headers):
    service_name = person.service_name
    service_instance = person.service_inst
    
    person_attributes = person.__dict__
    
    # get only the permissions that have ones 
    roles = []
    permissions = {key:value for key, value in person_attributes.items() if value == 1}
    platform_crns = [_platform_role_crn(key) for key in permissions.keys() if "platform" in key]
    service_crns = [_service_role_crn(key) for key in permissions.keys() if "service" in key]
    
    for service_crn, platform_crn in zip(service_crns, platform_crns):
        serv_dict = {"role_id": service_crn}
        plat_dict = {"role_id": platform_crn}
        
        roles.append(serv_dict)
        roles.append(plat_dict)
    
    # @TODO: Need to change the below code for non-premium instances when assigning access to just resources groups by adding if statement
    k, acct_id = params[0]
    account_attr = {"name": "accountId", "value": acct_id}
    service_name_attr = {"name": "serviceName", "value": service_name}
    service_inst_attr = {"name": "serviceInstance", "value": service_instance}
    
    resource_attributes = [account_attr, service_name_attr, service_inst_attr]
    resource = [{"attributes": resource_attributes}]
    
    subject_attributes = [{"name": "iam_id", "value": person.ibm_id}]
    subjects = [{"attributes": subject_attributes}]
    
    data = {"type": "access", "subjects": subjects, 
            "roles": roles, "resources": resource}
    
    data = json.dumps(data)
    response = requests.post('https://iam.cloud.ibm.com/v1/policies', headers=headers, data=data)
    
    if response.status_code != 201:
        logging.critical(f"Assigning Permissions failed for {person.ibm_id}")
        raise Exception(response.text)
    
    logging.info(f"Permissions sucessfully assigned for {person.ibm_id}")
    print(f"Permissions sucessfully assigned for {person.ibm_id}")
    
    
   

    