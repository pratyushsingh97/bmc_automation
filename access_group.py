import random
import requests
import io
import json
import logging

from configparser import ConfigParser

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
                platform_admin = person.platform_admin
                    
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
                print(member)
                if member['status_code'] != 200:
                    msg = f"{member.iam_id} not added to access group, {access_group.ag_name}. Result returned error, {member.message} with code {member.code}"
            

            
    @staticmethod
    def _assign_policies(headers):
        data = {"type": "access", "subjects": [{"attributes": [{"name": "access_group_id", "value": "AccessGroupId-e1c759ab-94d6-46e7-af84-f4d6ce6e1313"}]}], 
                                                "roles":[{"role_id": "crn:v1:bluemix:public:iam::::role:Editor"}, {"role_id":"crn:v1:bluemix:public:iam::::serviceRole:Writer"}], 
                                                "resources":[{"attributes": [{"name": "accountId","value": "04fdc60a7c0c404f50fd34aac79af45e"}, 
                                                                             {"name": "serviceName", "value": "natural-language-understanding"}, 
                                                                             {"name": "serviceInstance", "value":"f9666752-5b94-4d0d-84d2-c51cf104f027"}]}]}
        response = requests.post('https://iam.cloud.ibm.com/v1/policies', headers=headers, data=data)

    @staticmethod
    def create_access_groups(people_list, resource):
        print("Creating Access Group...")
        
        single_users, groups = AccessGroup._create_groupings(people_list, resource)
        iam_token, account_id = AccessGroup._credentials()
        headers = {
                    'Authorization': 'Bearer eyJraWQiOiIyMDE5MDcyNCIsImFsZyI6IlJTMjU2In0.eyJpYW1faWQiOiJJQk1pZC01NTAwMDNZME4yIiwiaWQiOiJJQk1pZC01NTAwMDNZME4yIiwicmVhbG1pZCI6IklCTWlkIiwiaWRlbnRpZmllciI6IjU1MDAwM1kwTjIiLCJnaXZlbl9uYW1lIjoiUHJhdHl1c2giLCJmYW1pbHlfbmFtZSI6IlNpbmdoIiwibmFtZSI6IlByYXR5dXNoIFNpbmdoIiwiZW1haWwiOiJwcmF0eXVzaHNpbmdoQGlibS5jb20iLCJzdWIiOiJwcmF0eXVzaHNpbmdoQGlibS5jb20iLCJhY2NvdW50Ijp7InZhbGlkIjp0cnVlLCJic3MiOiIwNGZkYzYwYTdjMGM0MDRmNTBmZDM0YWFjNzlhZjQ1ZSJ9LCJpYXQiOjE1NzQ4NDU0MDksImV4cCI6MTU3NDg0OTAwOSwiaXNzIjoiaHR0cHM6Ly9pYW0uY2xvdWQuaWJtLmNvbS9pZGVudGl0eSIsImdyYW50X3R5cGUiOiJ1cm46aWJtOnBhcmFtczpvYXV0aDpncmFudC10eXBlOnBhc3Njb2RlIiwic2NvcGUiOiJpYm0gb3BlbmlkIiwiY2xpZW50X2lkIjoiYngiLCJhY3IiOjEsImFtciI6WyJwd2QiXX0.lYpGg_zAACUXYD85n_--uQAThEQcq7iSMJWeNq3eZyFY2yk3rrjzSUI9j67HJGNd7L9EOkNr_0WqAFak-ZJMNpbtqGqXo4LccjG2MfgCmg4CwyEQaflAxVlz7AKS0viln0BbVSkdu00w5Fbz2yGGubuyCOqI5BxA41wasMAFh-btr7Vx0p80xKWtmviqbIK0IMVVGrfDxx-u61vnznOx_wLUcMd-3IRoxLRk1CASfJfVQWa8NBsOUO2ePjpmCifQxSvpES_C_cX59LHxWNtA95_mdKijhStnKODdANwSrK0R0dD5wEVtGdYM-5RuWF4-cQQLRpudUbpz3fnXVOmG-Q',
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

                for person in group:
                    person.ag = access_group
        
        print("Finished Creating Access Group...")
        print("Adding Members to Access Group...")
        
        AccessGroup._add_members(headers)
    
    
    
                    
    
    
    
    
        
