T = int(input())
for _ in range(T):
    n = int(input())
    a = list(map(int,input().split()))
    wrong = False
    mp = {}
    for i in a:
        if i in mp:
            wrong = True
            break
        mp[i] = True
    if wrong:
        print("YES")
    else:
        print("NO")