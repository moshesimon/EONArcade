def swapList(sl,pos1,pos2):
    temp = sl[pos1]
    sl[pos1] = sl[pos2]
    sl[pos2] = temp
    return sl 
edges = [2,3,1,2,1,6,4,6,4,5,2,3]#3-2-1-6-4
s = 3
d = 4
if not edges[0] == s:
    edges = swapList(edges,0,1)
for i in range(1,len(edges)-2,2):
    print(i,edges)
    if not edges[i] == edges[i+1]:
        edges = swapList(edges,i+1,i+2)
r = []#edges.copy()
for i in range(len(edges)):
    if i%2 == 0:
        r.append(edges[i])
r.append(edges[-1])
print(r)