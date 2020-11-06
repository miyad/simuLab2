import heapq
import numpy as np
q = []
heapq.heappush(q,(2,4))
heapq.heappush(q,(4,3))
heapq.heappush(q,(-1,2))
while len(q)>0:
    t = heapq.heappop(q)
    print(t)
a = []
a.append((2,4))
t,c = a.pop(0)
print(t)
print(c)
a = [2,3,5]
b = [3,5,1]
a = np.add(a,b)
print(a)
