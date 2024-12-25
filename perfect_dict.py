class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None
        self.prev = None


class PerfectDict:
    def __init__(self):
        self.head = None
        self.pointers = [None] * 25
        self._size = 0

    def __setitem__(self, key, value):
        if not 0 <= key <= 24:
            raise ValueError("Key must be between 0 and 24")

        if self.pointers[key] is not None:  # Update existing value
            self.pointers[key].value = value
            return

        # Create new node
        new_node = Node(key, value)

        # Insert at beginning of list
        if self.head:
            self.head.prev = new_node
        new_node.next = self.head
        self.head = new_node

        # Store pointer to node
        self.pointers[key] = new_node
        self._size += 1

    def __getitem__(self, key):
        if not 0 <= key <= 24:
            raise ValueError("Key must be between 0 and 24")

        node = self.pointers[key]
        if node is None:
            raise KeyError(key)
        return node.value

    def __delitem__(self, key):
        if not 0 <= key <= 24:
            raise ValueError("Key must be between 0 and 24")

        node = self.pointers[key]
        if node is None:
            raise KeyError(key)

        # Update adjacent nodes
        if node.prev:
            node.prev.next = node.next
        else:  # Node is head
            self.head = node.next

        if node.next:
            node.next.prev = node.prev

        # Clear pointer
        self.pointers[key] = None
        self._size -= 1

    def __bool__(self):
        return self.head is not None

    def __len__(self):
        return self._size

    def __contains__(self, key):
        if not 0 <= key <= 24:
            return False
        return self.pointers[key] is not None

    def __iter__(self):
        current = self.head
        while current:
            yield current.key
        current = current.next

    def items(self):
        current = self.head
        while current:
            yield current.key, current.value
            current = current.next

    def keys(self):
        return iter(self)

    def values(self):
        current = self.head
        while current:
            yield current.value
            current = current.next
