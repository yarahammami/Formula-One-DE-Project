import requests
import yaml
import csv

#FETCHING ALL CIRCUITS YML FILES
# GitHub repository details
owner = 'f1db'  
repo = 'f1db' 
path = 'src/data/circuits' 
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
    
    # Set of all headers
    all_headers = set()
    
    # Download and parse each YAML file
    for name, url in yaml_files.items():
        file_response = requests.get(url)
        
        if file_response.status_code == 200:
            yaml_content = file_response.text
            data = yaml.safe_load(yaml_content)
            
            # Collect headers
            all_headers.update(data.keys())
            
            # Append data to the list
            all_data.append(data)
        else:
            print(f"Failed to fetch the file {name}. Status code: {file_response.status_code}")
    
    # Create the CSV file
    with open('circuits_data.csv', mode='w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=list(all_headers))
        
        # Write the headers
        writer.writeheader()
        
        # Write the data rows
        for data in all_data:
            writer.writerow(data)
    
    print("Data has been successfully written to circuits_data.csv")
else:
    print(f"Failed to fetch the files. Status code: {response.status_code}")