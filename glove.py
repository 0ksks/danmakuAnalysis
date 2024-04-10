import jieba
import pandas as pd
import random as r
import math
from utils import *
from vec import *
from matplotlib.pyplot import plot,show
fpath=""
def read(amount):#读取原始数据 amount为数量，设为-1读取全部
    ts = pd.read_csv(fpath+"trainSet.csv")
    goodCnt = 0
    res = []
    lgth = len(ts['cat'])
    for i in range(1,lgth):
        if amount!=-1:
            try:
                if ts["label"][i]==1 and goodCnt<amount//2:
                    res.append([ts['cat'][i],ts['label'][i],"".join(ts['review'][i].split())])
                    goodCnt+=1
                elif ts["label"][i]==0 and not goodCnt<amount//2:
                    res.append([ts['cat'][i],ts['label'][i],"".join(ts['review'][i].split())])
                else:
                    pass
            except:
                pass
            procedure(i,lgth,"正在拉取","拉取完成")
            if len(res)>amount:break
        else:
            res.append([ts['cat'][i],ts['label'][i],"".join(ts['review'][i].split())])
    return res

def cut(amount):#分词
    res = read(amount)
    lgth = len(res)
    for i in range(lgth):
        try:
            tmp = jieba.lcut(res[i][-1])
            for j in range(len(tmp)):
                if '0'<=tmp[j][0]<='9':
                    tmp[j]='<num>'
            res[i][-1] = tmp
        except:
            pass
        procedure(i,lgth,"正在分词","分词完成")
    ress = []
    for i in range(lgth):
        procedure(i,lgth,"正在筛选","筛选完成")
        try:
            if len(res[i][2]) < 200:
                ress.append(res[i])
        except:
            pass
    toExcel(ress,"trainSetCut")

def wordSeq(unk):#生成词典 词频低于unk值(不包括unk)则记录为<unk>
    df = fromExcel("trainSetCut")
    dic = {}
    for i in range(len(df[0])):
        try:
            wl = eval(df[2][i])
            for j in range(len(wl)):
                if wl[j] in dic.keys():
                    dic[wl[j]]+=1
                else:
                    dic[wl[j]]=1
            procedure(i,len(df[0]))
        except:
            pass
    step1 = [[key,value] for key,value in dic.items()]
    step1.sort(key=lambda x:x[1])
    step2 = []
    unkCnt = 0
    for i in range(len(step1)):
        if step1[i][1]>=unk:
            step2.append(step1[i])
        else:
            unkCnt+=step1[i][1]
    step2.sort(key=lambda x:ord(x[0][0]))
    step2.append(["<pad>",0])
    step2.append(["<unk>",unkCnt])
    res = step2
    toExcel(res,"dict")

def finalTrainSet(pad):#padding 长度高于pad的句子在pad处截断，低于的句子用<pad>(在wordVec中为倒数第二个)填充
    wordDic = fromExcel("dict")[0]
    trainSetCut = fromExcel("trainSetCut")
    catagories = trainSetCut[0]
    label = trainSetCut[1]
    words = trainSetCut[2]
    sentences = []
    padIdx = len(wordDic)-2
    for i in range(len(words)):
        procedure(i,len(words))
        try:
            tmp = []
            sentence = eval(words[i])
            for j in range(pad):
                if j<len(sentence):
                    tmp.append(getIdx(wordDic,sentence[j]))
                else:
                    tmp.append(padIdx)
            sentences.append([catagories[i],label[i],tmp])
        except:
            pass
    toExcel(sentences,"finalTrainSet")

def coMatrix(maxWinLen):#计算共现矩阵
    dic = list(fromExcel("dict")[0])
    n = len(dic)
    coMat=[]
    row = [0 for j in range(n)]
    for i in range(n):
        procedure(i,n,"coMat正在初始化","coMat初始化完成")
        coMat.append(row.copy())
    df = fromExcel("finalTrainSet")
    dfl = len(df[2])
    for k in range(dfl):
        try:
            wl = eval(df[2][k])
            lgwl = len(wl)
            sst = "处理句子%d/%d %d"%(k+1,dfl,round((k+1)*100/dfl))+"% "
            for i in range(lgwl):
                winLen = r.randint(1,maxWinLen)
                procedure(i,lgwl,sst+"处理单词",sst+"处理完成")
                x = wl[i]
                ed = i + winLen + 1
                if ed > lgwl-1:ed = lgwl
                for j in range(i+1,ed):
                    y = wl[j]
                    val = round(1/(j-i),3)
                    coMat[x][y]+=val
                    coMat[y][x]+=val
        except:
            pass
    toExcel(coMat,'coMat')

def iniWordVec(dim):#初始化词向量
    dic = fromExcel('dict')
    n = len(dic[0])
    res = []
    for i in range(n):
        res.append([[r.randint(0,9) for i in range(dim)],[r.randint(0,9) for i in range(dim)]])
    return res

def f(x,alpha=0.75,xmax=3):#损失函数中的fx
    if x>=xmax:
        return 1
    return (x/xmax)**alpha

def wwbbl(wordVec,bi,bj,comat,i,j):#损失函数平方项的底
    if comat[i][j]==0:
        return 0
    summ = 0
    summ += dot(wordVec[i][0],wordVec[j][1])
    summ += bi[i]+bj[j]
    summ += -math.log(comat[i][j])
    return summ

def J(comat,wordVec,bi,bj):#损失函数
    summ = 0
    for i in range(len(comat)):
        for j in range(len(comat)):
            summ += f(comat[i][j])*wwbbl(wordVec,bi,bj,comat,i,j)*wwbbl(wordVec,bi,bj,comat,i,j)
    return summ

def trainWordVec(restart,dim,maxEpoch,eta0,eta1,turning,beta1=0.9,beta2=0.999):#训练词向量（restart：是否重新训练；dim：词向量维度；maxEpoch：最大轮数；eta0：初始学习率；eta1：降低后的学习率；turning：降低学习率的轮数
    comat = fromExcel('coMat')
    wordVec = []
    if restart == 1:
        wordVec = iniWordVec(dim)
        lossLog = ""
    else:
        wv = fromExcel("wordVec",0)
        for i in range(len(wv[0])):
            wordVec.append([eval(wv[0][i]),eval(wv[1][i])])
        with open(fpath+"lossLog.txt") as fp:
            lossLog = fp.read()
    wordAcnt = len(wordVec)#词数量
    epsilon = 1e-6
    epsilonList = [epsilon for i in range(dim)]
    

    bi = [r.randint(0,9) for i in range(wordAcnt)]
    bj = [r.randint(0,9) for i in range(wordAcnt)]

    v = 0
    s = 0

    beta1t = 1
    beta2t = 1

    percent = 0.1
    batchSize = round(wordAcnt*percent)

    eta = eta0
    for times in range(maxEpoch):#adam
        if times==turning:
            eta = eta1
        beta1t *= beta1
        beta2t *= beta2
        wordGradList = []
        bGradList = []
        centreWordVLast = [zeroV(dim) for i in range(wordAcnt)]
        centreWordSLast = [zeroV(dim) for i in range(wordAcnt)]
        contextWordVLast = [zeroV(dim) for i in range(wordAcnt)]
        contextWordSLast = [zeroV(dim) for i in range(wordAcnt)]
        vLast = [0 for i in range(wordAcnt)]
        sLast = [0 for i in range(wordAcnt)]
        stdFig = str(times+1)+(figLen(maxEpoch)-len(str(times+1)))*" "
        sstr = "epoch "+stdFig+" | word"
        for para in range(wordAcnt):#遍历所有参数
            procedure(para,wordAcnt,sstr,sstr)
            centreWordV = zeroV(dim)
            centreWordS = zeroV(dim)
            contextWordV = zeroV(dim)
            contextWordS = zeroV(dim)
            batchRange = r.sample(range(wordAcnt),batchSize)
            centreWordGrad = zeroV(dim)
            contextWordGrad = zeroV(dim)
            bGrad = 0
            for i in batchRange:#小批量随机梯度
                cewgrad = zeroV(dim)
                cowgrad = zeroV(dim)
                for j in batchRange:
                    cewgrad = addE(cewgrad,SxV(2*f(comat[i][j])*wwbbl(wordVec,bi,bj,comat,i,j),wordVec[j][1]))
                    cowgrad = addE(cowgrad,SxV(2*f(comat[i][j])*wwbbl(wordVec,bi,bj,comat,i,j),wordVec[i][0]))
                    bGrad += 2*f(comat[i][j])*wwbbl(wordVec,bi,bj,comat,i,j)
                centreWordGrad = addE(centreWordGrad,cewgrad)
                contextWordGrad = addE(contextWordGrad,cowgrad)
            centreWordGrad = SxV(1/batchSize, centreWordGrad)
            centreWordV = addE(SxV(beta1, centreWordVLast[para]), SxV(1-beta1, centreWordGrad))
            centreWordS = addE(SxV(beta2, centreWordSLast[para]), SxV(1-beta2, mulE(centreWordGrad, centreWordGrad)))
            centreWordV = SxV(1/(1-beta1t), centreWordV)
            centreWordS = SxV(1/(1-beta2t), centreWordS)
            centreWordVLast[para] = centreWordV
            centreWordSLast[para] = centreWordS
            centreWordGrad = SxV(eta, divE(centreWordV, addE(sqtE(centreWordS), epsilonList)))

            contextWordGrad = SxV(1/batchSize, contextWordGrad)
            contextWordV = addE(SxV(beta1, contextWordVLast[para]), SxV(1-beta1, contextWordGrad))
            contextWordS = addE(SxV(beta2, contextWordSLast[para]), SxV(1-beta2, mulE(contextWordGrad, contextWordGrad)))
            contextWordV = SxV(1/(1-beta1t), contextWordV)
            contextWordS = SxV(1/(1-beta2t), contextWordS)
            contextWordVLast[para] = contextWordV
            contextWordSLast[para] = contextWordS
            contextWordGrad = SxV(eta, divE(contextWordV, addE(sqtE(contextWordS), epsilonList)))

            bGrad = bGrad/batchSize
            v = beta1*vLast[para] + (1-beta1)*bGrad
            s = beta2*sLast[para] + (1-beta2)*bGrad*bGrad
            v = v/(1-beta1t)
            s = s/(1-beta2t)
            bGrad = eta*v/(math.sqrt(s)+epsilon)
            vLast[para] = v
            sLast[para] = s
            wordGradList.append([centreWordGrad,contextWordGrad])

            bGradList.append(bGrad)

        for i in range(wordAcnt):
            wordVec[i][0] = minusE(wordVec[i][0],wordGradList[i][0])
            wordVec[i][1] = minusE(wordVec[i][1],wordGradList[i][1])
            bi[i] -= bGradList[i]
            bj[i] -= bGradList[i]
        loss = J(comat,wordVec,bi,bj)
        print(" loss=%d"%(loss))
        lossLog+="%d,"%(loss)
        if times%10==9:
            lossLog+="\n"
        if times%20==19:
            print("save")
            toExcel(wordVec,'wordVec',0)
            with open(fpath+"lossLog.txt","w") as fp:
                fp.write(lossLog)
    toExcel(wordVec,'wordVec')
    with open(fpath+"lossLog.txt","w") as fp:
        fp.write(lossLog)

def plotLoss():#显示损失函数图像
    with open(fpath+"lossLog.txt") as fp:
        y = fp.read()
    y = "[%s]"%("".join(y.split("\n"))[:-2])
    y = eval(y)
    x = [i+1 for i in range(len(y))]
    plot(x,y)
    show()

def getWordVec():#读取词向量
    wordVec = fromExcel("wordVec")
    res = []
    for i in range(len(wordVec[0])):
        res.append(addE(eval(wordVec[0][i]),eval(wordVec[1][i])))
    return res

def getSentencesAndLabels():#获取训练集
    finalTrainSet = fromExcel("finalTrainSet",0)
    wordVec = getWordVec()
    sentences = list(map(eval,list(finalTrainSet[2])))
    for i in range(len(sentences)):
        for j in range(len(sentences[i])):
            sentences[i][j]=wordVec[sentences[i][j]]
    labels = list(finalTrainSet[1])
    return (sentences, labels)

if __name__=="__main__":
    trainWordVec(1,2,2,0.05,0.01,50)