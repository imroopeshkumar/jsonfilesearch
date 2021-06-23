from io import FileIO
import os
import re
import json
from state import State,Result
import sys
# from result import Result 
filepath = r'C:\Users\gohan\Work\MEL-ML_Engr-Challenge-20210525T063151Z-001\MEL-ML_Engr-Challenge\\'
# filetypes = ['json']


welcomemsg = 'Welcome!'
headermsg = 'Type quit to exit. Press enter after command to continue'
menuheader = 'Choose your option'
menuoptions1=[ 'Press 1 to begin term search', 'Press 2 to clear search file','Press 3 to run search on all files','Press 4 to check which file is set as searchfile','Type \'terms\' to lookup searchable terms', 'Type help to view help', 'Type quit to exit']
menuoptions2 = ['Press 1 to set search file', 'Press 3 to run search on all files', 'Type help to view help', 'Press quit to exit']
# toggleoptions = ['Press 3 to ']
optionselectmsg = 'Enter your option\n'
helpcode = 'HELP000';

relatedsearchdict= {}
relatedsearchdict['users']= ["_id","external_id","organization_id" ]
relatedsearchdict['organizations']=["_id", "external_id", ]
relatedsearchdict['tickets']= ["_id","external_id","submitter_id","assignee_id","organization_id"]


def readfile(path, filename):
    filepath = path+filename+'.json'
    return (json.loads(open(filepath, 'r').read()))
    pass


def search(searchfile,vals, terms,  refobj=None):
    resultlist = []

    
    for item in searchfile.content:
        for term in terms:
            for val in vals:
                try:
                    if(item[term]):

                        # if(term =='_id' and val ==68 and searchfile['name']=='users' and item['_id']==68):
                        #     print('found')
                            # print('found')
                        if(str(item[term]) == str(val)):
                            if(refobj):

                                temp = val
                                val = term

                                term = [key for key, value in refobj.items() if str(value) == str(temp)][0]
                                
                                
                            r = Result(val, item, searchfile.name, term )
                            resultlist.append(r)
                            
                            # if(item not in resultlist):
                            # resultlist.append(item)
                except Exception as e:
                    # print(e)
                    pass
    return resultlist
    # term = processinput('enter term to search by')
    # if(not term in  searchfile['searchableterms']):
    # searchterms = [searchterm for searchterm in searchfile['searchableterms'] if(re.search(term, searchterm))]
    # if(not any([re.search(term, searchterm) for searchterm in searchfile['searchableterms']])):
    # if(len(searchterms)<=0):
        # print('sorry term not matching any searchable term')
    # else:
    #     val = processinput('enter value for term')
    #     print('now searching')
        
    #     for item in searchfile['content']:
    #         for term in searchterms:
    #             if(str(item[term])==val):
    #                 if(not item in resultlist):
    #                     resultlist.append(item)

    #     return resultlist




    # for searchterm in searchfile['searchableterms']:
    #     if(re.search(term, searchterm)):
    #         print('now searching')
    # print('term not found')
    # if(not any(re.search(term, searchterm)) for searchterm in searchfile['searchableterms']):
    #     print('term not found please try again')
    # else: 
    #     print('now searching')

        
    pass



def relatedsearch(results, searchfile, fileslist):
    for file in fileslist:
        if(not file.name==searchfile):
            for result in results:
                result.subresults +=search(file,list(result.item.values()),relatedsearchdict[file.name],  result.item  )
        
    return results
            # passprin


def begintermsearch(fileslist, searchfile):
    results = {}
    mainfile = None
    term = processinput('enter term to search by')
    if(term==helpcode):
        return
    searchterms = None
    for file in fileslist: 
        if(file.name==searchfile):
            mainfile = file
            searchterms = [searchterm for searchterm in file.searchableterms if(re.search('^{term}.*|.*{term}$'.format(term = term), searchterm))]


    # searchterms = [searchterm for searchterm in fileslist[searchfile]['searchableterms'] if(re.search(term, searchterm))]

    if(len(searchterms)<=0):
        print('sorry term not found')
    else:

        val = processinput('enter value for term').split(',')
        if(val == helpcode):
            return

        results = search(mainfile,  val,searchterms,  None)
        # for file in fileslist:

        #     for result in results:
        #         for item in file['content']:

        allresults = relatedsearch(results, searchfile, fileslist)

        return allresults   

        # for term in searchterms:
        #     for item in mainfile['content']:
        #         if(item[term]==str(val)):


        #         pass


        # for file in fileslist:
        #     for term in searchterms:
        #         results[file['name']]=search(file['contents'], term, val)

        pass

def printdetails(obj):
    for x, y in obj.items():
            print('{0:10}\t\t {1}'.format(str(x).strip(),str(y).strip()))
    [print('=', end = '') for i in range(80)]
    print('\n')

def showresults(results):

    if(len(results)<=0):
        print('sorry no results found')

    # print('total results found = {}'.format( countresults(results)))
    for result in results: 
        print('matched on {} for value {} from file {}\n'.format(result.matchedon, result.val,  result.filename))
        # for x in (result.item):
        printdetails(result.item)
        if(len(result.subresults)>0):
            [print('-', end = '') for i in range(80)]
            print('\n')
            print('related objects to current obj')
            showresults(result.subresults)
    pass


def runsearchmenu(state:State):
    print('\n')
    [print(x) for x in menuoptions1]
    option1 = processinput()
    if(option1==helpcode):
        return
    try:
        if(option1.isnumeric()):
            if(int(option1)==2):

                state.searchfile=clearsearchfile(state.searchfile)
            elif(int(option1)==1):
                # terms = processinput('enter term to search by')
                # searchterms = [searchterm for searchterm in searchfile['searchableterms'] if(re.search(term, searchterm))]
                results = begintermsearch(state.searchfiles, state.searchfile)
                print('total results found = {}'.format( countresults(results)))
                showresults(results)
            elif(int(option1)==3):
                runfullsearch(state)
            elif(int(option1 )==4):
                print('\nsearchfile set = {}'.format(state.searchfile))
    
            else:
                raise ValueError
        if(option1.isalpha()):
            if(option1=='terms'):
                terms = None
                for file in state.searchfiles:
                    if(file.name== state.searchfile):
                        terms = file.searchableterms
                showsearchterms(terms)
            else:
                raise ValueError
    except Exception as e:
        print('sorry try again')



            # pass
def runfullsearch(state):
    results = []
    vals = processinput('enter values to search. if more than one value, separate by \',\'\n').split(',')
    if(vals == helpcode):
        return

    for file in state.searchfiles:
        results+=search(file,vals, file.searchableterms )

    print('total results found = {}'.format(countresults(results)))
    showresults(results)

    #     for item in file.content:


    #     pass


def rundefaultmenu(state):
    [print(x) for x in menuoptions2]
    option1 = processinput()
    if(option1==helpcode):
        return
    try:
        if(option1.isnumeric()):
            if(int(option1)==1):
                state.searchfile = setsearchfile(state)
            elif(int(option1)==3):
                runfullsearch(state)
            else:
                raise ValueError
        else:
            raise ValueError
    except Exception as e:
        print('sorry unknown command\n')
    

    pass
    # if(option1=='terms'):

    #             handler.showsearchterms(state1.searchfile['searchableterms'])
    #         else:
    #             print('invalidinputtryagain')
    # pass




def setsearchfile(state: State):
    

    print('Enter', end = ' ')
    [print('{}) for {}; '.format(x+1,y.name), end = ' ') for x,y in enumerate(state.searchfiles)]
    # print('\n')


    while(True):
        try:
            
            op = processinput()
            if(op==helpcode):
                pass
            op=int(op)
            if(op>len(state.filelist)):
                raise ValueError
                # pass
            else:
                print('searchfile set = {}'.format(state.searchfiles[op-1].name))
                return state.searchfiles[op-1].name
    #             obj = {}
    #             obj['name']=filelist[op-1]
    #             obj['content']=readfile(path, filelist[op-1])
    #             obj['searchableterms'] = [k for (k,v) in obj['content'][0].items()]


    #             print('searchfile set = {}'.format(obj['name']))
    #             return obj
    #             pass
    # #         # print('or leave empty if unsure')
    # #         filechoice = processinput()
    # #         if(filechoice):
    # #             return list(filedict.keys())[int(filechoice)]
    # #         # else:
    # #         #     return None
        except Exception as e:
            print('error try again')


    pass


def processinput(msg=''):
    
    inp = input(msg)
    if(len(inp)>50):
        raise ValueError
    if(inp.lower() == 'help'):
        runhelp()
        return helpcode
    elif(inp.lower() =='quit'):
        sys.exit('exitting application')
    else: 
        return inp

def runhelp():
    print('this is a helpful message')
    input('press enter to continue\n')

def showsearchterms(terms=None):
        # [print(key) for key in filedict.keys()]
        print('\n These terms are searchable in the file currently set\n')
        if(terms):
            [print(term) for term in terms]
        else:
            print('no searchfile set. to view searchable terms, please set searchfile first')
            return None
        processinput('\npress enter to view options')


            # pass



def createfilelist(path = ''):
        allfiles = []
        try:
            allfiles += os.listdir(path)
        except:
            print('error unable to find path showing current working directory\n')
            allfiles += os.listdir()
        finally: 
            if(len(allfiles)==0):
                print('error no file found')
                return []
            jsonfilelist = [re.sub('\.json$', '',file) for file in allfiles if file.endswith('.json')]
            return jsonfilelist

        # input(('press enter to continue'))


# def handleoption1(option1, state1):
#     if(option1.isnumeric()):
#         if(int(option1)==1):
#             state1.searchfile = setsearchfile(state1.filelist)
#         # print(state1.searchfile[0])
#         elif(int(option1) ==2):
#             clearsearchfile(state1)

#         elif(int(option1) ==4):
#             pass
#         else:
#             print('invalidinputtryagain')
#     elif(option1.isalpha()):
#         if(option1=='help'):
#             runhelp()
#         if(option1=='terms'):
#             showsearchterms(state1.filedict)
#         else:
#             print('invalidinputtryagain')
           
#     else:
#         print('invalidinputtryagain')

def clearsearchfile(searchfile):
    if(not searchfile):
        # return None
        print('no file set\n')
    else:
        print('searchfile cleared\n')
    return None

def countresults(results):
    count = 0
    for result in results:
        count+= len(result.subresults)
    count+= len(results)
    return count