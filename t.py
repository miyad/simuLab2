import heapq

q = []
heapq.heappush(q,(2,4))
heapq.heappush(q,(4,3))
heapq.heappush(q,(-1,2))
while len(q)>0:
    t = heapq.heappop(q)
    print(t)
a = ["miyad",4]
print(a)