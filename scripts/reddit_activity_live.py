import praw
import numpy as np
import sys
sys.path.append('../KEY')
from key import client_id, client_secret, password, user_agent, username

# Getting access to reddit
reddit = praw.Reddit(client_id = client_id,
                     client_secret = client_secret, password = password,
                     user_agent = user_agent, username = username)

# Initialize parameters for search
sub_reddit = "advice"
number_of_posts = 1000
score_limit = 0
day_minutes = 1440

#Function: gets submission time
#Parameters: sub= subreddit, limitter = number of posts, score_limit = minimum score
#Returns: list of submission times (UNIX TIME)
def get_sub_time(sub, limitter, score_limit):
    submission_time = []
    for submission in reddit.subreddit(sub).new(limit=limitter):
        if submission.score > score_limit:
            time = (submission.created_utc)
            submission_time.append(time)
            
    return submission_time


# Running the get_sub_time function.
# taking a copy of it without the first element. (For time comparisons)
time_line = get_sub_time(sub_reddit,number_of_posts,score_limit)
time_snap = time_line[1:]

#Function: calculates the time between all posts
#Parameters: Pass in list of all times and a copy without the first element.
#Return: List of times between posts
def time_between_posts(full_time_list,substraction_time_list):
    time_between = []
    for time, time_s in zip(full_time_list, substraction_time_list):
        between = time - time_s
        time_between.append(between)
        
    return time_between

# Running the time_between posts function
time_between_posts = time_between_posts(time_line, time_snap)

# Calculating the average time between posts in minutes
average = np.mean(time_between_posts) / 60

post_in_day = day_minutes / average

# Printing the average time between posts
print(average) 
print(post_in_day)