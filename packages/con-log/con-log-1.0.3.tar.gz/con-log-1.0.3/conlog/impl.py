# Copyright (c) 2019, Cswl Coldwind <cswl1337@gmail.com
# This software is licensed under the MIT Liscense.
# https://github.com/cswl/tsu/blob/v3.x/LICENSE-MIT

import logging
import subprocess

import wrapt
import re
import functools

from colored import fore, back, style

from conlog.expr_debug import _expr_debug, _cdebug
from conlog.Console import Console
from conlog.formats import format_dict, format_caller

"""
 Conlog : A console logger for Python

 console = Conlog(__name, enabled=True)

 @conlog.fn
 def cli(console) :
    console.log("Hello world");

 Then you import collections of functions.
 Only collections labelled as
 @Conlog.module works.. it means they support the conlog protocol.

"""


class ConlogImpl:
    CRITICAL = logging.CRITICAL
    ERROR = logging.ERROR
    WARNING = logging.WARNING
    INFO = logging.INFO
    DEBUG = logging.DEBUG
    NONE = logging.NOTSET
    TRACE = -10

    def __init__(self, name) :

        self.name = name
        self._console = None
    
    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, level):
        self._level = level
        
        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(self._level)

        self.logger_shandler = logging.StreamHandler()
        formatter = logging.Formatter("%(message)s")
        self.logger_shandler.setFormatter(formatter)
        self.logger.addHandler(self.logger_shandler)

        self._console = Console(self.name, self.logger)
    
    @property
    def console(self):
        return self._console

    def passRoot(self,cls):
        def enabled(cls,*args,**kw):
            inst = super(type(cls),cls).__new__(cls)

            logger = self.logger.getLogger(cls.__name__)
            inst._conlog_ = ConlogImpl(self, cls.__name__, logger)

            return inst


        def disabled(cls,*args,**lw):
            inst = super(type(cls),cls).__new__(cls)

            inst._conlog_ = ConlogImpl(self)

            return inst

        cls.__new__ = enabled if self._enabled else disabled
        return cls



    def fngrp(self, cls, level, enabled):
        _cdebug(" impl::  {cls=}, {level=}, {enabled=}")
        instance = cls()
        if self._enabled:
            instance._conlog_ = ConlogImpl(cls.__name__, self.logger)
        else:
            instance._conlog_ = ConlogImpl()
        _cdebug("impl -> proxy", cls)
        return instance

    def dir(self, xdict):
        self.logger.debug(format_dict(xdict))

    def trace(self, unwrapped):
        """
        A decorator style fucntion that allows tracing of function call and return value.

        Usage:
            conlog.trace(grp_function)
            grp_function(hello)
        """
        instance = unwrapped.__self__
        _cdebug("static::trace::Call {instance=}   {unwrapped.__name__=}")

        def wrapper(*args, **kw):
            name = format_caller(unwrapped.__qualname__)
            print(f"{name} called  with {args} {kw}")
            result = unwrapped(*args, **kw)
            print(f"{name} exited returned {result}")

        wrapper.__unwrapped__ = unwrapped
        functools.update_wrapper(wrapper, unwrapped)
        setattr(instance, unwrapped.__name__, wrapper)
        return True

