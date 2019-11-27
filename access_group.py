import random
import requests
import io
import json
import logging

from configparser import ConfigParser
from pprint import pprint

logging.basicConfig(filename='logs/logs.txt',
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.CRITICAL)

logging.critical("Running Access Groups")
logger = logging.getLogger('ag')

class AccessGroup(object):
    access_grp_list = []
    
    def __init__(self, ag_name=None, ag_id=None, members=None):
        self._ag_name = ag_name
        self._ag_id = ag_id
        self._members = members
        self.policy = None
    
    @property
    def ag_name(self):
        return self._ag_name
    
    @ag_name.setter
    def ag_name(self, name):
        self._ag_name = name
    
    @property
    def ag_id(self):
        return self._ag_id
    
    @ag_id.setter
    def ag_id(self, _id):
        self._ag_id = _id
    
    @property
    def members(self):
        return self._members
    
    @members.setter
    def members(self, ag_members):
        self.members = ag_members
    
    @staticmethod
    def _create_groupings(people_list:list, resource) -> list:
        # this returns the list of people who are not part of any resource group
        ag = {}
        
        if resource == 'premium':
            # only hashes on the permissions and service name
            for person in people_list:
                service_name = person.service_name
                platform_viewer = person.platform_viewer
                platform_editor = person.platform_editor
                platform_admin = person.platform_administrator
                    
                service_reader = person.service_reader
                service_writer = person.service_writer
                service_manager = person.service_manager
                
                hash_code = hash((service_name,
                                platform_viewer,
                                platform_editor,
                                platform_admin,
                                service_reader,
                                service_writer,
                                service_manager))
                
                if hash_code in ag.keys():
                    ag[hash_code].append(person)
                else:
                    ag[hash_code] = [person]
        
        # @TODO: write this porition of the script
        else:
            pass
        
        
        access_groups = list(ag.values())
        single_users = [person for person in access_groups if len(person) == 1]
        groups = [person for person in access_groups if len(person) > 1]
        
        return single_users, groups
        
    
    @staticmethod
    def _credentials():
        config = ConfigParser()
        config.read('config.ini')
        
        return config['Keys']['iam_token'], config['Keys']['account_id']
    
    @staticmethod
    def _add_members(headers):
        data = {"members": []}
        for access_group in AccessGroup.access_grp_list:
            ibm_ids = [ibmid.ibm_id for ibmid in access_group.members]
            
            for _id in ibm_ids:
                d = {"iam_id": _id, "type": "user"}
                data['members'].append(d)
            
            data = json.dumps(data)
            access_group_id = access_group.ag_id
            response = requests.put(f'https://iam.cloud.ibm.com/v2/groups/{access_group_id}/members', headers=headers, data=data)
            
            if response.status_code != 207:
                raise Exception(response.text) 
            
            response_json = response.json()
            members = response_json['members']
            
            for member in members:
                if member['status_code'] != 200:
                    msg = f"{member.iam_id} not added to access group, {access_group.ag_name}. Result returned error, {member.message} with code {member.code}"
                    logging.critical(msg) 

    @staticmethod
    def _platform_role_crn(role):
        mapping_role = {"_platform_viewer": "Viewer",
                        "_platform_editor": "Editor",
                        "_platform_administrator": "Administrator"}
        mapped_role = mapping_role[role]
        crn = f"crn:v1:bluemix:public:iam::::role:{mapped_role}"
        
        return crn
    
    @staticmethod
    def _service_role_crn(role):
        mapping_role = {"_service_reader": "Reader",
                        "_service_writer": "Writer",
                        "_service_manager": "Manager"}
        mapped_role = mapping_role[role]
        crn = f"crn:v1:bluemix:public:iam::::serviceRole:{mapped_role}" 
        
        return crn
        
    @staticmethod
    def _assign_policies(headers, params):
        print("Assigning Permission....")
        logging.info("Assigning Permissions")
        
        for access_group in AccessGroup.access_grp_list:
            # get the permissions from one person (all people in an AG have the same permissions)
            person = access_group.members[0]
            service_name = person.service_name
            service_instance = person.service_inst
            
            person_attributes = person.__dict__
            
            # get only the permissions that have ones 
            roles = []
            permissions = {key:value for key, value in person_attributes.items() if value == 1}
            platform_crns = [AccessGroup._platform_role_crn(key) for key in permissions.keys() if "platform" in key]
            service_crns = [AccessGroup._service_role_crn(key) for key in permissions.keys() if "service" in key]
            
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
            
            subject_attributes = [{"name": "access_group_id", "value": access_group.ag_id}]
            subjects = [{"attributes": subject_attributes}]
            
            data = {"type": "access", "subjects": subjects, 
                    "roles": roles, "resources": resource}
            
            data = json.dumps(data)
            response = requests.post('https://iam.cloud.ibm.com/v1/policies', headers=headers, data=data)
            
            if response.status_code != 201:
                logging.critical(f"Creating access group failed for AG {access_group.ag_name}")
                raise Exception(response.text)
            
            logging.info(f"Permissions sucessfully assigned for AG {access_group.ag_name}")
            print(f"Permissions sucessfully assigned for AG {access_group.ag_name}")
                

    @staticmethod
    def create_access_groups(people_list, resource):
        logging.info("Creating Access Group...")
        print("Creating Access Group...")
        
        single_users, groups = AccessGroup._create_groupings(people_list, resource)
        iam_token, account_id = AccessGroup._credentials()
        headers = {
                    'Authorization': 'Bearer eyJraWQiOiIyMDE5MDcyNCIsImFsZyI6IlJTMjU2In0.eyJpYW1faWQiOiJJQk1pZC01NTAwMDNZME4yIiwiaWQiOiJJQk1pZC01NTAwMDNZME4yIiwicmVhbG1pZCI6IklCTWlkIiwiaWRlbnRpZmllciI6IjU1MDAwM1kwTjIiLCJnaXZlbl9uYW1lIjoiUHJhdHl1c2giLCJmYW1pbHlfbmFtZSI6IlNpbmdoIiwibmFtZSI6IlByYXR5dXNoIFNpbmdoIiwiZW1haWwiOiJwcmF0eXVzaHNpbmdoQGlibS5jb20iLCJzdWIiOiJwcmF0eXVzaHNpbmdoQGlibS5jb20iLCJhY2NvdW50Ijp7InZhbGlkIjp0cnVlLCJic3MiOiIwNGZkYzYwYTdjMGM0MDRmNTBmZDM0YWFjNzlhZjQ1ZSJ9LCJpYXQiOjE1NzQ4NjU3ODksImV4cCI6MTU3NDg2OTM4OSwiaXNzIjoiaHR0cHM6Ly9pYW0uY2xvdWQuaWJtLmNvbS9pZGVudGl0eSIsImdyYW50X3R5cGUiOiJ1cm46aWJtOnBhcmFtczpvYXV0aDpncmFudC10eXBlOnBhc3Njb2RlIiwic2NvcGUiOiJpYm0gb3BlbmlkIiwiY2xpZW50X2lkIjoiYngiLCJhY3IiOjEsImFtciI6WyJwd2QiXX0.grO2Nz9vMmp0uoDQOVieew7lEue42EXiFEzBcZRsu13ZccFE8OnUNBm0i32AmxBsHyZUPXf3hqNSQgc6sIZT0CeZEFsJMHu3P0xkn8cbc5QXjfGgCGqkEWXGI3cPPk0xoG7EXjtHSIA1XaljtkCY60DZ3ENy2uASL2aQjhI6EEh1JdRjbZ877_sgVWTZ9_XTSI7AFhpCsXzEXycMJciH0NcRqjh3A3iSGwKOs9OJanLGj31G44rAc6OEKIDlcDccUQHR-8TB8IgzWaOdy-oB8CSxXzU4VT_GF0e34AXKDJwlG4uWPe9gn6h-dG8y5TkF-g1HMep1RAj93bm64iyovg',
                    'Content-Type': 'application/json',
                  }

        params = (
                  ('account_id', '04fdc60a7c0c404f50fd34aac79af45e'),
                )       
        
        for group in groups:
                identifier = random.randint(0, 999)
                identifier = str(identifier)
                name = f"Access Group {group[0].service_name}_{identifier}"
                
                data = {'name': name}
                data = json.dumps(data)
                response = requests.post('https://iam.cloud.ibm.com/v2/groups', headers=headers, params=params, data=data)
                
                if response.status_code != 201:
                    raise Exception(response.json())
                    
                
                response_json = response.json()
                access_group = AccessGroup(name, response_json['id'], group)
                AccessGroup.access_grp_list.append(access_group)
                
                logging.info(f'Created access group with the name, {name}')

                for person in group:
                    person.ag = access_group
        
        logging.info('Finished Creating Access Group')
        print("Finished Creating Access Group...")
        print("Adding Members to Access Group...")
        
        
        AccessGroup._add_members(headers)
        AccessGroup._assign_policies(headers, params)
        
        return single_users
    
    
    
                    
    
    
    
    
        
