import argparse
import os
import pandas as pd

from pathlib import Path

import permissions

from person import Person
from access_group import AccessGroup


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--premium', type=str)
    parser.add_argument('--non_premium', type=str)
    
    args = vars(parser.parse_args())
    premium_fp = args['premium']
    non_premium_fp = args['non_premium']
    
    if premium_fp:
        premium(premium_fp)
    
    # @TODO: Develop this part when I get to the non premium part 
    if non_premium_fp:
        non_premium_fp(non_premium_fp)

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

#def _get_access_group
    
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
            
            # creatinig a Person object with these attributes
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
                    'Authorization': 'Bearer eyJraWQiOiIyMDE5MDcyNCIsImFsZyI6IlJTMjU2In0.eyJpYW1faWQiOiJJQk1pZC01NTAwMDNZME4yIiwiaWQiOiJJQk1pZC01NTAwMDNZME4yIiwicmVhbG1pZCI6IklCTWlkIiwiaWRlbnRpZmllciI6IjU1MDAwM1kwTjIiLCJnaXZlbl9uYW1lIjoiUHJhdHl1c2giLCJmYW1pbHlfbmFtZSI6IlNpbmdoIiwibmFtZSI6IlByYXR5dXNoIFNpbmdoIiwiZW1haWwiOiJwcmF0eXVzaHNpbmdoQGlibS5jb20iLCJzdWIiOiJwcmF0eXVzaHNpbmdoQGlibS5jb20iLCJhY2NvdW50Ijp7InZhbGlkIjp0cnVlLCJic3MiOiIwNGZkYzYwYTdjMGM0MDRmNTBmZDM0YWFjNzlhZjQ1ZSJ9LCJpYXQiOjE1NzQ4NjU3ODksImV4cCI6MTU3NDg2OTM4OSwiaXNzIjoiaHR0cHM6Ly9pYW0uY2xvdWQuaWJtLmNvbS9pZGVudGl0eSIsImdyYW50X3R5cGUiOiJ1cm46aWJtOnBhcmFtczpvYXV0aDpncmFudC10eXBlOnBhc3Njb2RlIiwic2NvcGUiOiJpYm0gb3BlbmlkIiwiY2xpZW50X2lkIjoiYngiLCJhY3IiOjEsImFtciI6WyJwd2QiXX0.grO2Nz9vMmp0uoDQOVieew7lEue42EXiFEzBcZRsu13ZccFE8OnUNBm0i32AmxBsHyZUPXf3hqNSQgc6sIZT0CeZEFsJMHu3P0xkn8cbc5QXjfGgCGqkEWXGI3cPPk0xoG7EXjtHSIA1XaljtkCY60DZ3ENy2uASL2aQjhI6EEh1JdRjbZ877_sgVWTZ9_XTSI7AFhpCsXzEXycMJciH0NcRqjh3A3iSGwKOs9OJanLGj31G44rAc6OEKIDlcDccUQHR-8TB8IgzWaOdy-oB8CSxXzU4VT_GF0e34AXKDJwlG4uWPe9gn6h-dG8y5TkF-g1HMep1RAj93bm64iyovg',
                    'Content-Type': 'application/json',
                  }

            params = (
                    ('account_id', '04fdc60a7c0c404f50fd34aac79af45e'),
                    ) 
            
            for single_user in single_users:
                single_user = single_user[0]
                permissions.assign_permissions_premium(single_user, params, headers)
                
            
        
if __name__ == "__main__":
    main()