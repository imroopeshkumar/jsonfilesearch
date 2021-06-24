import os
import re
import json
# import threading
class State: 

    

    def __init__(self,path='./', searchfile=None) -> None:
        self.path = path
        self.searchfileName = searchfile
        self.searchfiles = self.loadfiles(path)
        self.filelist = None
        self.searchableterms = None
        self.searchfile = None

    def loadfiles(self, path='./'):
        allfiles = []
        try:
            allfiles += os.listdir(path)
        except:
            print('error unable to find path showing current working directory\n')
            allfiles += os.listdir()
        finally: 
            jsonfilelist = [file for file in allfiles if file.endswith('.json')]
            searchfilelist = []
            if(len(allfiles)==0):
                print('error no file found')
                return []

            for file in jsonfilelist:

                obj = fileobj(re.sub('\.json$','', file),json.loads(open(file, 'r').read()) ,list(json.loads(open(file, 'r').read())[0].keys()))
                searchfilelist.append(obj)

            return searchfilelist



class fileobj:
    def __init__(self, name, content, searchableterms) -> None:
        self.name = name
        self.content = content
        self.searchableterms = searchableterms
    
    
class Result:

    def __init__(self, val, item, filename, matchedon) -> None:
        self.val = val
        self.item = item
        self.filename = filename
        self.matchedon = matchedon
        self.subresults =[]
        pass

    pass