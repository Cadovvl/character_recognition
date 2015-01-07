# -*- coding: utf-8 -*-
from nltk.tokenize import word_tokenize
import re
import numpy as np   
      
def EmissionProb(dictList):
    for indexToFrequensy in dictList:
        for phraseAndIndex in indexToFrequensy:
            if phraseAndIndex[0] == phraseAndIndex[0].capitalize():
                indexToFrequensy[phraseAndIndex]+= 0.2
                if len(phraseAndIndex[0]) > 1:
                    indexToFrequensy[phraseAndIndex]+= 0.2
                    if phraseAndIndex[1]!=0:
                        indexToFrequensy[phraseAndIndex]+= 0.3
                    else:
                        indexToFrequensy[phraseAndIndex] = indexToFrequensy[phraseAndIndex] 
                        - 0.2
    return dictList
    
def TransProbFor4(zipList):
    sumForTransProb=[]
    lenForTransProb=[]
    listOfPercent0=[]
    for zipNums in zipList: 
        if zipNums[1]!=0:
            sumForTransProb.append(sum([zipNums[0] for zipNums in zipList[:int(zipNums[1])]]))
    print sumForTransProb
    for zipNums in zipList: 
        if zipNums[1]!=0:
            lenForTransProb.append(len([zipNums[0] for zipNums in zipList[:int(zipNums[1])]]))
    print lenForTransProb
    listOfPercent0.append(0.8)
    for i in range(len(sumForTransProb)):
        listOfPercent0.append(round(float(sumForTransProb[i]/float(lenForTransProb[i])+0.15),2))
    print listOfPercent0
    return listOfPercent0
    
def TransProb(indexAndNum):
    for zipList in indexAndNum:
        if len(zipList)==2:
            percent0[indexAndNum.index(zipList)].extend([0.2, 0.4])
            
        elif len(zipList)==3:
            percent0[indexAndNum.index(zipList)].extend([0.3, 0.3, 0.1])
        else:
            percent0[indexAndNum.index(zipList)].extend(TransProbFor4(zipList))
    return percent0
    
def ProbMaker(sent1,sent2):
    probability = np.array([sent1,sent2])
    return probability
    
def viterbi(obs, states, start_p, trans_p, emit_p):
    V = [{}]
    path = {}
    for y in states:
        V[0][y] = start_p[y] * emit_p[y][obs[0]]
        path[y] = [y]
    for t in range(1, len(obs)):
        V.append({})
        newpath = {} 
        for y in states:
            (prob, state) = max((V[t-1][y0] * trans_p[y0][y] * emit_p[y][obs[t]], y0) for y0 in states)
            V[t][y] = prob
            newpath[y] = path[state] + [y]
        path = newpath
    n = 0           # if only one element is observed max is sought in the initialization values
    if len(obs) != 1:
        n = t
    print_dptable(V)
    (prob, state) = max((V[n][y], y) for y in states)
    return (prob, path[state])
    
def print_dptable(V):
    s = "" + "  ".join(("%7d" % i) for i in range(len(V))) + "\n"
    for y in V[0]:
        s += "%.5s: " % y
        s += "  ".join("%.7s" % ("%f" % v[y]) for v in V)
        s += "\n"
    print(s)


    
f=open('tom.txt', 'r')
text=f.read()
phrase1 = re.compile("\,|\:|\n|\'|;")
text = phrase1.sub(" ", text)
phrase2 = re.compile('\!|\"|\?')
text = phrase2.sub('.', text)
text = text.split(".")
wordList = []
for phrase in text:
    wordList.append(word_tokenize(phrase))    
for i in wordList:
    if len(i)<2:
        wordList.remove(i)
dictList=[]
zipList = []
percentage1 = []
percentage0 = []
probableIndexEmission=[]
sumForTransProb=[]
lenForTransProb=[]
percent0 = [] 
percent1 = []     
for i in range(len(wordList)):
    dictList.append({})
    percentage0.append([])
    probableIndexEmission.append([])
    sumForTransProb.append([])
    lenForTransProb.append([])  
    percent0.append([]) 
    percent1.append([]) 
zipList = [zip(phrase, range(len(phrase))) for phrase in wordList]
for phrase in zipList:
    for phraseAndIndex in phrase:
        dictList[zipList.index(phrase)].update([(phraseAndIndex,0)])      
dictList = EmissionProb(dictList)                    
for i in dictList:
    percentage1.append(i.values())
    for num in i.values():
        percentage0[dictList.index(i)].append(1-num)
for lists in percentage1:
    for number in lists:
        if number<0.5:
            probableIndexEmission[percentage1.index(lists)].append(0)
        else:
            probableIndexEmission[percentage1.index(lists)].append(1)        
indexAndNum = []  
for lists in probableIndexEmission:
    indexAndNum.append(zip(lists,range(len(lists))))
percent0=TransProb(indexAndNum)

for lists in percent0:     
    for number in lists:
        percent1[percent0.index(lists)].append(round((1-number),2))
states = [0, 1]
start_probability = np.array([0.8, 0.2])
for i in range(len(percent0)):
    emission_probability = ProbMaker(percentage0[i],percentage1[i])
    transition_probability = ProbMaker(percent0[i],percent1[i])
    observations = [i for i in range(len(percent0[i]))]
    print viterbi(observations,states,start_probability,transition_probability,emission_probability)
