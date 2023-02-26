#Get access token

import praw
reddit = praw.Reddit(client_id='52b_-ogrKMs1rpbT0d-TJQ',
                     client_secret='IQF_XzdHCsPHXvWcNqGbD1YCmZurGA', password='reddIt3?',
                     user_agent='advicedata/0.1 by Otto_kuosmanen', username='Otto_kuosmanen')

subreddit = reddit.subreddit('advice')
hot_advice = subreddit.hot()

hot_advice = subreddit.hot(limit=1)
for submission in hot_advice:
    print(submission.title, 20*"-", submission.selftext)

comments = submission.comments
for comment in comments:
    if comment.ups > 200:
        print(20*"-")
        print(comment.body)