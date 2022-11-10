import math
from sklearn import datasets
from sklearn.metrics import accuracy_score
import numpy as np
def entropy(p1, n1):
    if p1==0 and n1==0:
        return 1
    elif p1==0 or n1==0:
        return 0
    else:
        pp = p1/(p1+n1)
        np = n1/(p1+n1)
        return -pp*math.log2(pp) - np*math.log2(np)

def Information_gain(p1, n1, p2, n2):
    num1 = p1 + n1
    num2 = p2 + n2
    if num1==0 or num2==0:
        return 0
    num = num1 + num2
    entropy_l = num1/num * entropy(p1, n1)
    entropy_r = num2/num * entropy(p2, n2)
    return entropy(p1 + p2, n1 + n2) - entropy_l - entropy_r

def ID3DTtrain(feature, target):
    node = dict()
    node['data'] = range(len(target))
    tree = []
    tree.append(node)
    t = 0
    while(t<len(tree)):
        idx = tree[t]['data']
        #print(target[idx])
        if(sum(target[idx])==0):
            #print('leaf:0')
            tree[t]['leaf'] = 1
            tree[t]['decision'] = 0
        elif(sum(target[idx])==len(idx)):
            #print('leaf:1')
            tree[t]['leaf'] = 1
            tree[t]['decision'] = 1
        else:
            best_IG = 0  # best information_gain
            for i in range(feature.shape[1]):
                pool = list(set(feature[idx, i]))
                pool.sort()
                for j in range(len(pool)-1):
                    thres = (pool[j] + pool[j+1]) / 2
                    G1 = []   # group 1
                    G2 = []   # group 2
                    for k in idx:
                        if feature[k][i]<thres:
                            G1.append(k)
                        else:
                            G2.append(k)
                    p1 = sum(target[G1]==1)
                    n1 = sum(target[G1]==0)
                    p2 = sum(target[G2]==1)
                    n2 = sum(target[G2]==0)
                    this_IG = Information_gain(p1, n1, p2, n2)
                    if this_IG > best_IG:
                        best_IG = this_IG
                        best_G1 = G1
                        best_G2 = G2
                        bestthres = thres
                        bestf = i
            if best_IG > 0:
                tree[t]['leaf'] = 0
                tree[t]['selectf'] = bestf
                tree[t]['threshold'] = bestthres
                tree[t]['child'] = [len(tree), len(tree)+1]
                node = dict()
                node['data'] = best_G1
                tree.append(node)
                node = dict()
                node['data'] = best_G2
                tree.append(node)
            else:
                tree[t]['leaf'] = 1
                if(sum(target[idx]==1) > sum(target[idx]==0)):
                    tree[t]['decision'] = 1
                else:
                    tree[t]['decision'] = 0
        t += 1
    return tree

def get_predict(tree, feature):
    now = 0
    while(tree[now]['leaf']==0):
        bestf = tree[now]['selectf']
        thres = tree[now]['threshold']
        if feature[bestf]<thres:
            now = tree[now]['child'][0]
        else:
            now = tree[now]['child'][1]
    return tree[now]['decision']

def ID3DTtest(tree, features, target):
    predict = []
    for feature in features:
        predict.append(get_predict(tree, feature))
    res = accuracy_score(target, predict)
    return res

if __name__ == '__main__':
    data = datasets.load_iris()
    #print(data)
    feature = data['data']
    target = data['target']

    T  = ID3DTtrain(feature[50:150, :], target[50:150] - 1)
    res = ID3DTtest(T, feature[50:150, :], target[50:150] - 1)
    print(f"acc:{res}")

    # 30 for train, 20 for test
    train_features = np.concatenate((feature[50:80, :] , feature[100:130, :]))
    train_targets = np.concatenate((target[50:80], target[100:130]))
    test_features = np.concatenate((feature[80:100, :] , feature[130:150, :]))
    test_targets = np.concatenate((target[80:100], target[130:150]))
    #print(test_targets.shape)
    T = ID3DTtrain(train_features, train_targets - 1)
    res = ID3DTtest(T, test_features, test_targets - 1)
    print(f"acc:{res}")

