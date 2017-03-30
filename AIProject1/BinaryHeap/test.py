from BinaryMinHeap import BinaryMinHeap

heap = BinaryMinHeap()
heap.push(1.1)
heap.push(1.2)
heap.push(.4)
heap.push(5)
heap.push(7)
heap.push(0)

print heap.pop()
print getattr(heap, 'binary_heap')
print heap.pop()
print getattr(heap, 'binary_heap')
print heap.pop()
print getattr(heap, 'binary_heap')
print heap.pop()
print getattr(heap, 'binary_heap')
print heap.pop()
print getattr(heap, 'binary_heap')
print heap.pop()
print getattr(heap, 'binary_heap')

#print heap.pop()
#print heap.pop()
#print heap.pop()
#print getattr(heap, 'binary_heap')
