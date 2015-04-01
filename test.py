import threading

def hello(string):
    print string

t = threading.Timer(3.0, hello, ["test"])
t.start() # after 30 seconds, "hello, world" will be printed