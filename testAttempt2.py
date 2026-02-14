import time
from queue import Queue
from attempt1 import Ticket
import unittest
from unittest.mock import patch

class testTicketing(unittest.TestCase):

    def setUp(self):
        self.testLine = Queue(maxsize=10)
        self.number = [1]
    
    def testTicketIncrement(self):
        t1 = Ticket(self.number[0],time.time())
        self.number[0] += 1
        t2 = Ticket(self.number[0],time.time())
        self.assertEqual(t1.ticketNumber,1)
        self.assertEqual(t2.ticketNumber,2)
    
    def testTicketTime(self):
        now = time.time()
        ticket = Ticket(1,now)
        self.assertIsInstance(now,float)
        self.assertEqual(ticket.timeStamp,now)
    
    def testFIFO(self):
        t1 = Ticket(1,time.time())
        t2 = Ticket(2,time.time())
        self.testLine.put(t1)
        self.testLine.put(t2)
        self.assertEqual(self.testLine.get(),t1)
        self.assertEqual(self.testLine.get(),t2)
    
    @patch('threading.Timer')
    def testShutdown (self,mockTimer):
        import attempt1
        attempt1.is_running = False

        def mockFill ():
            if not attempt1.is_running:
                return
            mockTimer(1,mockFill).start()
        mockFill()
        mockTimer.assert_not_called()
        

if __name__ == "__main__":
    unittest.main()