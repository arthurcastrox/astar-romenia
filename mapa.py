    # _*_ coding: utf-8 _*_
# mapa.py - os DADOS do problema (FASE 1)
#
# Mapa rodoviário da Romênia e a natureza
# h(n) = distancia em linha reta até Bucareste
# Este arquivo só guarda dados: ele não imprime nada quando é executado
# Os outros arqivos do projeto fazem "from mapa import..." para usá-los.

# _ _ _ _ _ PASSO 1: O Mapa como um dicionário _ _ _ _ _ 
# Chave  = nome da cidade(texto 
# valor  = lista de tuplas (cidade vizinha, distância em km)
mapa_romenia = {
    'Arad': [('Zerind', 75), ('Sibiu', 140), ('Timisoara', 118)],
    'Zerind': [('Arad', 75), ('Oradea', 71)],
    'Oradea': [('Zerind', 71), ('Sibiu', 151)],
    'Sibiu': [('Arad', 140), ('Oradea', 151), ('Fagaras', 99), ('Rimnicu Vilcea', 80)],

    'Timisoara': [('Arad', 118), ('Lugo', 111)],
    'Lugo': [('Timisoara', 111), ('Mehadia', 70)],
    'Mehadia': [('Lugo', 70), ('Drobeta', 75)],
    'Drobeta': [('Mehadia', 75), ('Craiova', 120)],
    'Craiova': [('Drobeta', 120), ('Rimnicu Vilcea', 146), ('Pitesti', 138)],
    'Rimnicu Vilcea': [('Sibiu', 80), ('Craiova', 146), ('Pitesti', 97)],
    'Fagaras': [('Sibiu', 99), ('Bucareste', 211)],
    'Pitesti': [('Rimnicu Vilcea', 97), ('Craiova', 138), ('Bucareste', 101)],
    'Bucareste': [('Fagaras', 211), ('Pitesti', 101), ('Giurgiu', 90)],
    'Giurgiu': [('Bucareste', 90)],
    'Urziceni': [('Bucareste', 85), ('Hirsova', 98), ('Vaslui', 142)],
    'Hirsova': [('Urziceni', 98), ('Eforie', 86)],
    'Eforie': [('Hirsova', 86)],
    'Vaslui': [('Urziceni', 142), ('Iasi', 92)],
    'Iasi': [('Vaslui', 92), ('Neamt', 87)],
    'Neamt': [('Iasi', 87)]
    }