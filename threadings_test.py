__author__ = 'tagloul'

# import time
# from threading import Thread
#
#
# def sleeper(i):
#     print 'thread %d sleeps for 5 seconds' % i
#     time.sleep(5)
#     print "thread %d woke up" % i
#
# for i in range(10):
#     t = Thread(target=sleeper, args=(i,))
#     t.start()

import threading

class PrimeNumber(threading.Thread):
    prime_numbers = {}
    lock = threading.Lock()

    def __init__(self, number):
        threading.Thread.__init__(self)
        self.Number = number
        PrimeNumber.lock.acquire()
        PrimeNumber.prime_numbers[number] = "None"
        PrimeNumber.lock.release()

    def run(self):
        counter = 2
        res = True
        while counter*counter <= self.Number:
            if self.Number % counter == 0:
                res = False
                print "%d ist keine Primzahl, da %d = %d * %d \n" % ( self.Number, self.Number, counter, self.Number / counter)
                return
            counter += 1
        PrimeNumber.lock.acquire()
        PrimeNumber.prime_numbers[self.Number] = res
        PrimeNumber.lock.release()
        print "%d ist eine Primzahl\n" % self.Number


threads = []
while True:
    input = long(raw_input("number: "))
    if input < 1:
        break

    thread = PrimeNumber(input)
    threads += [thread]
    thread.start()

for x in threads:
    x.join()