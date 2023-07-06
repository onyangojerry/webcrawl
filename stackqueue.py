
class Queue:
    """
    Provides a rudimentary implementation of the queue data structure

    Attributes
    ----------
    queue : (list of any) the underlying queue of objects

    Methods
    -------
    is_empty(): (bool) returns whether the queue is empty
    add(item): (None) adds the item at the back of the queue
    remove(): (any) removes and returns the item from the front of the queue

    """

    def __init__(self, initial_contents=[]):
        self.queue = initial_contents[:]

    def is_empty(self):
        """
        returns whether the queue is empty
        :return: (bool) whether the queue is empty
        """
        return self.queue == []

    def add(self, item):
        """
        adds the item at the back of the queue
        :param item: (any) the item to add at the back of the queue
        :return: (None)
        """
        self.queue.append(item)

    def remove(self):
        """
        removes and returns the item from the front of the queue
        :return: (any) the item from the front of the queue
        """
        return self.queue.pop(0)

    def __str__(self):
        return "The queue contains: " + str(self.queue)

class Stack:
    """
    Provides a rudimentary implementation of the stack data structure

    Attributes
    ----------
    stack : (list of any) the underlying stack of objects

    Methods
    -------
    is_empty(): (bool) returns whether the stack is empty
    add(item): (None) adds the item at the top of the stack
    remove(): (any) removes and returns the item from the top of the stack

    """

    def __init__(self, initial_contents=[]):
        self.stack = initial_contents[:]

    def is_empty(self):
        """
        returns whether the stack is empty
        :return: (bool) whether the stack is empty
        """
        return self.stack == []

    def add(self, item):
        """
        adds the item at the top of the stack
        :param item: (any) the item to add at the top of the stack
        :return: (None)
        """
        self.stack.append(item)

    def remove(self):
        """
        removes and returns the item from the top of the stack
        :return: (any) the item from the top of the stack
        """
        return self.stack.pop()

    def __str__(self):
        return "The stack contains: " + str(self.stack)