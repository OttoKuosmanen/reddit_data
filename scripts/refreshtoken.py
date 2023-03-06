import praw
from praw.models import MoreComments

reddit = praw.Reddit(client_id='52b_-ogrKMs1rpbT0d-TJQ',
                     client_secret='IQF_XzdHCsPHXvWcNqGbD1YCmZurGA', password='reddIt3?',
                     user_agent='advicedata/0.1 by Otto_kuosmanen', username='Otto_kuosmanen')



# INFO
"""Get submissions and comments from a subreddit.

    Args:
        subreddit_name (str): The name of the subreddit.
        limit (int): The maximum number of submissions to retrieve.
        score_limit (int): The minimum score a submission should have.

    Returns:
        Tuple: A tuple containing two lists - submission_list and comment_list.
            submission_list: A list of tuples containing submission data.
            comment_list: A list of comment forests.
    Data:
        Comments and submissions are linked by Index
"""
def get_submissions_and_comments(sub, limitter, score_limit):
    submission_list = []
    comment_forest_list = []
    for submission in reddit.subreddit(sub).new(limit=limitter):
        if submission.score > score_limit:
            submission_data = (submission.title + "\n" + submission.selftext,submission.score, submission.id, submission.url)
            submission_list.append(submission_data)
            comment_forest_list.append(submission.comments)
        
    return submission_list, comment_forest_list

            
submission_list, comment_forest_list = get_submissions_and_comments("advice", 1000, 20)


def remove(comment_forest_list):
    for commentforest in comment_forest_list:
        commentforest.replace_more(limit=0)

remove(comment_forest_list)

  
def get_top_comments(comment_forest_list):
    top_comments = []
    for comment_forest in comment_forest_list:
        comments = []
        for comment in comment_forest:
            comments.append((comment.score, comment.body))
        if comments:
            top_comment = max(comments, key=lambda c: c[0])
            top_comments.append((top_comment[0], top_comment[1]))
    return top_comments       

best_comments = get_top_comments(comment_forest_list)


def compile_list(submission_list, comment_list):
    compiled_list = []
    for submission, comment in zip(submission_list, comment_list):
        compiled_list.append(submission + comment)
    return compiled_list

compiled_list = compile_list(submission_list,best_comments)        
        

def convert_to_dict(compiled_list):
    submissions_dict = {}
    for submission in compiled_list:
        submission_dict = {
            "advice_question": submission[0],
            "score": submission[1],
            "id": submission[2],
            "url": submission[3],
            "answer_score": submission[4],
            "answer": submission[5]
        }
        submissions_dict[submission[2]] = submission_dict
    return submissions_dict


dic = convert_to_dict(compiled_list)
