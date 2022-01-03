import sys
import math

#To add a new element to the heap
def add_element(x):
    min_heap.append(x)
    size = len(min_heap)
    heapify_up(size) 
   
#To extract the root (minimum element) from the heap
def extract_min()   :
    min = min_heap[0]                                  #assigning the root (element at index - 0) as the minimum value
    min_heap[0] = min_heap[-1]                         #replacing the root with the last element
    min_heap.pop()                                     #removing the last element from the array

    size = len(min_heap)
    size = size - 1
    if size >= 1:
        heapify_down(1)                                #heapify_down is called to rearrange elements to maintain min-heap structure
    return min

#To re-order the elements after insertion (heapify-up)
def heapify_up(i):   
    parent = math.trunc((i / 2) - 1)                   #accounting for the fact that the array index starts with 0
    child = i - 1                                      #accounting for the fact that the array index starts with 0

    while child >= 1 and min_heap[child] < min_heap[parent]:
        #swapping the parent and child
        t = min_heap[parent]
        min_heap[parent] = min_heap[child]
        min_heap[child] = t
        child = parent

        if child % 2 == 0:
            parent = math.trunc(child / 2 - 1)         #accounting for the fact that the array index starts with 0
        else:
            parent = math.trunc(child / 2)

#To reorder elements after extraction (heapify-down) 
def heapify_down(i):
    while 2*i <= len(min_heap):
        if 2*i == len(min_heap) or min_heap[2*i - 1] <= min_heap[2*i]:
            j = (2 * i) - 1                            #accounting for the fact that the array index starts with 0
        else:
            j = (2 * i)
        i = i - 1                                      #accounting for the fact that the array index starts with 0

        if min_heap[j] < min_heap[i]:
            #swapping the child and parent
            t = min_heap[i]
            min_heap[i] = min_heap[j]
            min_heap[j] = t
            i = j + 1
        else:
            break


if __name__ == "__main__":
    min_heap = []
    lines = []
    while True:
        line = sys.stdin.readline().strip()
        if not line:
            break
        lines.append(line)
    for i in lines:
        if i[0] == 'A':
            add_element(int(i[2:]))
        else:
            print(extract_min())

