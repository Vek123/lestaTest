import datetime
import time
from typing import List, Optional, Any
from abc import ABC, abstractmethod


class BaseQueueAbstract(ABC):
    rewritable: bool
    _buffer_size: int
    length: int

    @abstractmethod
    def __len__(self):
        ...

    @abstractmethod
    def append(self, val):
        ...

    @abstractmethod
    def change_buffer(self, buffer_size: int, save_last: bool = False):
        ...


class BaseQueue(BaseQueueAbstract):

    rewritable: bool
    _buffer_size: int
    length: int

    def __init__(self, rewritable: bool = True):
        self.length = 0
        self.rewritable = rewritable

    def __iter__(self):
        return self

    def __len__(self):
        return self.length

    def append(self, val):
        pass

    def change_buffer(self, buffer_size: int, save_last: bool = False):
        pass


class QueueList(BaseQueue):
    """
    Class implements cycle buffer FIFO using list to store it.
    """
    buffer: list
    _left_index: int = 0
    _right_index: int = 0

    def __init__(
            self,
            buffer: Optional[List[Any]] = None,
            buffer_size: Optional[int] = None,
            rewritable: bool = True
    ):
        super().__init__(rewritable)
        # At least one of them must be not None
        if buffer_size is None and buffer is None:
            raise Exception("buffer_size or buffer should be not None")
        if buffer_size is not None and buffer_size <= 0:
            raise Exception("buffer_size should be > 0")
        if buffer is not None and len(buffer) == 0:
            raise Exception("buffer length should be > 0")
        if buffer_size is not None:
            self.buffer = [None] * buffer_size
            self._buffer_size = buffer_size
            if buffer is not None:
                for sub in buffer:
                    self._add_to_end(sub)
        else:
            self.buffer = buffer
            self._buffer_size = len(buffer)
            self.length = self._buffer_size
            self._right_index = self._buffer_size - 1

    def __next__(self):
        if self.length == 0:
            raise StopIteration
        val = self.buffer[self._left_index]
        self.buffer[self._left_index] = None
        self.length = max(0, self.length - 1)
        self._left_index = (self._left_index + 1) % self._buffer_size
        return val

    def _add_to_end(self, val: Any):
        if self._left_index == self._right_index and self.length != 0:
            if not self.rewritable:
                raise Exception("Buffer is not rewritable")
            self._left_index = (self._left_index + 1) % self._buffer_size
        self.buffer[self._right_index] = val
        self.length = min(self._buffer_size, self.length + 1)
        self._right_index = (self._right_index + 1) % self._buffer_size

    def change_buffer(self, buffer_size: int, save_last: bool = False):
        new_buffer = []
        if save_last:
            count = 0
            self._right_index = (self._right_index - 1) % self._buffer_size
            prev_right = self._right_index
            while count < buffer_size:
                new_buffer.append(self.buffer[self._right_index])
                self._right_index = (self._right_index - 1) % self._buffer_size
                if self._right_index == prev_right:
                    break
                count += 1
            new_buffer.reverse()
        else:
            count = 0
            for val in self:
                if count == buffer_size:
                    break
                new_buffer.append(val)
                count += 1
        self.length = len(new_buffer)
        new_buffer += [None] * (buffer_size - len(new_buffer))
        self.buffer = new_buffer
        self._buffer_size = buffer_size
        self._left_index = 0
        self._right_index = self.length % self._buffer_size

    def append(self, *val: Any) -> None:
        """
        Append values to the end of existing queue
        :param val:
        :return:
        """
        for sub in val:
            if isinstance(sub, list):
                for i in sub:
                    self._add_to_end(i)
            else:
                self._add_to_end(sub)


class QueueItem(object):
    val: int
    next_item: "QueueItem"
    prev_item: "QueueItem"

    def __init__(
            self,
            val: Any,
            prev_item: Optional["QueueItem"] = None,
            next_item: Optional["QueueItem"] = None
    ):
        self.val = val
        self.next_item = next_item
        self.prev_item = prev_item

    def __str__(self):
        return f"Val: {self.val}"


class QueueLinked(BaseQueue):
    """
    Class implements cycle buffer FIFO using linked list to store it.
    """
    left: QueueItem | None
    right: QueueItem | None

    def __init__(
            self,
            buffer_size: int,
            rewritable: bool = True,
    ):
        super().__init__(rewritable)
        self._buffer_size = buffer_size
        self.left = None
        self.right = None

    def __next__(self):
        if self.length == 0:
            self.left = None
            self.right = None
            raise StopIteration
        val = self.left.val
        self.left = self.left.next_item
        if self.left is not None:
            self.left.prev_item = None
        self.length = max(0, self.length - 1)
        return val

    def _add_one(self, val: Any):
        if self.length >= self._buffer_size and not self.rewritable:
            raise Exception("Buffer is not rewritable")
        insert = QueueItem(val)
        if self.left is None:
            self.left = insert
            self.right = insert
        else:
            self.right.next_item = insert
            insert.prev_item = self.right
            self.right = insert
            if self.length >= self._buffer_size:
                self.left = self.left.next_item
                self.left.prev_item = None
        self.length = min(self.length + 1, self._buffer_size)

    def change_buffer(self, buffer_size: int, save_last: bool = False):
        self._buffer_size = buffer_size
        if save_last:
            while self.length > self._buffer_size:
                self.left = self.left.next_item
                self.left.prev_item = None
                self.length = max(0, self.length - 1)
        else:
            while self.length > self._buffer_size:
                self.right = self.right.prev_item
                self.right.next_item = None
                self.length = max(0, self.length - 1)

    def append(self, *val: Any):
        for sub in val:
            if isinstance(sub, list):
                for i in sub:
                    self._add_one(i)
            else:
                self._add_one(sub)


fifo1 = QueueList(buffer_size=4, rewritable=True)
fifo1.append(1, 2)
assert next(fifo1) == 1
fifo1.append([3, 4, 5])
fifo1.change_buffer(2, True)
assert fifo1.buffer == [4, 5]
fifo1.append(6, 7)
fifo1.append(8, 9)
result = []
for i in fifo1:
    result.append(i)
assert result == [8, 9]

# fifo2 = QueueLinked(buffer_size=5)
# fifo2.append(1, 2, 3, 4, 5, 6, 7, 8)
# res = []
# for i in range(2):
#     res.append(next(fifo2))
# assert res == [4, 5]
# fifo2.change_buffer(2, True)
# assert fifo2.left.val == 7
# res.clear()
# for i in fifo2:
#     res.append(i)
# assert res == [7, 8]
# fifo2.change_buffer(3)
# fifo2.append(9, 10, 11)
# res.clear()
# for i in fifo2:
#     res.append(i)
# assert res == [9, 10, 11]


class Stress:
    @staticmethod
    def start_stress(que: BaseQueue):
        for k in range(5, 1000, 5):
            que.change_buffer(k)
            for i in range(1000):
                que.append([i] * i)
            for _ in que:
                ...


# fifo1 = QueueList(buffer_size=10)
# start = time.time()
# Stress.start_stress(fifo1)
# print(f"Time: {time.time() - start}")
# fifo2 = QueueLinked(buffer_size=10)
# start = time.time()
# Stress.start_stress(fifo2)
# print(f"Time: {time.time() - start}")
