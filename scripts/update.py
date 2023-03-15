# Update comments of each dict

import praw
import json
from praw.models import MoreComments
from datetime import date, datetime

# initialize access information
reddit = praw.Reddit(client_id='52b_-ogrKMs1rpbT0d-TJQ',
                     client_secret='IQF_XzdHCsPHXvWcNqGbD1YCmZurGA', password='reddIt3?',
                     user_agent='advicedata/0.1 by Otto_kuosmanen', username='Otto_kuosmanen')

# initialize date variable
time_stamp = date.today()
relative_location_name = f'../data/step2/{time_stamp}unique.json'  # file name has to be manually changed
output_file = f'../data/step2/update_file/{time_stamp}unique_up.json'

def read(relative_location_name):
    with open(relative_location_name, 'r') as f:
        out = json.load(f)
        return out


def get_reddit(data):
    comm = []
    score = []
    date = []
    for dicti in data:
        submission = reddit.submission(id = dicti["Id"])
        score.append(submission.score)
        date.append(submission.created_utc)
        out = submission.comments
        out.replace_more(limit=0)
        comm.append(out)
        
    return comm, score, date
    
def time_conversion(datetime_unconverted):
    date_time = []
    for i in datetime_unconverted:
        date_time.append(datetime.utcfromtimestamp(i))
    return date_time



def get_top_comments(comment_forest_list):
    top_comments = []
    for comment_forest in comment_forest_list:
        comments = []
        for comment in comment_forest:
            if len(comment.body.split()) > 30:
                comments.append((comment.score, comment.body))
        if comments:
            top_comment = max(comments, key=lambda c: c[0])
            top_comments.append((top_comment[0], top_comment[1]))
        else:
            top_comments.append(('No comments longer than 30 words', ''))
    return top_comments




def re_compile(data, score, top_comments, comment_scores, date_time):
    for dicti, score, comment, c_score, date_i in zip(data, score, top_comments, comment_scores, date_time):
        dicti['A_score'] = c_score
        dicti['Aswer'] = comment
        dicti['Q_score'] = score
        dicti['Date_of_creation'] = date_i



def clean(data):
    for dicti in data:
        if dicti["A_score"] < 20 or len(dicti["Aswer"].split()) > 1290 or len(dicti["Question"].split()) > 1290:
            data.remove(dicti)

            
    
def save_file(file):
    with open(output_file, 'w') as f:
        json.dump(file, f, indent=4) # by default it will overwrite the last save

#Sequence of functions
        
data = read(relative_location_name)

comment_forest_list, submission_score, datetime_unconverted = get_reddit(data)

date_time = time_conversion(datetime_unconverted)

results = get_top_comments(comment_forest_list)

comment_scores, top_comments = zip(*results)

re_compile(data, submission_score, top_comments, comment_scores, date_time)

clean(data)

save_file(data)
