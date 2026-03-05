import heapq

class Scheduler:
    def __init__(self):
        self.queue = []
        self.counter = 0  # To ensure unique ordering when priorities are equal

    def add_task(self, task, priority):
        """Add task with priority. Counter ensures stable ordering."""
        heapq.heappush(self.queue, (priority, self.counter, task))
        self.counter += 1

    def next_task(self):
        """Get the highest priority task (lowest priority number)"""
        if not self.queue:
            return None
        return heapq.heappop(self.queue)[2]

