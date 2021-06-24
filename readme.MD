zendesk assignment.

clone repo

run main.py

the program will read all json files in current directory or in path specified. and list them dynamically. all this will be done as soon as the program launches.

the ProgramState object is used to keep track of all files, results, and files chosen to search on. 

read menu options carefully.

only exact value matches will be returned

input limit set at 50 characters

help, quit, save, results  commands work at any point in program execution

each result will have 3 additional fields, file: the file the result is from, matchedon: the feature it was matched on, matched_on_value = the value it was matched on

each result will also have results that cross match with other files
(this is done under the assumption that ids do not overlap)

searching all files will return all results with a matching data

I have not done unit testing since I used up all the time to build this. I infact built another app but was not satisfied with it so i built this. I can do unit testing if I'm given more time. 

Looking back I would've improved the modularity a lot more making the methods cleaner. 