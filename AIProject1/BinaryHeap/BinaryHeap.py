class BinaryHeap(object):

  def __init__(self):
    self.binary_heap = []
    self.binary_heap_size = 0

  def push(self, new_element):
    self.binary_heap.append(new_element)
    self.sift_up()
    self.binary_heap_size += 1

  def pop(self):
    root = self.binary_heap[0]
    self.binary_heap[0] = self.binary_heap[self.binary_heap_size-1]
    del self.binary_heap[self.binary_heap_size - 1]
    self.binary_heap_size -= 1
    self.sift_down()
    return root

  def sift_up(self):
    pass

  def sift_down(self):
    pass

  def left_child(self, index):
    return 2 * index + 1

  def right_child(self, index):
    return 2 * index + 2

  def parent(self, index):
    return (index - 1) / 2

  def swap_elements(self, index_1, index_2):
    self.binary_heap[index_1], self.binary_heap[index_2] = self.binary_heap[index_2], self.binary_heap[index_1]
