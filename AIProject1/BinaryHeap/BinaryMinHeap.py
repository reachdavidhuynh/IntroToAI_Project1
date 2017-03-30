from BinaryHeap import BinaryHeap

class BinaryMinHeap(BinaryHeap):

  def __init__(self):
    super(BinaryMinHeap, self).__init__()

  def sift_up(self):
    new_element_index = self.binary_heap_size
    while new_element_index > 0:
      parent_index = self.parent(new_element_index)
      if self.binary_heap[parent_index] > self.binary_heap[new_element_index]:
        self.swap_elements(new_element_index, parent_index)
        new_element_index = parent_index
      else:
        break

  def sift_down(self):
    sifting_element_index = 0

    if self.binary_heap_size == 2:
      left_child_index = self.left_child(sifting_element_index)

      sifting_element = self.binary_heap[sifting_element_index]
      left_child = self.binary_heap[left_child_index]

      if left_child < sifting_element:
        self.swap_elements(sifting_element_index, left_child_index)
    else:
      while sifting_element_index < self.binary_heap_size-1 and self.binary_heap_size > 1:

        sifting_element = self.binary_heap[sifting_element_index]

        left_child_index = self.left_child(sifting_element_index)
        if left_child_index > self.binary_heap_size - 1:
          break
        left_child = self.binary_heap[left_child_index]

        right_child_index = self.right_child(sifting_element_index)
        right_child = self.binary_heap[right_child_index]

        if (sifting_element > left_child) or (sifting_element > right_child):
          sift_left = False
          sift_right = False
          if left_child < right_child:
            sift_left = True
          elif right_child < left_child:
            sift_right = True
          else:
            sift_left = True

          if sift_left:
            self.swap_elements(sifting_element_index, left_child_index)
            sifting_element_index = left_child_index
          elif sift_right:
            self.swap_elements(sifting_element_index, right_child_index)
            sifting_element_index = right_child_index
        else:
          break
