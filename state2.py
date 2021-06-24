class ProgramState:
    def __init__(self, dfdict:dict) :
        self.dfobjlist = dfdict
        self.filechoice = None
        self.results = None


class dataobject:
    def __init__(self, name, df, id) -> None:
        self.name = name
        self.df = df
        self.id = id

class Result:

    def __init__(self, val, item, filename, matchedon) -> None:
        self.val = val
        self.item = item
        self.filename = filename
        self.matchedon = matchedon
        self.subresults =[]
        pass

    pass