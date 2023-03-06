""" Reads in all json files in the data folder.
    Creates a list of dictionaries.
    Removes duplicates and compiles it into another json file.
"""

import os,json

path_to_json = '../data/'

def read():
    out = []
    for file_name in [file for file in os.listdir(path_to_json) if file.endswith('.json')]:
        with open(path_to_json + file_name) as json_file:
            data = json.load(json_file)
            out.append(data)
    return out

data = read()
           
def simplify(data): #combine files so that iteration is easy




def uni(data): # returns only items with unique id's
    for file in data:
        


def json_final # takes the file and creates a new json file