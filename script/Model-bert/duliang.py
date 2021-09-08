import nltk
from nltk.corpus import wordnet
from nltk import data
def correlation(n1,n2):
    
    num = 0
    weight = 0
    syns0 = wordnet.synsets(n1)
    syns1 = wordnet.synsets(n2)

    for k1 in syns0:
        x1=str(k1)
        y1=x1.split('(')[1].split(')')[0]
        z1=y1.split("'")[1][0:len(y1)]

        if "'" in z1:
            continue
        if len(z1.split('.')) ==1:
            continue
        if(z1.split('.')[0]!=n1):
            continue
        w1=wordnet.synset(z1)
        for k2 in syns1:
            x2=str(k2)
            y2=x2.split('(')[1].split(')')[0]
            z2=y2.split("'")[1][0:len(y2)]
            if "'" in z2:
                # print('**')
                continue
            if len(z2.split('.')) ==1:
                continue
            if(z2.split('.')[0]!=n2):
                continue
            w2=wordnet.synset(z2)
            if(w1.path_similarity(w2) == None):
                w = 0
            else:
                w = w1.path_similarity(w2)
            num  += 1
            weight +=w
    #        print(z1,'----',z2)
   #         print('--',w,'---')
  #  print(num)
 #   print(weight)
    return weight

#x="like"
#y="similarity"
#correlation(x,y)
