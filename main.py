import argparse
import os
import pandas as pd

from pathlib import Path

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
        AccessGroup.create_access_groups(Person.person_list, "premium")
        
if __name__ == "__main__":
    main()