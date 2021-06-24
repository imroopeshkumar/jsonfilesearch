
from state2 import ProgramState 
import handler2



state = ProgramState(handler2.loadfiles())
        

print(handler2.welcomemsg)

print(handler2.headermsg)
print('\n\n\n'+handler2.menuheader)

while(True):
    try:
        if(state.filechoice):
            handler2.runsearchonfile(state)
        else:
            handler2.rundefault(state)
    except Exception as e:
        print('unknown error')
        continue


