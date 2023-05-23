import random
list = [0,0,0,0,0,0,0,0,0]

def Computer(list):
    global x,r,c,p
    x = 0
    r = 0
    c = 0
    p = 0
    # def disp(list):
    #     print('===============')
    #     print('|', list[0:3], '|')
    #     print('|', list[3:6], '|')
    #     print('|', list[6:9], '|')
    #     print('===============')

    # function to find the move which can win the game by one move
    def next(list, x):
        global r, c, p
        if x == 'x':
            y = 1
        else:
            y = 'x'
        for i in range(3):
            if list[3 * i:(3 * i + 3)].count(x) == 2 and list[3 * i:(3 * i + 3)].count(0) == 1:
                r = i
                c = list[3 * i:(3 * i + 3)].index(0)
                p = 3 * r + c + 1
                return p
        for j in range(3):
            list1 = []
            list1.append(list[j])
            list1.append(list[j + 3])
            list1.append(list[j + 6])
            if list1.count(x) == 2 and list1.count(0) == 1:
                r = list1.index(0)
                c = j
                p = 3 * r + c + 1
                return p
        list3 = []
        list2 = []
        for k in range(3):
            list2.append(list[4 * k])
            list3.append(list[2 * (k + 1)])
        if list2.count(x) == 2 and list2.count(0) == 1:
            r = list2.index(0)
            p = 4 * r + 1
            return p
        if list3.count(x) == 2 and list3.count(0) == 1:
            r = list3.index(0)
            p = 2 * r + 3
            return p


    # function to find the next best move
    def winp(list):
        x = 'x'
        mlist = [0,0,0,0,0,0,0,0,0]
        for i in range(3):
            if list[3*i:(3*i+3)].count(x) < 1:
                for a in range(3*i,(3*i+3)):
                    mlist[a] += 1

        for j in range(3):
            list1 = []
            list1.append(list[j])
            list1.append(list[j + 3])
            list1.append(list[j + 6])
            if list1.count(x) < 1:
                mlist[j] += 1
                mlist[j+3] += 1
                mlist[j+6] += 1
        list2 = []
        list3 = []
        for c in range(3):
            list2.append(list[4*c])
            list3.append(list[2*(c+1)])
        if list2.count(x) < 1:
            for d in range(3):
                mlist[4*d] += 1
        if list3.count(x) < 1:
            for e in range(3):
                mlist[2*(e+1)] += 1
        max1 = max(mlist)
        for i in range(9):
            if mlist[i] == max1 and list[i] == 'x':
                return i
            mlist[mlist.index(max(mlist))] = 0
            max1 = max(mlist)
            for i in range(9):
                if mlist[i] == max1 and list[i] == 'x':
                    return i

    def listed(list):
        next(list, 'x')
        if p != 0 and list[p - 1] == 0:
            list[p - 1] = 'x'
            return list
        else:
            next(list, 1)
            if p != 0 and list[p - 1] == 0:
                list[p - 1] = 'x'
                return list
            else:
                a = winp(list)
                if list[a - 1] == 0:
                    list[a - 1] = 'x'
                    return list




    dirs = [1, 3, 5, 7]
    adirs = []
    corners = [0, 2, 6, 8]
    acorners = []
    for i in range(9):
        if list[i] == 0 and i in corners:
            acorners.append(i)
        if list[i] == 0 and i in dirs:
            adirs.append(i)
    if list.count(0) == 9:
        list[random.choice(corners)] = 'x'
    if list.count(0) == 7:
        if list.index(1) in dirs:
            if list.index('x') == 0:
                if list.index(1) == 3:
                    list[2] = 'x'
                else:
                    list[6] = 'x'
            if list.index('x') == 2:
                if list.index(1) == 1:
                    list[8] = 'x'
                else:
                    list[0] = 'x'
            if list.index('x') == 6:
                if list.index(1) == 7:
                    list[0] = 'x'
                else:
                    list[8] = 'x'
            if list.index('x') == 8:
                if list.index(1) == 7:
                    list[2] = 'x'
                else:
                    list[6] = 'x'
        if list.index(1) in corners:
            list[random.choice(acorners)] = 'x'
        if list.index(1) not in corners and list.index(1) not in dirs:
            list = listed(list)
    if list.count(0) == 5:
        next(list, 'x')
        next(list, 1)
        if p == 0:
            list[random.choice(acorners)] = 'x'
        else:
            list = listed(list)
    if list.count(0) == 3:
        list = listed(list)
    if list.count(0) == 1:
        list[list.index(0)] = 'x'
    # x = int(input('Enter index: '))
    # list[x] = 1
    # disp(list)
    return list

# print(Computer(['x',0,0,1,1,'x','x',0,1]))