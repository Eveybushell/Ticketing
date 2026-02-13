from queue import Queue
import sys
import time
import threading
import random
class Ticket :

    def __init__(self, queueNumber, timeStamp):
        self.queueNumber = queueNumber
        self.timeStamp = timeStamp
is_running = True

def runQueue():
    line = Queue(maxsize=10)
    number = [1]

    def fillQueue():
        global is_running
        if not is_running:
            return # Stop the cycle!
        
        if not line.full():
            ticket = Ticket(number, time.time())
            number[0] += 1
            line.put(ticket)
            print(f"You have ticket number {ticket.queueNumber} at {ticket.timeStamp}.")
        threading.Timer(random.randint(1,5),fillQueue).start()
    
    def emptyQueue():
        global is_running
        if not is_running:
            return # Stop the cycle!
            
        if not line.empty():
            ticket = line.get()
            print(f"Calling ticket {ticket.queueNumber} at {ticket.timeStamp}.")
        threading.Timer(random.randint(1,5),emptyQueue).start()
    
    fillQueue()
    emptyQueue()

if __name__ == "__main__":
    try:
        runQueue()
        while True:
            time.sleep(0.1)  # Keep main thread alive so it can catch Ctrl+C
    except KeyboardInterrupt:
        is_running = False  # This prevents new timers from being scheduled
        sys.exit(0)


