"""
Lab 4: The Memory Linker -- starter.

Complete DoublyLinkedList below. See the assignment,
Part B, for the full requirements. No node may ever become
unreachable from `head` after any sequence of operations.
"""

from typing import Generic, Iterator, Optional, TypeVar

T = TypeVar("T")


class _Node(Generic[T]):
    __slots__ = ("value", "prev", "next")

    def __init__(self, value: T) -> None:
        self.value = value
        self.prev: Optional["_Node[T]"] = None
        self.next: Optional["_Node[T]"] = None


class DoublyLinkedList(Generic[T]):
    def __init__(self) -> None:
        self.head: Optional[_Node[T]] = None
        self.tail: Optional[_Node[T]] = None
        self._size = 0

    def __len__(self) -> int:
        return self._size

    def insert_front(self, value: T) -> None:
        new_node = _Node(value)

        if self.head is None:
            # List is empty, new node becomes both head and tail
            self.head = new_node
            self.tail = new_node
        else:
            # List is not empty, insert new node at the front
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node

        self._size += 1

    def insert_back(self, value: T) -> None:
        new_node = _Node(value)

        if self.tail is None:
            # List is empty, new node becomes both head and tail
            self.head = new_node
            self.tail = new_node
        else:
            # List is not empty, insert new node at the back
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node

        self._size += 1

    def delete(self, value: T) -> bool:
        """Remove the first node matching `value`. Return True if removed, False if not found."""
        current = self.head
        while current is not None:
            if current.value == value:
                if current.prev is None:
                    self.head = current.next
                else:
                    # Deleting the head node
                    current.prev.next = current.next

                if current.next is None:
                    self.tail = current.prev
                else:
                    # Deleting the tail node
                    current.next.prev = current.prev

                self._size -= 1
                return True

            current = current.next

        return False

    def reverse(self) -> None:
        """Reverse the list in place."""
        current = self.head

        while current is not None:
            current.prev, current.next = current.next, current.prev
            current = current.prev

        self.head, self.tail = self.tail, self.head

    def insert(self, index: int, value: T) -> None:
        """
        Insert `value` so it becomes the element at `index` (0 through
        len(self), inclusive). Traverse from whichever end is closer to
        `index` to minimize steps.
        """
        if index < 0 or index > self._size:
            raise IndexError("index out of range")

        if index == 0:
            self.insert_front(value)
            return

        if index == self._size:
            self.insert_back(value)
            return

        new_node = _Node(value)

        if index <= self._size // 2:
            current = self.head

            for _ in range(index):
                current = current.next

            new_node.prev = current.prev
            new_node.next = current
            current.prev.next = new_node
            current.prev = new_node

        else:
            current = self.tail

            for _ in range(self._size - index):
                current = current.prev

            new_node.next = current.next
            new_node.prev = current
            current.next.prev = new_node
            current.next = new_node

        self._size += 1


    def delete_at(self, index: int) -> T:
        """Remove and return the value at `index`. Raise IndexError if out of range."""
        if index < 0 or index >= self._size:
            raise IndexError("index out of range")

        if index <= self._size // 2:
            current = self.head

            for _ in range(index):
                current = current.next

        else:
            current = self.tail

            for _ in range(self._size - index - 1):
                current = current.prev
        if current.prev is None:
            self.head = current.next
        else:
            current.prev.next = current.next

        if current.next is None:
            self.tail = current.prev
        else:
            current.next.prev = current.prev

        self._size -= 1
        value = current.value
        return value

    def __iter__(self) -> Iterator[T]:
        current = self.head

        while current is not None:
            yield current.value
            current = current.next
