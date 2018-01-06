# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 20:41:43 2017

@author: majin
"""

import numpy as np
def kernels(nodes,Eps,MinPts):
    '''
    标记所有的点是不是核心点,是nodes[2]=-1,不是nodes[2]=-2
    @nodes
        (n,3) 要标记的点
    @Eps
        范围半径
    @MinPts
        范围内的最少点数
    @return 
        nodes,node_nears
        标记后的点集，以及每个点的临近点
    '''
    node_pisi = np.copy(nodes)
    n = nodes.shape[0]
    nodes_nears = []
    
    
    nodes_nears = []
    for i in range(n):  #第i个点
                
        #第i点到其他点的距离
        res = np.sum(np.sqrt(np.power(node_pisi[i]-node_pisi,2)),axis=1,keepdims=True)
        
        #统计距离小于Eps的点的个数,并记录i点的临近点
        l_nodes = np.less(res,Eps)
        LtEpsCount = np.count_nonzero(l_nodes)
        
        #判断是不是核心点
        if LtEpsCount >= MinPts:
            #保存i点的所有临近点
            the_node_nears = np.where(l_nodes)
            #只保存核心点的邻接点
            nodes_nears.append(the_node_nears[0].tolist())
            nodes[i][2] = -1
        else:
            nodes_nears.append([])
            nodes[i][2] = -2
    return nodes,nodes_nears

def DBScan(nodes,Eps,MinPts):
    '''
    -3代表噪音，-2表示未遍历的非核心，-1表示未遍历的核心点,>0遍历的核心点
    '''
    #标记处所有的核心点
    nodes,nodes_nears = kernels(nodes,Eps,MinPts)
    
    n = nodes.shape[0]
    c = 0
    for i in range(n):
        #print(str(round(i/n*100,2))+"%")
        if nodes[i][2]==-2:#未遍历的非核心
            nodes[i][2] = -3#-3代表噪音
            continue
        elif nodes[i][2]==-1:#是未遍历的核心点
            nodes[i][2] = c#标记P为c
            P_near = nodes_nears[i] #取出P的临近点
            for ii in P_near:
                ii = int(ii)
                if nodes[ii][2] == -2 or nodes[ii][2]==-3:#是噪声或未遍历的非核心
                    nodes[ii][2] = c
                elif nodes[ii][2] == -1:#是未遍历的核心点
                    nodes[ii][2] = c
                    #将P'的临近点加入到M
                    for shouldExt in nodes_nears[ii]:
                        if shouldExt not in P_near:
                            P_near.append(shouldExt)
            c += 1
    return nodes,c
    
    