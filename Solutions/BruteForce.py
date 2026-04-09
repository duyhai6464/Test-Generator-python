n, q = map(int, input().split())
arr = list(map(int, input().split()))
for _ in range(q):
    # query is "sum l r" or "add l r x"
    query = input().split()
    query_type = query[0]
    l = int(query[1])
    r = int(query[2])
    if query_type == "sum":
        print(sum(arr[l - 1:r]))
    elif query_type == "add":
        x = int(query[3])
        for i in range(l - 1, r):
            arr[i] += x