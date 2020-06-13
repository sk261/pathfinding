
class pqueue:
    def __init__(self):
        self.queues = []

    def enqueue(self, item):
        if len(self.queues) == 0:
            self.queues.append([item])
        for n in range(len(self.queues)):
            if item.compare(self.queues[n][0]) == 0:
                self.queues[n].append(item)
                return
            if item.compare(self.queues[n][0]) < 0:
                self.queues.insert(n, [item])
                return
        if item.compare(self.queues[-1][0]) > 0:
            self.queues.append([item])

    def dequeue(self):
        if len(self.queues) == 0:
            return False
        ret = self.queues[0].pop(0)
        if len(self.queues[0]) == 0:
            self.queues.pop(0)
        return ret

class stack:
    def __init__(self):
        self.list = []
    
    def push(self, item):
        self.list.append(item)
    
    def pop(self):
        if len(self.list) > 0:
            return self.list.pop()
        else:
            return False

