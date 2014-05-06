__author__ = 'tagloul'
# import threading
#
# class Thread(object, threading.Thread):
#     def __init__(self, t):
#         threading.Thread.__init__(self, target=t)
#         self.start()
import threading
import time
import inspect

class Thread(threading.Thread):
    lock = threading.Lock()
    def __init__(self, t, *args):
        threading.Thread.__init__(self, target=t, args=args)
        self.start()

lock = threading.Lock()
count = [1, 2, 3, 4, 5]

def incre():
    print 'appender'
    caller = inspect.getouterframes(inspect.currentframe())[1][3]
    #print "Inside %s()" % caller
    #print "Acquiring lock"
    #with lock:
    #print "Lock Acquired by %s()" % caller

    while len(count) < 10:
        lock.acquire()
        print 'lock acquired by appender'
        count.append(1)
        #time.sleep(0.5)
        lock.release()

def loop():
    for i in range(10):
        #lock.acquire()
        print 'lock acquired by loop'
        for a in count:
            #lock.acquire()
            print a
            #lock.release()
            #time.sleep(0.0003)
            # try:
            #     count.remove(1)
            # except:
            #     pass
        print 'ended'
        #lock.release()
def appender():
    # while count < 5:
    incre()

def iteratr():
    # while count < 5:
    pass

def main():
    # goodbye = Thread(loop)
    # time.sleep(3)
    hello = Thread(incre)
    time.sleep(1)
    goodbye = Thread(loop)
    threads = [goodbye, hello]
    # for x in threads:
    #     x.join()

if __name__ == '__main__':
    main()