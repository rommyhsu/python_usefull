def decorator_example1():
    '''
        like\n
        def f(x):\n
        \t"""does some math"""\n
        \treturn x + x * x\n

        f = logged(f)\n

        print f(3)
    '''
    def logged(func):
        def with_logging(*args, **kwargs):
            print (func.__name__ + " was called")
            return func(*args, **kwargs)
        return with_logging

    @logged
    def f(x):
        """does some math"""
        return x + x * x

    print (f(3))

def decorator_example1_2():
    
    def logged2(func):
        print (func.__name__ + " was called")
        return func

    @logged2
    def f(x):
        """does some math"""
        return x + x * x

    print(f(3))


def decorator_example2():
    '''
    decorator fold call function
    '''
    
    def makebold(fn):
        def wrapped():
            return "<b>" + fn() + "</b>"
        return wrapped

    def makeitalic(fn):
        def wrapped():
            return "<i>" + fn() + "</i>"
        return wrapped

    @makeitalic
    @makebold
    def hello():
        return "hello world"

    print (hello())



def entryExit_example():
    '''
    decorator fold call class object
    '''
    class entryExit(object):

        def __init__(self, f):
            print ('entry init enter')
            self.f = f
            print ('entry init exit')

        def __call__(self, *args):
            print ("Entering", self.f.__name__)
            r = self.f(*args)
            print ("Exited", self.f.__name__)
            return r

    print ('decorator using')

    @entryExit
    def hello(a):
        print ('inside hello')
        return ("hello world " + a)

    print ('test start')
    print( hello('friends'))





if __name__ == '__main__':
    decorator_example1()
    print("\n----------------------\n")
    decorator_example1_2()
    print("\n----------------------\n")
    decorator_example2()
    print("\n----------------------\n")
    entryExit_example()
