import pykka

class Link_Actor(pykka.ThreadingActor):
    history = -1
    def link(self, *args):
        try:
            args[0]
        except IndexError:
            pass
        else:
            self.history = args[0]
        return self.history
            
class Log_And(pykka.ThreadingActor):
    def and_op(self, a, b):
        if (b == -1):
            return (not a)
        else:
            return (a and b)


class Log_Or(pykka.ThreadingActor):
    def or_op(self, a, b):
        return (a or b)
    
class Log_Not(pykka.ThreadingActor):
    def not_op(self, a):
        return (not a)
    
