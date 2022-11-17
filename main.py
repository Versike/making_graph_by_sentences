from natasha import NewsEmbedding, Segmenter, NewsSyntaxParser, Doc
import pymorphy2
import networkx as nx
import matplotlib.pyplot as plt

emb = NewsEmbedding()
segmenter = Segmenter()
syntax_parser = NewsSyntaxParser(emb)
morph = pymorphy2.MorphAnalyzer()

text = ['Сема пошел за хлебом', 'Дамир сдает лабу', 'Ромазанов проверяет лабу',
        'Илья выбросил хлеб', 'Ромазанов работает в университете', 'Илья едет в университет', 'Данил пьет протеин', 'Хлеб содержит протеин']
subj_list = []
obj_list = []
verb_list = []
for sent in text:
    doc = Doc(sent)
    doc.segment(segmenter)
    doc.parse_syntax(syntax_parser)
    for tocken in doc.tokens:
        if tocken.rel == 'obj' or tocken.rel == 'obl':
            word = morph.parse(tocken.text)[0]
            obj_list.append(word.normal_form)
        elif tocken.rel == 'nsubj':
            word = morph.parse(tocken.text)[0]
            subj_list.append(word.normal_form)
        elif tocken.rel == 'root':
            word = morph.parse(tocken.text)[0]
            verb_list.append(word.normal_form)

edges = []
_temp_list = []
_2temp_list = []
for i in range(len(text)):
    if i%2 == 0:
        _temp_list.append(subj_list[i])
        _temp_list.append(obj_list[i])
        edges.append(_temp_list)
        _temp_list = []
    else:
        _2temp_list.append(subj_list[i])
        _2temp_list.append(obj_list[i])
        edges.append(_2temp_list)
        _2temp_list = []

print(edges)

G = nx.DiGraph()
G.add_edges_from(edges)
pos = nx.spring_layout(G, k=2, iterations=20)
plt.figure()
nx.draw(
    G, pos, edge_color='black', width=1, linewidths=1,
    node_size=500, node_color='gray', alpha=0.9,
    labels={node: node for node in G.nodes()}
)
nx.draw_networkx_edge_labels(
    G, pos,
    edge_labels={(subj_list[i], obj_list[i]): verb_list[i] for i in range(len(text))},
    font_color='black'
)
plt.axis('off')
plt.show()

#Проще говоря, что нужно сделать.
    #1) Составить набор предложений из входного текста. [Просто переменная в которой хранится набор странных предложений] ++
    #2) (не разобрался, но на готовых изи делается) Разработать микро-алогритм для определения синтаксиса слова. ++
        #2.1) Подготовить технологии.++
        #2.2) Сделать цикл для прогонки списка предложений и разбиение на синтаксиса.++
        #2.3) доп пункт на лемматизация
        #2.4) Вытащить только subject object root++
        #2.5) пункт еще обновляется...
    #3) Вывести список предложений на граф.
        #3.1) Определиться с технологией++
        #3.2) Создать алгоритм для внедрения списка синтаксиса
            #subj, obj - node, root - edge
