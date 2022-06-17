import os
import sys


class Vertex:
    def __init__(self, key):
        # member id，和key值相同
        self.id = key
        # 统计参加活动的次数
        self.count = 0
        # key为vertex，value 为int（权值）
        self.connectedTo = {}

    # 从这个顶点添加一个连接到另一个
    def addNeighbor(self, nbr, weight=1):
        self.connectedTo[nbr] = weight


class Graph:
    def __init__(self):
        # vertex字典， key为int（member id），value 为vertex
        self.vertList = {}

    def addVertex(self, key):
        newVertex = Vertex(key)
        self.vertList[key] = newVertex
        return newVertex

    def __contains__(self, n):
        return n in self.vertList

    # 用于添加边，边的添加可以看作是有向，因为只针对一个顶点修改邻居，想双向可以调用两次
    # 也可以用用于修改权值
    def addEdge(self, f, t, const=1):
        if f not in self.vertList:
            nv = self.addVertex(f)
        if t not in self.vertList:
            nv = self.addVertex(t)
        self.vertList[f].addNeighbor(self.vertList[t], const)

    def edgeValue(self, f, t):
        if f not in self.vertList.keys() or t not in self.vertList.keys():
            return 0
        elif self.vertList[t] in self.vertList[f].connectedTo.keys():
            return self.vertList[f].connectedTo[self.vertList[t]]
        else:
            return 0

    # 只有开启有权图的时候才有效，因为此时边权相当于并集的势
    def similarityCalc(self, f, t):
        if (self.vertList[f].count + t.count - self.vertList[f].connectedTo[t]) > 0:
            return self.vertList[f].connectedTo[t] / (
                        self.vertList[f].count + t.count - self.vertList[f].connectedTo[t])
        else:
            return 0

    def neighborCalc(self, f, t):
        return len(self.vertList[f].connectedTo.keys() & self.vertList[t].connectedTo.keys()) / \
               len(self.vertList[f].connectedTo.keys() | self.vertList[t].connectedTo.keys())

    def __iter__(self):
        return iter(self.vertList.values())


# 无向图
def build_graph_1(val_id):
    g = Graph()
    path = r'./exp2data/GroupEvent'
    for filename in os.listdir(path):
        event_count = 0
        f = open(path + "\\" + filename, 'r')
        ctx = f.readlines()
        if ctx:
            for line in ctx:
                if line[0] == 'E':
                    event_count = event_count + 1
                    if event_count % 5 == val_id:
                        continue
                if line[0] == 'M':
                    member = line.split()
                    if 'null' in member:
                        member.remove('null')
                    if len(member) >= 2:
                        for i in range(len(member)-1):
                            for j in range(i+1, len(member)):
                                g.addEdge(int(member[i][1:]), int(member[j][1:]), 1)
                                g.addEdge(int(member[j][1:]), int(member[i][1:]), 1)
                    for i in range(len(member)):
                        if int(member[i][1:]) not in g.vertList:
                            g.addVertex(int(member[i][1:]))
                            g.vertList[int(member[i][1:])].count = 1
    return g


# 无向图，权值为同组次数
def build_graph_2(val_id):
    g = Graph()
    path = r'./exp2data/GroupEvent'

    count = 0
    total = len(os.listdir(path))
    for filename in os.listdir(path):
        # 进度显示
        if count+1 == total:
            percent = 100.0
            print('net_Progress: %s [%d/%d]' % (str(percent)+'%', count+1, total), end='\n')
        else:
            percent = round(1.0 * count / total * 100, 2)
            print('net_Progress: %s [%d/%d]' % (str(percent)+'%', count+1, total), end='\r')
        count = count + 1

        # 五折检验文件选取，选取不同的余数即可
        # if count % 5 == 0:
        #    continue

        event_count = 0

        f = open(path + "\\" + filename, 'r')
        ctx = f.readlines()
        if ctx:
            for line in ctx:
                if line[0] == 'E':
                    event_count = event_count + 1
                    if event_count % 5 == val_id:
                        continue
                if line[0] == 'M':
                    member = line.split()
                    if 'null' in member:
                        member.remove('null')
                    if len(member) >= 2:
                        for i in range(len(member)-1):
                            for j in range(i+1, len(member)):
                                g.addEdge(int(member[i][1:]), int(member[j][1:]),
                                          g.edgeValue(int(member[i][1:]), int(member[j][1:])) + 1)
                                g.addEdge(int(member[j][1:]), int(member[i][1:]),
                                          g.edgeValue(int(member[j][1:]), int(member[i][1:])) + 1)
                    for i in range(len(member)):
                        if int(member[i][1:]) not in g.vertList:
                            g.addVertex(int(member[i][1:]))
                        g.vertList[int(member[i][1:])].count = g.vertList[int(member[i][1:])].count + 1
    return g


# example
'''
g = build_graph_1(val_id=0)
for i in g.vertList[48462].connectedTo.keys():
    print(i.id, g.vertList[48462].connectedTo[i], g.similarityCalc(48462, i))
'''