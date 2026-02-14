import time
import threading
import random
import sys
from queue import Queue

class Ticket:
    def __init__(self, ticketNumber, timeStamp):
        self.ticketNumber = ticketNumber
        self.timeStamp = timeStamp
is_running = True

def runQueue():
    line = Queue(maxsize=5)
    number = [1]

    def fillQueue():
        global is_running
        if not is_running:
            return
        if not line.full():
            ticket = Ticket(number, time.time())
            number[0] += 1
            print (f"Your ticket number is {ticket.ticketNumber} at {ticket.timeStamp}.")
            line.put(ticket)
        threading.Timer(random.randint(1,5),fillQueue).start()
    
    def emptyQueue():
        global is_running
        if not is_running:
            return
        if not line.empty():
            ticket = line.get()
            print (f"Ticket number {ticket.ticketNumber} is ready at {ticket.timeStamp}.")
        threading.Timer(random.randint(1,5),emptyQueue).start()
    
    fillQueue()
    emptyQueue()

if __name__ == "__main__":
    try:
        runQueue()
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        is_running = False
        sys.exit()