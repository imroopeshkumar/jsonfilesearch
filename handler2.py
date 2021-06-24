import json
from state2 import Result
import os
import sys
from state2 import ProgramState, dataobject
import re
import pandas as pd
import warnings
warnings.simplefilter(action='ignore')



## all static menu options
welcomemsg = 'Welcome!'
headermsg = 'Type quit to exit. Press enter after command to continue'
menuheader = 'Choose your option'

searchmenuoptions=[ 'Press 1 to set field to search on', 'Press 2 to clear search file','Press 3 to run search on all files','Press 4 to check which file is set as searchfile','Type \'terms\' to lookup searchable terms', 'Type help to view help', 'Type quit to exit','Type save to save results to file', 'Type results to show previous results']
defaultmenuoptions = ['Press 1 to set search file', 'Press 3 to run search on all files', 'Type help to view help', 'Press quit to exit','Type save to save results to file', 'Type results to show previous results']
helpcode = 'HELP000'

relatedsearchdict= {}
relatedsearchdict['users']= ["_id","external_id","organization_id" ]
relatedsearchdict['organizations']=["_id", "external_id", ]
relatedsearchdict['tickets']= ["_id","external_id","submitter_id","assignee_id","organization_id"]


## method to add matched on attribute to results

def returnmatchedon(row, columns, val):
    # (json.loads(row.to_json(orient = 'records')))
    l = list(row)
    index = list(row).index(val)
    return (columns[index])
    
        
## run search on all files
def runfullsearch(state:ProgramState):
    results = []
    vals = processinput(state,'enter values to search. if more than one value, separate by \',\'\n').split(',')
    if(vals[0] == helpcode):
        return helpcode
    for name, dfobj in state.dfobjlist.items():
        df = dfobj.df
        for val in vals:

            if(val.isnumeric()):
                val = int(val)
            result = df[df.eq(val).any(axis = 1)]
            if(result.size >0):
                result['filename'] = name

                result['matchedon'] = result.apply(lambda x: returnmatchedon(x, list(df.columns), val), axis = 1)
                result['matched_on_val'] = val


                results+= json.loads(result.to_json(orient = 'records') )
    if(not(results)):
        print('no results found')
            
    return results






## print help message

def runhelp():
    print('this is a helpful message')
    input('press enter to continue\n')
    return helpcode

## check input for key menu options
def processinput(state:ProgramState, msg=''):
    
    inp = input(msg)
    if(len(inp)>50):
        raise ValueError
    if(inp.lower() == 'help'):
        runhelp()
        return helpcode
    elif(inp.lower() =='quit'):
        sys.exit('exitting application')
    elif(inp.lower()=='results'):

        processresults(state)
        return helpcode
    elif(inp.lower()=='save'):
        saveresults(getresults(state))
        return helpcode
    else: 
        return inp

## save results to file
def saveresults(results):
    try:
        f= open("results.txt", "w") 
        if(not results):
            print('no results found')
            return helpcode
        else: 
            f.write('Total results found = {}\n\n'.format(countresults(results)))
            f.write('\n')
            f.close()
            for result in results:
                writedetails("results.txt", result)
                if('subresults' in result.keys()):
                    if(len(result['subresults'])>0):
                        f= open("results.txt", "a") 
                        [f.write('*') for i in range(80)]
                        f.write('\n objects related to current result\n')
                        [f.write('*') for i in range(80)]
                        f.write('\n')
                        f.close()
                        for result in result['subresults']:
                            writedetails('results.txt', result)
            print('saved\n')
    except Exception as e:
        print('unknown error')
        return
    # finally:
        print('saved\n')
        # print(e)



## set file to search from 


def setfilechoice(state):

    

    while(True):
        try:
            print('Enter', end = ' ')
            [print('{}) for {}; '.format(i+1,name), end = ' ') for i,(name, value) in enumerate(state.dfobjlist.items())]
            op = processinput(state)
            if(op==helpcode):
                continue
            op=int(op)
            if(op>len(state.dfobjlist)):
                raise ValueError
            else:
                print('searchfile set = {}'.format(list(state.dfobjlist.keys())[op-1]))
                return list(state.dfobjlist.keys())[op-1]
        except Exception as e:
            print('error try again')

## run default menu

def rundefault(state:ProgramState):
    try:
        results = None
        [print(x) for x in defaultmenuoptions]
        option1 = processinput(state)
        if(option1==helpcode):
            return helpcode
    
        if(option1.isnumeric()):
            if(int(option1)==1):
                #set file choice
                #pass
                state.filechoice = setfilechoice(state)
                return
            elif(int(option1)==3):
                results =runfullsearch(state)
                #search all files
                pass
                # runfullsearch(state)
            else:
                raise ValueError
        else:
            raise ValueError
    except Exception as e:
        print(e)
        print('sorry unknown command\n')
    finally:
        if(results):
            state.results = results
            processresults(state)






## clear the search file

def clearsearchfile(filechoice):
    if(not filechoice):
        # return None
        print('no file set\n')
    else:
        print('file choice cleared\n')
    return None


## search dataframe given key and value

def simplesearch(df, key , value, filename) ->list:
    try:
        if(not isinstance(value, str)):
            processedval = value
        else: 
            processedval = int(value) if value.isnumeric() else value

        result = df[df[key] == processedval]
        result['file'] = filename
        result['matchedon'] = key
        result['matched_on_val'] = processedval

        return json.loads(result.to_json(orient = 'records'))
    except Exception as e:
        return []

## start search on field

def startfieldsearch(state:ProgramState,file, fields= None, vals = None):


    results = []
    if(not fields):
        field = processinput(state, 'Enter field to search on\n')
        
        if(field== helpcode):
            return helpcode
        fields =  [column for column in list(file.df.columns) if(re.search('^{term}.*|.*{term}$'.format(term = field), column))]
        if(len(fields)<=0):
            print('sorry field not found')
            return results




    if(not vals):
        val = processinput(state, 'Enter value to search\n')
        if(vals == helpcode):
            return helpcode
        vals = [val]
    for field in fields:
        for val in vals:
            results+=simplesearch(file.df, field, val, file.name)
    return results



## get results from state object
def getresults(state):
    if(state.results):
        return state.results
    print('no results found')
    return helpcode


## search using the file set

def performsearch(state):
    primeresults = startfieldsearch(state, state.dfobjlist[state.filechoice])
    if(primeresults == helpcode):
        return helpcode
    for result in primeresults:
        result['subresults']=[]
        for file, obj in state.dfobjlist.items():
            if(not file == state.filechoice):
           
                
                fields = list(set(list(obj.df.columns)) &set(relatedsearchdict[file]))
                vals = [values for key, values in result.items()]
                
                result['subresults'] += startfieldsearch(state,obj,fields, vals)
    if(not primeresults):
        print('sorry no results found')
    return primeresults


## show searchable terms

def showterms(state:ProgramState, terms):
    [print(term) for term in terms]
    processinput('press enter to go back')
    return helpcode


## run search on set file
def runsearchonfile(state:ProgramState):
    try:
        results =None
        print('\n')
        [print(x) for x in searchmenuoptions]
        option1 = processinput(state)
        if(option1==helpcode):
            return helpcode
        if(option1.isnumeric()):
            if(int(option1)==2):
                state.filechoice = clearsearchfile(state.filechoice)
            elif(int(option1)==1):
                #begin search
                results= performsearch(state)
                pass
            elif(int(option1)==3):
                results =runfullsearch(state)
            elif(int(option1==4)):
                checkfilechoice(state)
            else:
                raise ValueError
        if(option1.isalpha()):
            if(option1=='terms'):
                return showterms(state, list(state.dfobjlist[state.filechoice].df.columns.values))
                # return helpcode
            elif(option1==helpcode):
                return helpcode
            else:
                raise ValueError
    except Exception as e:
        print('sorry unknown error')
        return
    finally:
        if(results):
            
            state.results = results
            processresults(state)
            return



## process results


def processresults(state):
    if(not state.results):
        print('no results found\n')
        return
    else: 
        print('Total results found = {}'.format(countresults(state.results)))
        for result in state.results:
            printdetails(result)
            if('subresults' in result.keys()):
                if(len(result['subresults'])>0):
                    [print('*', end = '') for i in range(80)]
                    print('\n objects related to current result')
                    [print('*', end = '') for i in range(80)]
                    print('\n')
                    for result in result['subresults']:
                        printdetails(result)

##print details on console

def printdetails(obj):
    for x, y in obj.items() :
        if(not x=='subresults'):
            print('{0:10}\t\t {1}'.format(str(x).strip(),str(y).strip()))
    [print('=', end = '') for i in range(80)]
    print('\n')
            


## write details to file
def writedetails(filename, obj):
    with open(filename, 'a') as f:
        for x, y in obj.items() :
            if(not x=='subresults'):
                f.write('{}\t{}\n'.format( x,y))
        [f.write('=') for i in range(80)]
        f.write('\n')


## check file set

def checkfilechoice(state:ProgramState):
    if(state.filechoice):
        print('\nsearchfile set = {}'.format(state.filechoice))
        
    else:
        print('no file set to search on')
    return
## load all files from path
    
def loadfiles(path='.//'):
    dataobjs = {}
    allfiles = []
    try:
        allfiles += os.listdir(path)
    except:
        print('error unable to find path showing current working directory\n')
        allfiles += os.listdir()
    finally:
        jsonfilelist = [file for file in allfiles if file.endswith('.json')]
        if(len(jsonfilelist) == 0):
            print('error no files found')
            sys.exit('exitting application')
        for file in jsonfilelist:
            # dataframes[re.sub('\.json$','', file)] = pd.read_json(file)
            dfobj = dataobject(re.sub('\.json$','', file), pd.read_json(file), jsonfilelist.index(file))
            dataobjs[dfobj.name] = dfobj
        
        return dataobjs

## count all results

def countresults(results):
    count = 0
    for result in results:
        if('subresults' in result.keys()):
            count+= len(result['subresults'])
    count+= len(results)
    return count