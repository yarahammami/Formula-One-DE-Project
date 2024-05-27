import requests
import yaml
import json

# FETCHING ALL CIRCUITS YML FILES
# GitHub repository details
owner = 'f1db'  
repo = 'f1db' 
path = 'src/data/constructors' 
branch = 'main'

# GitHub API URL to list contents of the folder
url = f'https://api.github.com/repos/{owner}/{repo}/contents/{path}?ref={branch}'

# Fetch the list of files in the folder
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    files = response.json()
    
    # Dictionary to store YAML file names
    yaml_files = {}
    
    # Filter and store YAML files
    for file in files:
        if file['name'].endswith('.yaml') or file['name'].endswith('.yml'):
            yaml_files[file['name']] = file['download_url']  # storing file name and download URL

    # FETCHING THE CIRCUITS DATA
    # List to store all rows of data
    all_data = []
    
    # Download and parse each YAML file
    for name, url in yaml_files.items():
        file_response = requests.get(url)
        
        if file_response.status_code == 200:
            yaml_content = file_response.text
            data = yaml.safe_load(yaml_content)
            
            # Append data to the list
            all_data.append(data)
        else:
            print(f"Failed to fetch the file {name}. Status code: {file_response.status_code}")
    
    # Create the JSON file
    with open('RAW/constructors_data.json', mode='w') as json_file:
        json.dump(all_data, json_file, indent=4)
    
    print("Data has been successfully written to constructors_data.json")
else:
    print(f"Failed to fetch the files. Status code: {response.status_code}")
