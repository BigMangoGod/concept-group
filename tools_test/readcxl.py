# -*- coding : utf-8-*-

from bs4 import BeautifulSoup
import networkx as nx


def cxl2graph(loc):
    """读取cxl文件（lynkage提取出来的文件），试图转化成graph，以便于进行后续处理
    返回的是nx网络G和一个字典，对应连词的id和实际内容
    Note：目前将连词和概念视为了等价的节点，未来注意更新成概念之间的直接连接
    用到了BeautifulSoup包
    """
    file = open(loc, 'rb')
    html = file.read()
    # 用parser解析器来解析类html文档，形成了一个文件树
    bs = BeautifulSoup(html, 'html.parser')

    # 记录概念节点的id和名称键值对，储存在字典中
    concepts = bs.find_all('concept')  # 所有概念节点条目
    concept_name = {}
    for i in concepts:
        concept_name[i.get('id')] = i.get('label')
    # 记录连词的id和名称键值对
    link_phrases = bs.find_all('linking-phrase')
    lp_name = {}
    for i in link_phrases:
        lp_name[i.get('id')] = i.get('label')
    # 合并字典，前提是概念和连词id没有重复的
    name_dict = dict(lp_name, **concept_name)
    # print(name_dict)

    # 构建网络
    connection_list = bs.find_all('connection')
    # print(connection_list)
    edges = []
    for i in connection_list:
        edges.append((i.get('from-id'), i.get('to-id')))

    # 存入nx网络
    G = nx.DiGraph()
    G.add_edges_from(edges)
    print('G读取完成\n')

    return G, name_dict


def ranking(nodes_c, rev=True):
    """根据节点中心性输出从大到小的排列
    输入为{节点：重要性}的字典，
    输出为两个列表，分别为按重要性排列后的节点和数值，仅为了看结果用
    """
    dic2asc = sorted(nodes_c, key=nodes_c.__getitem__, reverse=rev)
    nodes_c_value = []
    for k in dic2asc:
        nodes_c_value.append(nodes_c[k])
    return dic2asc, nodes_c_value


def get_name(list, dict):
    """把概念id列表转化为名字列表，方便看是哪个概念
    dict是节点ID和具体名字的字典
    """
    name = []
    for i in list:
        name.append(dict[i])
    return name


def cxl2graph_withloc(loc):
    """读取cxl文件，试图转化成graph，以便于进行后续处理
    不同之处是连边都标上了前后节点的名字，方便定位
    """
    file = open(loc, 'rb')
    html = file.read()
    # 用parser解析器来解析类html文档，形成了一个文件树
    bs = BeautifulSoup(html, 'html.parser')

    # 记录概念节点的id和名称键值对，储存在字典中
    concepts = bs.find_all('concept')  # 所有概念节点条目
    concept_name = {}
    concept_list = []
    for i in concepts:
        concept_name[i.get('id')] = i.get('label')
        concept_list.append(i.get('id'))
    # 记录连词的id和名称键值对
    link_phrases = bs.find_all('linking-phrase')
    lp_name = {}
    link_list = []
    for i in link_phrases:
        lp_name[i.get('id')] = i.get('label')
        link_list.append(i.get('id'))

    # 合并字典，前提是概念和连词id没有重复的
    name_dict = dict(lp_name, **concept_name)
    name = name_dict

    # 构建网络
    connection_list = bs.find_all('connection')
    # print(connection_list)
    edges = []
    for i in connection_list:
        edges.append((i.get('from-id'), i.get('to-id')))

    # 存连词数据
    for item in link_list:
        for i in connection_list:
            if i.get('from-id') == item:
                forward = i.get('to-id')
                break
        for i in connection_list:
            if i.get('to-id') == item:
                backward = i.get('from-id')
                break
        name_dict[item] = name[item] + ' (定位：' + name[backward] \
                          + '→' + name[item] + '→' + name[forward] + ')'

    # print(name_dict)

    # 存入nx网络
    G = nx.DiGraph()
    G.add_edges_from(edges)
    print('G读取完成，忽略了孤立概念\n')

    return G, name_dict


if __name__ == "__main__":
    G, name_dict = cxl2graph_withloc("test_graph.cxl")
    """度中心性"""
    print('测试')
    c_degree = nx.degree_centrality(G)
    centrality_degree, centrality_degree_value = ranking(c_degree)
    centrality_degree = get_name(centrality_degree, name_dict)
    print('度中心性排序：', centrality_degree)
