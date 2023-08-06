


class ConlogDummy:
    def __init__(self,*args, **kw):
        pass

    def get(self,name):
        pass
    
    @property
    def console(self):
        return ConsoleDummy()

class ConsoleDummy:
    def dir (self, *args, **kw):
        pass

    def debug(self, *args, **kw):
        pass

    def log(self, *args, **kw):
        pass

    def debug_func_set(self, func):
        pass
