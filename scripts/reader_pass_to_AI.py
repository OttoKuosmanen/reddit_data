
import json
from datetime import date
time_stamp = date.today()

relative_location_name = f'../data/step2/update_file/{time_stamp}unique_up.json'

def read(relative_location_name):
    with open(relative_location_name, 'r') as f:
        out = json.load(f)
        return out


analysis_data = read(relative_location_name)



def extract_questions(analysis_data):
    out = []
    for dicti in analysis_data:
        out.append(dicti["Question"])
    return out
        
    

questions = extract_questions(analysis_data) 