import math

def dot(lia,lib):#向量点乘
    s = 0
    for i in range(len(lia)):
        s += lia[i]*lib[i]
    return s

def addE(lia,lib):#向量按元素相加
    res = []
    for i in range(len(lia)):
        res.append(lia[i]+lib[i])
    return res

def minusE(lia,lib):#向量按元素相减
    res = []
    for i in range(len(lia)):
        res.append(lia[i]-lib[i])
    return res

def mulE(lia,lib):#向量按元素相乘
    res = []
    for i in range(len(lia)):
        res.append(lia[i]*lib[i])
    return res

def divE(lia,lib):#向量按元素相除
    res = []
    for i in range(len(lia)):
        res.append(lia[i]/lib[i])
    return res

def sqtE(lia):#向量按元素开方
    res = []
    for i in range(len(lia)):
        res.append(math.sqrt(lia[i]))
    return res

def SxV(s,vec):#标量乘以向量
    res = []
    for i in range(len(vec)):
        res.append(s*vec[i])
    return res

def pV(lia):#打印向量
    for row in lia:
        for item in row:
            print(item,end=" ")
        print()

def T(lia):#矩阵转制
    nrow = len(lia)
    ncol = len(lia[0])
    res = []
    for i in range(ncol):
        row = []
        for j in range(nrow):
            row.append(lia[j][i])
        res.append(row)
    return res

def iso(lia):#是否为0向量
    for i in lia:
        if i!=0:return False
    return True

def zeroV(n):#生成0向量
    return [0 for i in range(n)]