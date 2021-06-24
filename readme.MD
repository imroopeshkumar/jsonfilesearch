zendesk assignment.
-------------steps-----------------------
clone repo

run main.py

the program will read all json files in current directory or in path specified. and list them dynamically. all this will be done as soon as the program launches.

----------------assumptions/ design choices-------------------

the ProgramState object is used to keep track of all files, results, and files chosen to search on. 

the handler2.py file houses all the logic. and since there is only one state object, it is being passed around the program and the stated is read and updated all the time. 

read menu options carefully.

for field search, leaving field empty will search all fields

only exact value matches will be returned

input limit set at 50 characters

help, quit, save, results  commands work at any point in program execution

each result will have 3 additional fields, file: the file the result is from, matchedon: the feature it was matched on, matched_on_value = the value it was matched on

each result will also have results that cross match with other files
(this is done under the assumption that ids do not overlap)

searching all files will return all results with a matching data

duplicates are also listed

----------------------------aftermath--------------------------

Since my class does not have any methods, i have skipped unit testing 

Looking back I would've improved the modularity a lot more making the methods cleaner. 

