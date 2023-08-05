import logging
import inspect
from collections import UserString

class MUDFactory(object):
    pass

class MUDObject(object):

    _heartbeats = {}

    heartbeat = None

    def __init__(self):
        if self.heartbeat:
            MUDObject._heartbeats[self] = self.heartbeat

    def __str__(self):
        return "{}({})".format(self.__class__.__name__, ", ".join([str(k) + "=" + str(v) for k,v in self.__dict__.items()]))

    def __del__(self):

        self._deregister_heartbeat()
        logging.debug("Deleting {}".format(self))

    def _deregister_heartbeat(self):
        if self in MUDObject._heartbeats:
            del MUDObject._heartbeats[self]

class MUDAction(MUDObject):

    def __init__(self, function):
        self.function = function

    def __call__(self, *args, **kwargs):
        acts = self.function(*args, **kwargs)
        if not isinstance(acts, list) or not isinstance(acts, tuple):
            return [acts]
        return acts

class MUDActionException(Exception):
    pass

class StopAction(MUDActionException):
    pass

class MUDEvent(MUDObject):

    def __init__(self, function):
        self.function = function

    def __call__(self, *args, **kwargs):
        self.function(*args, **kwargs)

class MetaMUDInterface(type):

    _interfaces = {}

    def __new__(cls, name, bases, dct):
        inst = super().__new__(cls, name, bases, dct)
        if inst.name:
            cls._interfaces[inst.name] = inst
        return inst

class MUDInterface(object, metaclass=MetaMUDInterface):

    name = None
    game = None

    @classmethod
    def get_interface(cls, name, default=-1):
        interface = MetaMUDInterface._interfaces.get(name)
        if not interface and default==-1:
            raise Exception("Attempting to access interface {}, which doesn't exist".format(name))
        return interface or default

    def __del__(self):
        logging.debug("Deleting {}".format(self))

    def __getattribute__(self, k):

        import inspect

        v = object.__getattribute__(self, k)
        if k == "game" and not v:
            v = self.__class__.game
            if not v:
                raise Exception("Game not instantiated yet")
        elif not k.startswith("__") and inspect.isclass(v):
            v = v()
        elif v is None:
            # If we haven't gotten a value, lets see if there's an iface we can use
            v = MUDInterface.get_interface(k, default=None) or v

        setattr(self, k, v)

        return v

    def __init__(self):
        self.game = None
        for k,v in MetaMUDInterface._interfaces.items():
            setattr(self, k, v)

class MUDDecorator(object):

    def __init__(self, *args, **kwargs):
        if args and inspect.isclass(args[0]):
            self.cls = args[0]
            self.args = []
            self.kwargs = kwargs
            self.decorate()
        else:
            self.args = args
            self.kwargs = kwargs

    def __call__(self, cls):
        self.cls = cls
        self.decorate()

    def decorate(dself):
        pass

class MUDMessage(UserString):

    def __init__(self, data, context=None):
        self.data = data
        self.context = context or {}
