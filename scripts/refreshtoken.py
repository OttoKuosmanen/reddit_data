#Get access token

import praw
import pandas as pd

reddit = praw.Reddit(client_id='52b_-ogrKMs1rpbT0d-TJQ',
                     client_secret='IQF_XzdHCsPHXvWcNqGbD1YCmZurGA', password='reddIt3?',
                     user_agent='advicedata/0.1 by Otto_kuosmanen', username='Otto_kuosmanen')

subreddit = reddit.subreddit('advice') # state subreddit
tag = []
selftext = []
top_advice = []
top_submissions = subreddit.top(limit=10)

for submission in top_submissions:
    if submission.score > 100:
        tag.append(submission.id)
        question = submission.title + "\n" + submission.selftext
        selftext.append(question)
        question = ""




 #Sort the comments in the forest by score and get the top comment

submission_id = tag[0]
submission = reddit.submission(id=submission_id)
top_comment = sorted(submission.comments, key=lambda comment: comment.score, reverse=True)[0]
top_advice.append(top_comment.body)
    
