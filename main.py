from os import stat
import handler
from state import State 
print(handler.welcomemsg)
print(handler.headermsg)
print('\n\n\n'+handler.menuheader)

state1 = State(handler.filepath)


state1.filelist = handler.createfilelist(state1.path)



while(True):

    if(state1.searchfile):
        handler.runsearchmenu(state1)
    else:
        handler.rundefaultmenu(state1)

    