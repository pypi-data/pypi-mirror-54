from conlog import Conlog 

     
def wait(self,  s):
    console = Conlog.get_console("main") 
    console.debug(r'{s=}')
    print("waiting")


def retry(self,  n):
    console = Conlog.get_console("main") 
    console.debug(r'{n=}')
    print("rettrun")

 
def sleep(self, secs, minutes):
    console = Conlog.get_console("main") 
    print("I am Sleeping")
    return secs+minutes
