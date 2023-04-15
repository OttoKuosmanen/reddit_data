# Made by: Otto Kuosmanen

This is a scripted procedure for getting advice data from Reddit and building a data file for research.

I wanted to make a data file with advice data from reddit that had at least 20 upvotes in the post.
It saves the best answer to this advice question, rating of the answer, rating of the post, id, url, time of creation, lenght of the answer and post.

#important: before gaining using the scripts you need to make a account to reddit and follow the steps in the KEY folder. (GAIN ACCESS)

# RUN order: reddit.py, json_reader_unique, update, clean.

Because the reddit API has a limit of 1000 posts per search.
With the settings that i had, 1000 posts, minimum rating 20. The average yield of suitable posts were 20.
I ran the reddit.py script for many days in a row. Each day i got many new suitable posts.

After there were many files in the data folder. Some of the posts were identical. I made the json_reader_unique.
This script reads all the posts in the data folder and creates a new data file with no idetical posts in the data/step2 folder.

Some because time is running during the data collection and some posts change i created the update script. 
Aditionally in the update script i get the best comment of each posts and set some criteria for inclusion.
Running the update script reads the unique data file that was created at the time of executing the update script. (Needs to be run on the same day)
The script outputts another data file into data/step2/update_file folder.

lastly the clean script was written to clean up the data based on some criteria. Running this file excldes some items from the data.
It also runs a basic statistical analysis and gives out a receipt file.
Theese files are the final result of the procedure and are found in the /data/step2/update_file/final folder.

This scripted procedure is not the most elegant but works well and can easily be adjusted for other purpouses with little tinkering.

# have fun!


