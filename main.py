import threading
import time
import socket
from queue import Queue
from datetime import datetime

# a print_lock is what is used to prevent modification of shared variables
# this is used so while one thread is using a variable, others cannot access it
# Once done, the thread releases the print_lock
# to use it, you want to specify a print_lock per thing you wish to print_lock


print("|| alrea port scanner ||")

print_lock = threading.Lock()

TARGET = input("Enter a remote host to scan: ")
NUMBER_OF_THREADS = int(input("Enter the amount of threads allocated for the scan: "))
NUMBER_OF_PORTS = int(input("Enter the amount of ports to scan: "))
# should be 65535

print("-" * 60)
print(f"Please wait, scanning remote host {socket.gethostbyname(TARGET)}")
print("-" * 60)


def port_scan(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((TARGET, port))
        with print_lock:
            print(f"Port {port}: Open")
        s.close()
    except WindowsError:
        pass


# The threader thread pulls a worker from the queue and processes it
def threader():
    while True:

        # run the example job with the available worker in queue
        port_scan(queue.get())

        # completed the task
        queue.task_done()


# create the queue and the threader
queue = Queue()

# define how many threads we are going to allow
for _ in range(NUMBER_OF_THREADS):
    thread = threading.Thread(target=threader)

    # classifying as a daemon, hence they will die when the main dies
    thread.daemon = True

    # begins, must come after daemon definition
    thread.start()

start_time = time.time()

# 1000 tasks assigned.
for worker in range(1, NUMBER_OF_PORTS + 1):
    queue.put(worker)

# wait until the thread terminates.
queue.join()

print(f"Process completed in {round(time.time() - start_time, 1)} seconds")
