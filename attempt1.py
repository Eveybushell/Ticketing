from queue import Queue
import random
import time
import sys
import threading

class Ticket:

    def __init__(self, ticketNumber, timeStamp):
        self.ticketNumber = ticketNumber
        self.timeStamp = timeStamp
is_running = True

def runQueue():
    line = Queue(maxsize=5)
    queuenumber = [1]
    def fillQueue():
        global is_running
        if not is_running:
            return
        if not line.full():
            ticket = Ticket(queuenumber, time.time())
            queuenumber[0] += 1
            line.put(ticket)
            print(f"Your number is {ticket.ticketNumber} at {ticket.timeStamp}.")
        threading.Timer(random.randint(1,5),fillQueue).start()
    def emptyQueue():
        global is_running
        if not is_running:
            return
        if not line.empty():
            ticket = line.get()
            print (f"Calling ticket number {ticket.ticketNumber} at {ticket.timeStamp}.")
        threading.Timer(random.randint(1,5),fillQueue).start()

    fillQueue()
    emptyQueue()

if __name__ == "__init__":
    try:
        runQueue()
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        is_running = False
        sys.exit(0)

    