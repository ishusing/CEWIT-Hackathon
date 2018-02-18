
from threading import Thread
from time import sleep
from getToken import sendReq
def threaded_function(arg,micro):
    total = 0;
    for i in range(10000000):
        interval = 1
        print( "running")
        sleep(interval)
        print(micro.test())
        total += interval
        if total > 10:
              print("Sending Request to pay")
              total = 0;
              try:
                   sendReq()
              except:
                   print("Exception Occured")

def startThread1(   micro):
    
    thread = Thread(target=threaded_function, args=(10,micro,))
    thread.start()
    #thread.join()
    print ("thread finished...exiting")

#startThread()
