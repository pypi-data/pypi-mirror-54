__version__ = "1.0.3"



from .disabled import ConlogDummy, ConsoleDummy


class Conlog:

    _ConlogImpl = None
    _state_ = dict()

    @classmethod 
    def get_console(cls, name):
        if name in cls._state_: 
            console =  cls._state_[name].console
            return console
        return ConsoleDummy()

    @classmethod
    def create(cls, name):
        _ConlogImpl = cls._ConlogImpl
        if _ConlogImpl is None:
            from conlog.impl import ConlogImpl
            _ConlogImpl  = ConlogImpl
            
            inst =  _ConlogImpl(name)

            cls._state_[name] = inst
            return inst

    @classmethod
    def disabled(cls):
        inst = ConlogDummy()
        return inst

