
from conlog import Conlog

class EnvVar:
    def __init__(self, ):
        self.envcopy = {}
        

    def getVar(self, name):
        console = Conlog.get_console("main")
        console.debug("{name=} ")
        return name
    
    def setVar(self, name, val ) :
        cconsole = Conlog.get_console("main")
        self.envcopy["name"] = val
        console.debug("{self.envcopy=}{name=} ")
