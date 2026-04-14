def binary(left, right, result):
    while left < right:
        mid = (left + right) // 2
        k = len(result) + mid
        print("?", k, *list(range(1, mid + 1)), *result)
        query_result = int(input())
        if query_result % 2 == k % 2:
            left = mid + 1 # it means 0 not in the range [1, mid]
        else:
            right = mid # it means 0 in the range [1, mid]
    result.append(left)


# interactive problem so we have read input when query ? k [x1 x2 ... xk] to get input and print ! a b c to output answer
def solve():
    n = int(input())
    """ A have 2n + 1 member (1,2,...,n) 1 number repeat 3 times others repeat 2 times, 
    we need to find index the one that repeat 3 times. Print index of member that repeat
    3 times, print ! a b c to output answer. We can do this by query ? k [x1 x2 ... xk] 
    to get input number unique X, mean X number that unique in the array [Ax1, Ax2, ... Axk]
    
    if i query 1--k and add 1--(k+1) the result will increase by 1, decrease by 1 or stay 
    the same, it only stay the same when the number that repeat 3 times is in the range [1, k+1] 
    and it will increase if new number is unique others it will decrease.
    """ 
    result = []
    binary(1, 2 * n + 1, result)
    binary(1, result[-1] - 1, result)
    binary(1, result[-1] - 1, result)
    print("!", *result)
    

t = int(input())
for _ in range(t):
    solve()