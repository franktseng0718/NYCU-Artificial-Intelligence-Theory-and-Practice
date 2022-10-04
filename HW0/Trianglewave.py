case = int(input())
case = case
for i in range(case):
    l = input()
    a = int(input())
    f = int(input())
    for j in range(f):
        for k in range(1, a*2):
            if k > a:
                times = 2*a - k
            else:
                times = k
            for t in range(times):
                print(times, end="")
            print()
        if j != f-1:
            print()
    if i != case-1:
        print()