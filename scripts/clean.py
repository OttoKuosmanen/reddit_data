import numpy as np
import json
from datetime import date
time_stamp = date.today()


                # INFORMATION
""" This is a script for cleaning the data.
    Here you can adjust final limits to lenght and censor questions 
    that are not wanted in the final items.
    
    By default it loads today's output of the update script. location: data/step2/update_file
    you can adjust it below'
"""
                #_______________

#INPUT
# Specify name of file if you are not running today's output of update script.
relative_location_name = f'../data/step2/update_file/{time_stamp}unique_up.json'

#OUTPUT
output_file = f'../data/step2/update_file/final/{time_stamp}clean.json'
stamp_file = f'../data/step2/update_file/final/{time_stamp}stamp.json'

# Specify exclusion words
exclude = ["abuse","abused", "abusing","assault","assaulted","assaulting",
           "rape","raped","raping","molest","molested","molesting",
           "suicide","suicidal","kill","killer","killing","update","edit","UPDATE:","edit:"]

# Specify minimum and maximum lenght of answer and question
min_question = 32
max_question = 500
min_answer = 32
max_answer = 400
score_min = 20



""" FUNCTIONS """
# Reads in a json file.
def read(relative_location_name):
    with open(relative_location_name, 'r') as f:
        out = json.load(f)
        return out
    

#Function: makes a list of advice questions
#Parameter: Pass in the data
#Returns: A list of advice questions
def extract_questions(data):
    out = []
    for dicti in data:
        out.append(dicti["Question"])
    return out

#Function: makes a list of advice answers
#Parameter: Pass in the analysis data
#Returns: A list of advice answers
def extract_answers(data):
    out = []
    for dicti in data:
        out.append(dicti["Aswer"])
    return out

#Function: makes a list of advice scores
#Parameter: Pass in the analysis data
#Returns: A list of advice scores
def extract_score(data):
    out = []
    for dicti in data:
        out.append(dicti["A_score"])
    return out

#Function: counts how many words are in a list of strings
#Parameter: Pass in a list of strings
#Returns: returns a list of numbers corresponding to the number of words in each string
def count_word(list_of_strings):
    words_list = []
    for string in list_of_strings:
        words = string.split()
        n = len(words)
        words_list.append(n)
    return words_list


#Function: pushes info on word count into the original datafile
#Parameter: pass in the data file (loaded with the first function), list of word counts for both answer and question.
#Result: makes changes to the original data file (in code not in file)
def add_info(data, answer_count, question_count):
    for dicti, count_a, count_q in zip(data, answer_count,question_count):
        dicti['answer_len'] = count_a
        dicti['question_len'] = count_q
    

    

#Function: Checks if the advice questions include the specified words. 
#Parameter: Pass in a list of advice questions and a list of words that you want to check for.
#Returns: An equally long list of advice questions but the questions containing the exclusion words are replaced with REMOVE
def sensor(questions, exclude):
    results = []
    for q in questions:
        text = q.upper()
        if not any(item.upper() in text for item in exclude):
            results.append(q)
        else:
            results.append("REMOVE")
    return results

#Function: Checks if a number falls between the mini and maxi parameters
#Parameter: Pass in a list of numbers
#Returns: returns the list of numbers but replaces numbers that are larger than maxi or smaller than mini with REMOVE
def word_minmax(words_length, mini, maxi):
    results = []
    for n in words_length:
        if n < mini or n > maxi:
            results.append("REMOVE")
        else:
            results.append(n)
    return results

#Function: Checks if a number falls between the mini and maxi parameters
#Parameter: Pass in a list of numbers
#Returns: returns the list of numbers but replaces numbers that are larger than maxi or smaller than mini with REMOVE
def min_score(answer_scores, score_min):
    results = []
    for n in answer_scores:
        if n < score_min:
            results.append("REMOVE")
        else:
            results.append(n)
    return results



#Function: Checks the item sequence for any reasons to delete data
#Parameter: Pass in a all checks of deletion
#Returns: a list of 0's and 1's (0 = delete, 1 = good to go)
def check(questions_length_ok, answers_length_ok, sensored_questions, answer_scores_ok):
    deletion_sequence = []
    for a, b, c, d in zip(questions_length_ok, answers_length_ok, sensored_questions,answer_scores_ok):
        if "REMOVE" in str(a) or "REMOVE" in str(b) or "REMOVE" in str(c) or "REMOVE" in str(d):
            deletion_sequence.append(0)
        else:
            deletion_sequence.append(1)
    return deletion_sequence


#Function: Deletes the dictionaries in the datafile that were marked for deletion
#Parameter: Pass in deletion_sequence and the original data file
#Result: this will modify the file directly, only leaving dictionaries that have passed all the criteria
def delete(delete, data):
    new_data = []
    for mark, dicti in zip(delete,data):
        if mark == 0:
            pass
        else:
            new_data.append(dicti)
    return new_data

def stamp(information_wanted):
    with open(stamp_file, 'w') as f:
        json.dump(information_wanted,f,indent=4)

            
def save_file(file):
    with open(output_file, 'w') as f:
        json.dump(file, f, indent=4)
    
"""PROGRAM SEQUENCE"""

#Loading the data
data = read(relative_location_name)

    
# Extracting questions and answers
questions = extract_questions(data)
answers_h = extract_answers(data)
answer_scores = extract_score(data)

# Counting how many words are in answers and questions
words_answer = count_word(answers_h)
words_question = count_word(questions)

# updating the data file with word counts
add_info(data, words_answer, words_question)

# Checking the mean number of words, standard deviation and number of items
mean_answer_score = np.mean(answer_scores)
mean_answer = np.mean(words_answer)
mean_question = np.mean(words_question)
std_answer_score = np.std(answer_scores)
std_answer = np.std(words_answer)
std_question = np.std(words_question)
max_answer_score = np.max(answer_scores)
longest_answer = np.max(words_answer)
longest_question = np.max(words_question)
least_answer_score = np.min(answer_scores)
shortest_answer = np.min(words_answer)
shortest_question = np.min(words_question)
number = len(data)   

# Perform exclusion scan
sensored_questions = sensor(questions,exclude)


# Running the lenght analysis and score checking
questions_lenght_ok = word_minmax(words_question, min_question, max_question)
answers_lenght_ok = word_minmax(words_answer, min_answer, max_answer)
answer_scores_ok = min_score(answer_scores, score_min)

# Running the check function to get the cumulative list of items to be deleted
deletion = check(questions_lenght_ok, answers_lenght_ok, sensored_questions, answer_scores_ok)

# Performing deletion
new = delete(deletion, data)


""" RE-RUNNING a segment of the code sequence"""  # This is to get information for the "receipt" = stamp_file


# Extracting questions and answers
questions_new = extract_questions(new)
answers_h_new = extract_answers(new)
answer_scores_new = extract_score(new)

# Counting how many words are in answers and questions
words_answer = count_word(answers_h_new)
words_question = count_word(questions_new)


# Checking the mean number of words and standard deviation
mean_answer_score_new = np.mean(answer_scores_new)
mean_answer_new = np.mean(words_answer)
mean_question_new = np.mean(words_question)
std_answer_score_new = np.std(answer_scores_new)
std_answer_new = np.std(words_answer)
std_question_new = np.std(words_question)
max_answer_score_new = np.max(answer_scores_new)
longest_answer_new = np.max(words_answer)
longest_question_new = np.max(words_question)
least_answer_score_new = np.min(answer_scores_new)
shortest_answer_new = np.min(words_answer)
shortest_question_new = np.min(words_question)
number_new = len(new)




""" RECEIPT """

information_wanted = {
    'word parameters' : {'excluded': exclude,
                         'minimum length question': str(min_question), 
                         'maximum length question': str(max_question),
                         'minimum length answer': str(min_answer),
                         'maximum length answer': str(max_answer)
                         },
    
    'before' : {    'mean length of answer':  str(mean_answer),
                    'mean length of question': str(mean_question),
                    'mean answer score': str(mean_answer_score),
                    'std answer score': str(std_answer_score),
                    'std question': str(std_question),
                    'std_answer': str(std_answer),
                    'max answer score': str(max_answer_score),
                    'longest answer': str(longest_answer),
                    'longest question': str(longest_question),
                    'min answer score': str(least_answer_score),
                    'shortest answer': str(shortest_answer),
                    'shortest question': str(shortest_question),
                    'number of items': str(number)
                },
                         
    'after': {      'mean length of answer': str(mean_answer_new),
                    'mean length of question': str(mean_question_new),
                    'mean answer score': str(mean_answer_score_new),
                    'std answer score': str(std_answer_score_new),
                    'std question': str(std_question_new),
                    'std_answer': str(std_answer_new),
                    'max answer score': str(max_answer_score_new),
                    'longest answer': str(longest_answer_new),
                    'longest question': str(longest_question_new),
                    'min answer score': str(least_answer_score_new),
                    'shortest answer': str(shortest_answer_new),
                    'shortest question': str(shortest_question_new),
                    'number of items':str(number_new)
        
                }    
    
   
    }

stamp(information_wanted)
save_file(new)


"""END"""