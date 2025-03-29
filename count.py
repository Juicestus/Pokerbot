k = .4

with open('NewEV.txt', 'r') as f:
    v = [float(l.strip()) for l in f]
    n = 0
    for x in v:
        if x < k:
            n+= 1
            
    print(n, n/len(v))

            