from yaml import safe_load, YAMLError
import shutil
import os

def populate_jekyll(process_description_path: str, project_path: str):
    jekyll_project_name = project_path.split('/')[-1]
    statics_base_path = 'jekyll_statics/'

    files_to_copy = [
        'index.html', 
        'phase.html', 
        'guideline.html', 
        'activity.html', 
        'template.html', 
        'role.html', 
        'tool.html', 
        'artifact.html'
    ]
    folders_to_copy = [
        '_layouts', 
        '_includes', 
        'assets/css'
    ]

    def create_folder(path, name):
        folder_path = f'{path}/{name}'
        if os.path.isdir(folder_path):
            print(f'{folder_path} already exists. Re-creating it.')
            shutil.rmtree(folder_path)
        
        os.mkdir(folder_path)

    def delete_file(path):
        if os.path.isfile(path):
            os.remove(path)

    def enrich_role_data(raw_data):
        # Add the 'activities that reference it' for each role
        for activity_id, activity in raw_data['activities'].items():
            activity_roles = activity.get('participant_roles', []) + activity.get('responsible_roles', [])
            for role_id in activity_roles:
                if role_id not in raw_data.get('roles', []):
                    continue
                
                raw_data['roles'][role_id].setdefault('activities', []).append(activity_id)

    def create_collection(path, items, layout):
        for identifier, properties in items.items():
            file_path = f'{path}/{identifier}.md'
            delete_file(file_path)

            with open(file_path, 'w') as f:
                f.write('---\n')

                f.write(f'layout: {layout}\n\n')

                f.write(f'pk: {identifier}\n\n')
                for property, values in properties.items():
                    if values is None:
                        f.write(f'{property}:\n')
                    elif isinstance(values, str) or isinstance(values, bool):
                        f.write(f'{property}: {values}\n')
                    elif isinstance(values, list):
                        f.write(f'{property}:\n')
                        for value in values:
                            f.write(f'  - {value}\n')
                    else:
                        raise TypeError(f'"{values}" is not a valid value for the "{property}" property')

                f.write('---')

    def build_activity_graph(activities):
        mermaid_string = '"graph TD\\n'
        solo_activities = set(activities.keys())

        for id, activity in activities.items():
            name = activity['name']

            if activity.get('predecessor') in activities:
                predecessor_id = activity['predecessor']
                predecessor_name = activities[predecessor_id]['name']
                mermaid_string += f' {id}[{name}] --> {predecessor_id}[{predecessor_name}]\\n'

                if id in solo_activities:
                    solo_activities.remove(id)
        
        for id in solo_activities:
            name = activities[id]['name']
            mermaid_string += f' {id}[{name}]\\n'
        
        return mermaid_string + '"'

    def fill_config_file(path, collections, global_variables):
        delete_file(path)
        
        with open(path, 'a') as f:
            for key, value in global_variables.items():
                f.write(f'{key}: {value}\n')
            
            f.write('\ncollections:\n')
            for collection in collections:
                f.write(f'  {collection}:\n')
                f.write(f'    output: true\n')

    def copy_statics_to_project(dest_path, files, folders):
        statics_dir = os.getcwd() + f'/{statics_base_path}' # TO-DO: Change this to not use the current dir
        create_folder(dest_path, 'assets')

        for file in files:
            delete_file(f'{dest_path}/{file}')
            shutil.copyfile(f'{statics_dir}/{file}', f'{dest_path}/{file}')
        
        for folder in folders:
            create_folder(dest_path, folder)
            
            for _, _, folder_files in os.walk(f'{statics_dir}/{folder}'):
                for file in folder_files:
                    shutil.copyfile(f'{statics_dir}/{folder}/{file}', f'{dest_path}/{folder}/{file}')

    jekyll_global_variables = {}

    if not os.path.exists(project_path):
        # Init Jekyll project
        os.system(f'jekyll new {jekyll_project_name}')

        # Remove template files
        os.remove(f'{project_path}/404.html')
        os.remove(f'{project_path}/about.markdown')
        os.remove(f'{project_path}/index.markdown')

    # Read .yml file
    raw_data = {}
    with open(process_description_path, 'r') as stream:
        try:
            raw_data = safe_load(stream)
        except YAMLError as exc:
            print(exc)

    jekyll_global_variables['process_name'] = raw_data.pop('process_name')
    jekyll_global_variables['process_description'] = raw_data.pop('process_description')

    # Create collections
    enrich_role_data(raw_data)
    entities = raw_data.keys()
    for entity in entities:
        collection_name = f'_{entity}'
        create_folder(project_path, collection_name)

        collection_path = f'{project_path}/{collection_name}'
        create_collection(collection_path, raw_data[entity], entity)
        print(f'Created {entity} collection successfully')

    # Fill _config.yml file
    jekyll_global_variables['activity_graph'] = build_activity_graph(raw_data.get('activities', []))
    config_path = f'{project_path}/_config.yml'
    fill_config_file(config_path, entities, jekyll_global_variables)

    # Copy static files
    copy_statics_to_project(project_path, files_to_copy, folders_to_copy)