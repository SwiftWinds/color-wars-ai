class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None


class PerfectSet:
    def __init__(self):
        self.head = None
        # List of pointers to nodes, index is the data value
        self.pointers = [None] * 25  # For integers 0-24

    def add(self, item):
        if not 0 <= item <= 24:
            raise ValueError("Item must be between 0 and 24")

        if self.pointers[item] is not None:  # Item already exists
            return

        # Create new node
        new_node = Node(item)

        # Insert at beginning of list
        if self.head:
            self.head.prev = new_node
        new_node.next = self.head
        self.head = new_node

        # Store pointer to node
        self.pointers[item] = new_node

    def remove(self, item):
        if not 0 <= item <= 24:
            raise ValueError("Item must be between 0 and 24")

        node = self.pointers[item]
        if node is None:  # Item doesn't exist
            return

        # Update adjacent nodes
        if node.prev:
            node.prev.next = node.next
        else:  # Node is head
            self.head = node.next

        if node.next:
            node.next.prev = node.prev

        # Clear pointer
        self.pointers[item] = None

    def __contains__(self, item):
        if not 0 <= item <= 24:
            return False
        return self.pointers[item] is not None

    def __iter__(self):
        current = self.head
        while current:
            yield current.data
            current = current.next
