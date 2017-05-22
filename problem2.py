'''
CS300 HW10: Implementing Edit Distance
    Due date: 2017-05-22 10 am
    Team number: 26
    Names: 20130416 SEUNGHEE YOON, 20130289 haeorem park
'''


def print_matrix(lst):
    for elem in lst:
        print(elem)
    print()

def InputHandler():
    r1 = open("raw1.txt", "r")
    raw1 = r1.read().rstrip()
    r2 = open("raw2.txt", "r")
    raw2 = r2.read().rstrip()

    d1 = {}
    d2 = {}
    for i in range(1, len(raw1)+1):
        d1[i] = raw1[i-1]
    for j in range(1, len(raw2)+1):
        d2[j] = raw2[j-1]
    d1[0] = ''
    d2[0] = ''
    return d1, d2

def Edit_distance():
    d1, d2 = InputHandler()
    l1 = len(d1)-1; l2= len(d2)-1
    Edit, Track = Init_DP(l1,l2)
    #Track = [ [ 0 for i in range(l2+1)] for j in range(l1+1)]
    for i in range(1, l1+1):
        for j in range(1, l2+1):
            A = Edit[i-1][j] + 1
            B = Edit[i][j-1] + 1
            C = Edit[i-1][j-1]
            if d1[i] == d2[j]:
                Edit[i][j] = min(A,B,C)
                if A <= B and A <= C:
                    Track[i][j] = (i-1,j)
                if B <= A and B <= C:
                    Track[i][j] = (i,j-1)
                if C <= A and C <= B:
                    Track[i][j] = (i-1,j-1, False)
            else:
                Edit[i][j] = min(A,B,C+1)
                if A <= B and A <= C+1:
                    Track[i][j] = (i-1,j)
                if B <= A and B <= C+1:
                    Track[i][j] = (i,j-1)
                if C+1 <= A and C+1 <= B:
                    Track[i][j] = (i-1,j-1, True)
    print("Edit Matrix: ")
    print_matrix(Edit)
    print("Track Matrix: ")
    print_matrix(Track)
    return Edit, Track, d1, d2


def Init_DP(l1,l2):
    Edit = [ [ 0 for i in range(l2+1)] for j in range(l1+1) ]
    for j in range(1, l2+1):
        Edit[0][j] = j
    for i in range(1, l1+1):
        Edit[i][0] = i
    Track = [[0 for i in range(l2 + 1)] for j in range(l1 + 1)]
    for j in range(1, l2+1):
        Track[0][j] = (0,j-1)
    for i in range(1,l1+1):
        Track[i][0] = (i-1,0)
    return Edit, Track

def Backtrack():
    Edit, Track, d1, d2 = Edit_distance()
    output =[dictionary_read(d1)]
    coordinate = (len(d1)-1, len(d2)-1)
    B = []
    B.append(coordinate)
    while True:
        coordinate = Track[coordinate[0]][coordinate[1]]
        B.append(coordinate)
        if (coordinate[0]+coordinate[1]==0): break;
    B.reverse()
    print("Backtrack:", B)
    for i in range(1,len(B)):
        if B[i][0]-B[i-1][0]==1 and B[i][1]-B[i-1][1]==0:
            del_index = B[i][0]
            d1[del_index] = 'del'
        elif B[i][0]-B[i-1][0]==0 and B[i][1]-B[i-1][1]==1:
            insert_index = B[i][0]
            d1[insert_index] = d1[insert_index] + d2[B[i][1]]
        elif B[i][0]-B[i-1][0]==1 and B[i][1]-B[i-1][1]==1:
            if B[i-1][2] is True:
                d1[B[i][0]] = d2[B[i][1]]
        if output[-1] != dictionary_read(d1):
            output.append(dictionary_read(d1))
    print("output:", output)
    return output

def dictionary_read(d):
    ret = ''
    for i in range(0,len(d)):
        if d[i] != 'del':
            ret += d[i]
    return ret

def OutputHandler():
    output = Backtrack()
    f = open("output.txt", "w")
    for i in range(len(output)):
        f.write(output[i])
        if i != len(output)-1:
            f.write("\n")
    f.close()

OutputHandler()