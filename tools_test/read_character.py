# -*- coding : utf-8-*-
# @Author : yjc

from matplotlib import pyplot as plt
import numpy as np
import networkx as nx
import xlrd
import pandas as pd


def ranking(nodes_c: 'dict', rev=True) -> 'list,list':
    """根据节点中心性输出从大到小的排列
    输入为节点和重要性的字典，输出为排列后的节点和数值
    看结果用。谨慎使用
    """
    dic2asc = sorted(nodes_c, key=nodes_c.__getitem__, reverse=rev)
    nodes_c_value = []
    for k in dic2asc:
        nodes_c_value.append(nodes_c[k])
    return dic2asc, nodes_c_value


def readChineseMap(loc, reverse=False):
    """读数据"""
    df = pd.read_excel(loc)
    data = df.values
    # print("获取到所有的值:\n{}".format(data))
    # print(data[100,1])
    print('行数：', len(data))

    """生成网络，目前没有添加各种权重属性，只考虑了拓扑结构"""
    characters = []
    edges = []

    for line in data:
        characters.append(line[0])

    for line in data:
        for char in line[1]:
            if char != line[0]:
                if char in characters:
                    edges.append((char, line[0]))
    print('连边数：', len(edges))
    # print(edges[0:10])
    # 存入nx网络
    G = nx.DiGraph()
    G.add_nodes_from(characters)
    # G.add_weighted_edges_from(edges)
    G.add_edges_from(edges)
    print('test:', nx.dijkstra_path(G, '手', '热'))

    """看是否反转边的方向，取决于具体意义"""
    if reverse: G = nx.DiGraph.reverse(G)
    print('G读取完成，连边不包含打分信息。此处是有向图，没有加入0频字，后面再处理\n')
    return G


if __name__ == "__main__":
    """测试：度中心性（不考虑出入）"""
    loc = 'ChineseMap.xlsx'
    G = readChineseMap(loc)
    c_degree = nx.degree_centrality(G)
    centrality_degree, centrality_degree_value = ranking(c_degree)
    print('度中心性排序：', centrality_degree[0:30])
    print('方向:', nx.dijkstra_path(G, '手', '热'))
