import threading
import time
from threading import Thread

def foo(t):
    i = 0
    while i<10:
        print(threading.currentThread().getName(),i)
        i+=1
        time.sleep(t)
    return"{} end".format(threading.currentThread().getName())

class ThreadWithReturnValue(Thread):
    def __init__(self,group=None, target=None, name= None, args=(),kwargs={},Verbose=None):
        Thread.__init__(self, group,target,name,args,kwargs)
        self._return= None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

    def join(self,*args):
        Thread.join(self,*args)
        return self._return

class WorkQueue:
    def __init__(self):
        self.works = list()

    def push(self,cb,*args, **kwargs):
        self.works.append([cb,args,kwargs])

    def pop(self):
        if len(self.works):
            work, args,kwargs = self.works.pop(0)
            t = ThreadWithReturnValue(target= work, args=args,kwargs=kwargs)
            t.start()
            return t.join()

works = WorkQueue()
works.push(foo,0.1)
works.push(foo,1)
works.push(foo,3)
print("a",works.pop())
print("b",works.pop())
print("c",works.pop())