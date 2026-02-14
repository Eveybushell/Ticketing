import unittest
from unittest.mock import patch
import time
from attempt2 import Ticket
from queue import Queue

class ticketTests(unittest.TestCase):
    
    def setUp(self):
        self.line = Queue(maxsize=5)
        self.number = [1]
    
    def testTicketIncrement (self):
        t1 = Ticket(self.number[0], time.time())
        self.number[0] += 1
        t2 = Ticket(self.number[0], time.time())
        self.assertEqual(t1.ticketNumber, 1)
        self.assertEqual(t2.ticketNumber, 2)
    
    def testFIFO (self):
        t1 = Ticket(1, time.time())
        t2 = Ticket(2, time.time())
        self.line.put(t1)
        self.line.put(t2)
        self.assertEqual(self.line.get(),t1)
        self.assertEqual(self.line.get(),t2)
    
    def testTimeStamp (self):
        now = time.time()
        ticket = Ticket(0,now)
        self.assertIsInstance(ticket.timeStamp,float)
        self.assertEqual(ticket.timeStamp, now)
    
    def testOverfill (self):
        testLine = Queue(maxsize=2)
        testLine.put(Ticket(1,0))
        testLine.put(Ticket(2,0))
        hasAdded = False
        if not testLine.full():
            testLine.put(Ticket(3,0))
            hasAdded = True
        self.assertFalse(hasAdded)
        self.assertEqual(testLine.qsize(),2)
    
    def testTakeEmpty (self):
        testLine = Queue(maxsize=5)
        ticket = None
        if not testLine.empty():
            ticket = testLine.get()
        self.assertIsNone(ticket)

    @patch('threading.Timer')
    def testShutdown (self, mockTimer):
        import attempt2
        attempt2.is_running = False
        def fillMock():
            if not attempt2.is_running:
                return
            mockTimer(1,fillMock).start()
        fillMock()
        mockTimer.assert_not_called()
if __name__ == "__main__":
    unittest.main()
    

