__version__ = "0.6.0"



from .disabled import ConlogDummy, ConsoleDummy

class Conlog:

    @classmethod 
    def get_console(self, name):
        return ConsoleDummy()
    
    @classmethod
    def disabled(cls):
        inst = ConlogDummy()
        return inst

