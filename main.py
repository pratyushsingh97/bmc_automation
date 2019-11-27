from pathlib import Path

import argparse
import os
import pandas as pd

from person import Person

from access_group import AccessGroup
import permissions


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--premium', type=str)
    parser.add_argument('--non_premium', type=str)
    
    args = vars(parser.parse_args())
    premium_fp = args['premium']
    non_premium_fp = args['non_premium']
    
    if premium_fp:
        premium(premium_fp)
    
    if non_premium_fp:
        non_premium(non_premium_fp)

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
                        'Authorization': 'Bearer eyJraWQiOiIyMDE5MDcyNCIsImFsZyI6IlJTMjU2In0.eyJpYW1faWQiOiJJQk1pZC01NTAwMDNZME4yIiwiaWQiOiJJQk1pZC01NTAwMDNZME4yIiwicmVhbG1pZCI6IklCTWlkIiwiaWRlbnRpZmllciI6IjU1MDAwM1kwTjIiLCJnaXZlbl9uYW1lIjoiUHJhdHl1c2giLCJmYW1pbHlfbmFtZSI6IlNpbmdoIiwibmFtZSI6IlByYXR5dXNoIFNpbmdoIiwiZW1haWwiOiJwcmF0eXVzaHNpbmdoQGlibS5jb20iLCJzdWIiOiJwcmF0eXVzaHNpbmdoQGlibS5jb20iLCJhY2NvdW50Ijp7InZhbGlkIjp0cnVlLCJic3MiOiIwNGZkYzYwYTdjMGM0MDRmNTBmZDM0YWFjNzlhZjQ1ZSJ9LCJpYXQiOjE1NzQ4NjU3ODksImV4cCI6MTU3NDg2OTM4OSwiaXNzIjoiaHR0cHM6Ly9pYW0uY2xvdWQuaWJtLmNvbS9pZGVudGl0eSIsImdyYW50X3R5cGUiOiJ1cm46aWJtOnBhcmFtczpvYXV0aDpncmFudC10eXBlOnBhc3Njb2RlIiwic2NvcGUiOiJpYm0gb3BlbmlkIiwiY2xpZW50X2lkIjoiYngiLCJhY3IiOjEsImFtciI6WyJwd2QiXX0.grO2Nz9vMmp0uoDQOVieew7lEue42EXiFEzBcZRsu13ZccFE8OnUNBm0i32AmxBsHyZUPXf3hqNSQgc6sIZT0CeZEFsJMHu3P0xkn8cbc5QXjfGgCGqkEWXGI3cPPk0xoG7EXjtHSIA1XaljtkCY60DZ3ENy2uASL2aQjhI6EEh1JdRjbZ877_sgVWTZ9_XTSI7AFhpCsXzEXycMJciH0NcRqjh3A3iSGwKOs9OJanLGj31G44rAc6OEKIDlcDccUQHR-8TB8IgzWaOdy-oB8CSxXzU4VT_GF0e34AXKDJwlG4uWPe9gn6h-dG8y5TkF-g1HMep1RAj93bm64iyovg',
                        'Content-Type': 'application/json',
                    }

                params = (
                        ('account_id', '04fdc60a7c0c404f50fd34aac79af45e'),
                        ) 
            
                for single_user in single_users:
                    single_user = single_user[0]
                    permissions.assign_policies(single_user, headers, params, "non premium")
        
        
    
def premium(fp):
    if _does_file_exist(fp) and _is_csv(fp):
        print("Starting the process for assigning permissions in premium offerings...")
        
        people_df = pd.read_csv(fp)
        
        for _, people in people_df.iterrows():
            ibm_id = people['ibm_id']
            service_name = people['service_name']
            service_inst = people['service_instance']
            
            platform_viewer = people['platform_viewer']
            platform_editor = people['platform_editor']
            platform_admin = people['platform_admin']
            
            service_reader = people['service_reader']
            service_writer = people['service_writer']
            service_manager = people['service_manager']
            
            # creating a Person object with these attributes
            person = Person(ibm_id,
                            service_name,
                            service_inst,
                            platform_viewer,
                            platform_editor,
                            platform_admin,
                            service_reader,
                            service_writer,
                            service_manager)
            
            Person.person_list.append(person)
        
        # Create the access groups 
        single_users = AccessGroup.create_access_groups(Person.person_list, "premium")
        
        if len(single_users): # now assign permissions to a single group of users
            headers = {
                    'Authorization': 'Bearer eyJraWQiOiIyMDE5MDcyNCIsImFsZyI6IlJTMjU2In0.eyJpYW1faWQiOiJJQk1pZC01NTAwMDNZME4yIiwiaWQiOiJJQk1pZC01NTAwMDNZME4yIiwicmVhbG1pZCI6IklCTWlkIiwiaWRlbnRpZmllciI6IjU1MDAwM1kwTjIiLCJnaXZlbl9uYW1lIjoiUHJhdHl1c2giLCJmYW1pbHlfbmFtZSI6IlNpbmdoIiwibmFtZSI6IlByYXR5dXNoIFNpbmdoIiwiZW1haWwiOiJwcmF0eXVzaHNpbmdoQGlibS5jb20iLCJzdWIiOiJwcmF0eXVzaHNpbmdoQGlibS5jb20iLCJhY2NvdW50Ijp7InZhbGlkIjp0cnVlLCJic3MiOiIwNGZkYzYwYTdjMGM0MDRmNTBmZDM0YWFjNzlhZjQ1ZSJ9LCJpYXQiOjE1NzQ4NzU0NjAsImV4cCI6MTU3NDg3OTA2MCwiaXNzIjoiaHR0cHM6Ly9pYW0uY2xvdWQuaWJtLmNvbS9pZGVudGl0eSIsImdyYW50X3R5cGUiOiJ1cm46aWJtOnBhcmFtczpvYXV0aDpncmFudC10eXBlOnBhc3Njb2RlIiwic2NvcGUiOiJpYm0gb3BlbmlkIiwiY2xpZW50X2lkIjoiYngiLCJhY3IiOjEsImFtciI6WyJwd2QiXX0.JXhI23ft5Vlz_km_W02q1z8Ncs9X1uAbrwhv491ZhJ52tmwshzI3VUW29KgOuIX_t4263eSaGEkSH5n9omdAUiotLDcwPWAZ4uehA-m5ShZvxbBfyuU10yfVHpskeRviw6qpqjGEXag6pzVbb-qBCTQe89d3YFoQqbKLfjNXN55clCYKhEjZQgf4CRR6bk6SvwS_5ur0ByRYOh-m8lINolSFjmfghKITWle0ukBXidkDpHzdUXBCVh31Lh6JdLwP2ZGVUePBQ4B96DQHDhOJmY5qdxpC5NMLDo1Dcn2PrTUVBXbjOSooLe0_Dm1ikmIVecpGSEa8kE1JbdqEN0fLOQ',
                    'Content-Type': 'application/json',
                  }

            params = (
                    ('account_id', '04fdc60a7c0c404f50fd34aac79af45e'),
                    ) 
            
            for single_user in single_users:
                single_user = single_user[0]
                permissions.assign_policies(single_user, headers, params, "premium")
                
            
        
if __name__ == "__main__":
    main()