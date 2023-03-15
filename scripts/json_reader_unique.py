""" Reads in all json files in the data folder.
    Creates a list of dictionaries.
    Removes duplicates and compiles it into another json file.
"""

import os,json
from datetime import date

# initialize date for data outputs
time_stamp = date.today()

#initiallize path to input and output
path = '../data/'
output_file = f'../data/step2/{time_stamp}unique.json'



# Reads all the json files in folder: set to path variable. Stores the data as output.
def read():
    out = []
    for file_name in [file for file in os.listdir(path) if file.endswith('.json')]:
        with open(path + file_name) as json_file:
            data = json.load(json_file)
            out.append(data)
    return out

#combine files so that iteration is easy           
def simplify(data):
    out = []
    for file in data:
        for dic in file["Posts"]:
            out.append(dic)
    return out
            
        
# returns only items with unique id's
def uni(new):
    out = []
    id_seen = []
    for dic in new:
        if dic["Id"] not in id_seen:
            id_seen.append(dic["Id"])
            out.append(dic)
    return out

#saves file in json format
def save_file(file):
    with open(output_file, 'w') as f:
        json.dump(unique, f, indent=4) # by default it will overwrite the last save


#running functions in sequence
data = read()
simple_data = simplify(data)
unique = uni(simple_data)
save_file(unique)

