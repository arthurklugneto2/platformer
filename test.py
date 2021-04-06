itens = [0,1,2,3,4,5,6]
index = 6

# 0 - 6,0,1
# 1 - 0,1,2
# 3 - 2,3,4
# 6 - 5,6,0

for x in range(3):
    prev = (index-1) % len(itens)
    selc = index % len(itens)
    next = (index+1) % len(itens)

print(prev,' : ',selc,' : ',next)