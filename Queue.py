class Queue:
    def __init__(self):
        self.queue = []

    def enqueue(self, item):
        self.queue.append(item)

    def dequeue(self):
        if not self.is_empty():
            return self.queue.pop(0)
        else:
            print("Queue is empty")
            return None

    def peek(self):
        if not self.is_empty():
            return self.queue[0]
        else:
            print("Queue is empty")
            return None

    def is_empty(self):
        return len(self.queue) == 0

    def size(self):
        return len(self.queue)
