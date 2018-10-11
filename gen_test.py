import threading
import time
import numpy as np

def do_sleep(i):
    time.sleep(i)

def initial_data_gen():
    for i in range(30):
        do_sleep(3)
        yield(i)


input = 5
result = None
access_input = threading.Lock()
access_output = threading.Lock()

def pp():
    print("-----------------------------")


def thread_do_sleep():
    global result, input, access_input,access_output
    #print("Starting the do sleep thread")
    #block the main thread
    #pp(), print("Do sleep thread waiting output") , pp()
    access_output.acquire()
    #pp(), print("Do sleep thread acquired output") , pp()
    #access the input data
    #pp(), print("Do sleep thread waiting input") , pp()
    access_input.acquire()
    #pp(), print("Do sleep thread acquired input") , pp()
    val = input
    access_input.release()
    #pp(), print("Do sleep thread released input") , pp()
    time.sleep(3)
    result = val + 1
    #release output value
    access_output.release()
    #pp(), print("Do sleep thread released output") , pp()

#Please note this function is not perfect and will break half the time - problem initialising threads - maybe semaphore or something is needed?
#also starting new thread on each round is slowwww - improve
def threaded_data_gen():
    global result, input, access_input,access_output
    #acquire the mutex, write data and release the mutex
    input = 0
    threading.Thread(target=thread_do_sleep).start()

    for i in range(1,30):
        #Note this bit is broken and hacky - should improve
        #while result == None:
            #time.sleep(0.1)

        #wait to acquire the output mutex and read result
        #pp(), print("Main thread waiting output") , pp()
        access_output.acquire()
        #pp(), print("Main thread acquired output") , pp()
        value = result
        #ensure blocking of do sleep thred (order is important here!!)
        #pp(), print("Main thread waiting input") , pp()
        access_input.acquire()
        #pp(), print("Main thread acquired input") , pp()
        access_output.release()
        threading.Thread(target=thread_do_sleep).start()
        #pp(), print("Main thread released output") , pp()
        input = value
        access_input.release()
        #pp(), print("Main thread released input") , pp()

        yield(value)


def test_functions():
    generator_v1 = initial_data_gen()
    generator_v2 = threaded_data_gen()

    g1_time = []
    g2_time = []

    for i in range(20):
        print("iter number " + str(i))
        time.sleep(2)

        start = time.time()
        print(generator_v1.__next__())
        end = time.time()
        g1_time.append(start-end)

        start = time.time()
        print(generator_v2.__next__())
        end = time.time()
        g2_time.append(start-end)
    print("The average time for non_threaded is " + str(np.mean(g1_time)) + " the average time for threaded is " + str(np.mean(g2_time)))

test_functions()
