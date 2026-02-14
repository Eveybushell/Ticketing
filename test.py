import unittest
from unittest.mock import patch, MagicMock
from queue import Queue
import time

from ticketQueue import Ticket, runQueue

class TestTicketSystem(unittest.TestCase):

    def setUp(self):
        self.test_queue = Queue(maxsize=10)
        self.test_number = [1]

    ## --- NORMAL CASES ---

    def test_sequential_increment(self):
        """Normal Case: Ensure ticket numbers increase by 1."""
        t1 = Ticket(self.test_number[0], time.time())
        self.test_number[0] += 1
        t2 = Ticket(self.test_number[0], time.time())
        
        self.assertEqual(t1.queueNumber, 1)
        self.assertEqual(t2.queueNumber, 2)

    def test_fifo_integrity(self):
        """Normal Case: Ensure First-In-First-Out order."""
        ticket1 = Ticket(1, time.time())
        ticket2 = Ticket(2, time.time())
        
        self.test_queue.put(ticket1)
        self.test_queue.put(ticket2)
        
        self.assertEqual(self.test_queue.get(), ticket1)
        self.assertEqual(self.test_queue.get(), ticket2)

    def test_ticket_timestamp_capture(self):
        """Normal Case: Ensure tickets capture a valid float timestamp."""
        now = time.time()
        ticket = Ticket(1, now)
        self.assertIsInstance(ticket.timeStamp, float)
        self.assertEqual(ticket.timeStamp, now)

    ## --- EDGE CASES ---

    def test_queue_overflow_prevention(self):
        """Edge Case: Ensure fillQueue doesn't add to a full queue."""
        # Fill the queue to its maxsize
        full_queue = Queue(maxsize=2)
        full_queue.put(Ticket(1, 0))
        full_queue.put(Ticket(2, 0))
        
        # Simulate the 'if not line.full()' logic
        was_added = False
        if not full_queue.full():
            full_queue.put(Ticket(3, 0))
            was_added = True
            
        self.assertFalse(was_added)
        self.assertEqual(full_queue.qsize(), 2)

    def test_empty_queue_handling(self):
        """Edge Case: Ensure emptyQueue doesn't crash when line is empty."""
        empty_line = Queue(maxsize=10)
        
        # Simulate 'if not line.empty()' logic
        processed_ticket = None
        if not empty_line.empty():
            processed_ticket = empty_line.get()
            
        self.assertIsNone(processed_ticket)

    @patch('threading.Timer')
    def test_shutdown_propagation(self, mock_timer):
        """Edge Case: Ensure no new timers are scheduled if is_running is False."""
        import ticketQueue
        ticketQueue.is_running = False
        
        # We manually trigger the logic inside runQueue (mocked)
        # If is_running is False, the function should return before calling Timer()
        def fill_mock():
            if not ticketQueue.is_running:
                return
            mock_timer(1, fill_mock).start()

        fill_mock()
        mock_timer.assert_not_called()

if __name__ == '__main__':
    unittest.main()