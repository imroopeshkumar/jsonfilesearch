from os import stat
import handler
from state import State 
print(handler.welcomemsg)
print(handler.headermsg)
print('\n\n\n'+handler.menuheader)


# state = State(handler.mainmenu(handler.optionselectmsg))



# filedict = handler.createfiledict()

state1 = State(handler.filepath)

state1.filelist = handler.createfilelist(state1.path)



while(True):

    # if(state1.searchfile):
    #     # handler.menuoptions.insert(3, 'Press 3 to remove search file')
    #     [print(x) for x in handler.menuoptions1]
    #     # pass
    # else:
    #     # handler.menuoptions.
    #     [print(x) for x in handler.menuoptions2]

    # option1 = handler.processinput()
    # print(type(option1))



    if(state1.searchfile):
        handler.runsearchmenu(state1)
    else:
        handler.rundefaultmenu(state1)

    # state1.searchfile = handler.handleoption1(option1)
    # if(option1):
    #     if(option1.isnumeric()):
    #         if(int(option1)==1):
    #             state1.searchfile = handler.setsearchfile(state1.filelist, state1.path)
    #         # print(state1.searchfile[0])
    #         elif(int(option1) ==2):
    #             state1.searchfile = handler.clearsearchfile(state1.searchfile)
    #         elif(int(option1) ==3):
    #             handler.showhelp(state1)
    #         elif(int(option1) ==4):
    #             pass
    #         else:
    #             print('invalidinputtryagain')
    #     elif(option1.isalpha()):
    #         # if(option1=='help'):
    #         #     handler.runhelp()
    #         if(option1=='terms'):

    #             handler.showsearchterms(state1.searchfile['searchableterms'])
    #         else:
    #             print('invalidinputtryagain')

    
        
    # else:
    #     print('invalidinputtryagain')
