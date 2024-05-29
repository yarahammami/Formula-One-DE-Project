from urllib.request import urlopen
import json

response = urlopen('https://api.openf1.org/v1/sessions?session_name=Qualifying')
data = json.loads(response.read().decode('utf-8'))


# Create the JSON file
try:
    with open('RAW/qualifying_data.json', mode='w') as json_file:
        json.dump(data, json_file, indent=4)
    
    print("Data has been successfully written to constructors_data.json")
except:
    print(f"Failed to fetch the files. Status code: {response.status_code}")