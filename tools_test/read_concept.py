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


def readConceptMap(loc, reverse=False):
    """读取概念关系抽取的表格
    输入xlsx文件的路径，读取处有向网络G
    reverse为True时翻转网络，默认不翻转
    """
    #读数据
    df = pd.read_excel(loc, keep_default_na=False)
    data = df.values
    # print("获取到所有的值:\n{}".format(data))
    print('行数：', len(data))

    """生成网络"""
    characters = []
    edges = []

    for line in data:
        if line[0] != '':
            concept = line[0]
            if line[2] != '': edges.append((line[2], concept))

        else:
            if line[2] != '': edges.append((line[2], concept))

    print('连边数：', len(edges))

    # 存入nx网络
    G = nx.DiGraph()
    G.add_edges_from(edges)

    """看是否反转边的方向，取决于具体意义"""
    if reverse: G = nx.DiGraph.reverse(G)

    print('G读取完成\n')
    return G


if __name__ == "__main__":

    """测试：度中心性（不考虑出入）"""
    loc = '概念关系抽取11-5.xlsx'
    G = readConceptMap(loc)
    c_degree = nx.degree_centrality(G)
    centrality_degree, centrality_degree_value = ranking(c_degree)
    print('度中心性排序：', centrality_degree[0:30])

    # 输出文件，可以到gephi软件画图用
    nx.write_gexf(G, 'temp.gexf')

    # 正确显示汉字windows用
    # plt.rcParams['font.sans-serif']=['SimHei']
    # plt.rcParams['axes.unicode_minus'] = False

    # 正确显示汉字mac用
    plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
    plt.rcParams['axes.unicode_minus'] = False

    # 画图中节点的位置。不好用。
    pos = nx.spring_layout(G)
    # pos = nx.shell_layout(G)
    # pos = nx.circular_layout(G)

    nx.draw(G,pos,node_size=10)
    nx.draw_networkx_labels(G, pos, font_size=10)

    plt.show()
