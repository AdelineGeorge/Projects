import sys
import math

lines = []
while True:
    line = sys.stdin.readline().strip()
    if not line:
        break
    lines.append(line)

min_heap = []

def add_element(x):
    min_heap.append(x)
    print(min_heap)
    size = len(min_heap)
    bubble_up(size) 
    print(min_heap)
   

def extract_min()   :
    min = min_heap[0]
    size = len(min_heap)
    min_heap[0] = min_heap[size - 1]
    min_heap.pop()
    size = len(min_heap)
    size = size - 1
    if size >=1:
        sink_down(0)
    return min


def bubble_up(i):
    parent = math.trunc((i / 2) - 1)
    child = i - 1
    print("child:",min_heap[child], " - ","parent:",min_heap[parent])


    while child >=1 and min_heap[child] < min_heap[parent]:
            print("child:",child, " - ","parent:",parent)
            print("swapping child and parent")
            print("child:",min_heap[child], " - ","parent:",min_heap[parent])
            t = min_heap[parent]
            min_heap[parent] = min_heap[child]
            min_heap[child] = t
            child = parent
            parent = math.trunc(child / 2 - 1)

    '''
    while child >= 1:
        #parent = int(math.floor(i / 2) - 1)
        print("child:",child, " - ","parent:",parent)
        print("child:",min_heap[child], " - ","parent:",min_heap[parent])

        if min_heap[child] < min_heap[parent]:
            #print("child:",child, " - ","parent:",parent)
            print("swapping child and parent")
            #print("child:",min_heap[child], " - ","parent:",min_heap[parent])
            t = min_heap[parent]
            min_heap[parent] = min_heap[child]
            min_heap[child] = t
            child = parent
            parent = math.trunc(child / 2 - 1)
        else:
            break
        '''
        
def sink_down(i):
    while 2*i <= len(min_heap) - 1:
        if 2*i == len(min_heap) - 1 or min_heap[2*i] <= min_heap[2*i + 1]:
            j = 2 * i
        else:
            j = 2 * i + 1

        if min_heap[j] < min_heap[i]:
            t = min_heap[i]
            min_heap[i] = min_heap[j]
            min_heap[j] = t
            i = j
        else:
            break

for l in lines:
    print("adding :",l,"\n")
    add_element(l)

#print(min_heap)

'''
extract_min()
print(min_heap)
'''


'''
result = lines
for i in range(len(result)):
    print(result[i])
'''