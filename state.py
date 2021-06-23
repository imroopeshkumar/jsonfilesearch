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
        # self.filelist = self.createfilelist()

    # def createfilelist(path = os.getcwd()):
    #     allfiles = []
    #     try:
    #         allfiles += os.listdir(path)
    #     except:
    #         print('error unable to find path showing current working directory\n')
    #         allfiles += os.listdir()
    #     finally: 
    #         if(len(allfiles)==0):
    #             print('error no file found')
    #             return []
    #         jsonfilelist = [file for file in allfiles if file.endswith('.json')]
    #         return jsonfilelist



    # def addfiletodict(filelist:dict):
        
    #     filedict = {re.sub('\.json$', '',file): json.loads(open(file, 'r').read()) for file in filelist}
    #     return filedict

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
            # jsonfilelist = [file for file in allfiles if file.endswith('.json')]
            for file in jsonfilelist:
                # obj = {}
                # obj['name']=re.sub('\.json$','', file)
                # obj['content']=json.loads(open(file, 'r').read())
                # obj['searchableterms'] = obj['content'][0].keys()
                obj = fileobj(re.sub('\.json$','', file),json.loads(open(file, 'r').read()) ,list(json.loads(open(file, 'r').read())[0].keys()))
                searchfilelist.append(obj)
        #     filedict = {re.sub('\.json$', '',file): json.loads(open(file, 'r').read()) for file in jsonfilelist}
            return searchfilelist
        #     return filedict
        # pass


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