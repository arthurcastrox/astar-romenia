# astar-romeniaimplemetação do algoritmo A*
# A* na Romênia

Implementação didática do algoritmo de busca **A\*** (A-estrela) em Python puro, aplicada ao clássico problema do mapa rodoviário da Romênia: encontrar o menor caminho entre uma cidade de origem e **Bucareste**.

O projeto foi construído em **fases**, cada uma em um arquivo próprio, indo dos dados brutos até o algoritmo completo. Dá para rodar e ler cada fase na ordem para entender como o A\* funciona por dentro.

## Como o A* funciona

Para cada cidade `n`, o algoritmo calcula:

```
f(n) = g(n) + h(n)
```

| Termo | Significado |
|-------|-------------|
| `g(n)` | custo real, em km, já percorrido da origem até `n` |
| `h(n)` | heurística: distância em linha reta, em km, de `n` até Bucareste |
| `f(n)` | estimativa do custo total de um caminho que passa por `n` |

A cada passo, o A\* expande a cidade com **menor `f`** na fronteira. Como a heurística nunca superestima a distância real, o primeiro caminho que chega ao objetivo é o de menor custo.

## Estrutura do projeto

| Arquivo | Fase | O que faz |
|---------|------|-----------|
| `mapa.py` | 1 | Dados do problema: o mapa (`mapa_romenia`) e a heurística (`heuristica_bucareste`). Não imprime nada. |
| `fase1 explorar.py` | 1 | Navega pelos dados: dicionários, listas, tuplas, laços `for` e consulta à heurística. Ainda sem busca. |
| `fase2_caminhos.py` | 2 | Funções `custo_da_estrada` e `custo_do_caminho`; mostra `g`, `h` e `f` ao longo de dois caminhos (por Fagaras e por Pitesti). |
| `fase3_fronteira.py` | 3 | Monta o nó de busca `(f, g, cidade, caminho)` e a fronteira à mão; expande Arad e ordena por `f`. |
| `fase4_expandir.py` | 4 | Transforma a expansão em função (`expandir`) e repete três rodadas manualmente, mostrando fronteira e explorados. |
| `fase5_busca.py` | 5 | Junta tudo em um laço `while` e devolve o caminho de Arad a Bucareste. |
| `a_estrela.py` | 6 | **Programa completo**: busca A\* parametrizada, com rastro passo a passo, verificação do resultado e testes com outras origens. |

## Representação dos dados

- **Mapa:** dicionário em que a chave é a cidade e o valor é uma lista de tuplas `(cidade_vizinha, distancia_km)`.
- **Heurística:** dicionário `cidade -> distância em linha reta até Bucareste`.
- **Nó da busca:** tupla `(f, g, cidade, caminho)`. O `f` fica na posição 0 porque é por ele que a fronteira é ordenada.
- **Fronteira:** lista ordenada por `f`. **Explorados:** conjunto (`set`) de cidades já expandidas.

O mapa tem 20 cidades e 22 estradas.

## Requisitos

- Python 3.6 ou superior (usa f-strings)
- Nenhuma dependência externa: apenas a biblioteca padrão

## Como executar

```bash
git clone https://github.com/arthurcastrox/astar-romenia.git
cd astar-romenia

# programa completo
python a_estrela.py

# fases didáticas (opcional, em ordem)
python "fase1 explorar.py"
python fase2_caminhos.py
python fase3_fronteira.py
python fase4_expandir.py
python fase5_busca.py
```

> Execute os scripts de dentro da pasta do projeto, para que o `from mapa import ...` funcione.

## Exemplo de saída

Rodando `python a_estrela.py`:

```
--- Busca A* de Arad para Bucareste ---
1. expandindo: Arad | g(n)=0, h(n)=366 -> f(n)=366
   fronteira: Sibiu(393), Timisoara(447), Zerind(449)
2. expandindo: Sibiu | g(n)=140, h(n)=253 -> f(n)=393
   fronteira: Rimnicu Vilcea(413), Fagaras(415), Timisoara(447), Zerind(449), Oradea(671)
3. expandindo: Rimnicu Vilcea | g(n)=220, h(n)=193 -> f(n)=413
   fronteira: Fagaras(415), Pitesti(417), Timisoara(447), Zerind(449), Craiova(526), Oradea(671)
4. expandindo: Fagaras | g(n)=239, h(n)=176 -> f(n)=415
   fronteira: Pitesti(417), Timisoara(447), Zerind(449), Bucareste(450), Craiova(526), Oradea(671)
5. expandindo: Pitesti | g(n)=317, h(n)=100 -> f(n)=417
   fronteira: Bucareste(418), Timisoara(447), Zerind(449), Bucareste(450), Craiova(526), Craiova(615), Oradea(671)
6. expandindo: Bucareste | g(n)=418, h(n)=0 -> f(n)=418

--- Resultado ---
Caminho encontrado: Arad -> Sibiu -> Rimnicu Vilcea -> Pitesti -> Bucareste
Custo real total: 418 km em 4 passos
Conferido: igual ao livro (418 km, 4 passos).
```

O programa também calcula o melhor caminho a partir de outras origens:

| Origem | Custo | Caminho |
|--------|-------|---------|
| Timisoara | 536 km | Timisoara → Arad → Sibiu → Rimnicu Vilcea → Pitesti → Bucareste |
| Oradea | 429 km | Oradea → Sibiu → Rimnicu Vilcea → Pitesti → Bucareste |
| Craiova | 239 km | Craiova → Pitesti → Bucareste |
| Iasi | 319 km | Iasi → Vaslui → Urziceni → Bucareste |

## Uso como função

A função `busca_a_estrela` recebe o grafo e a heurística, então pode ser reaproveitada com outros dados:

```python
from mapa import mapa_romenia, heuristica_bucareste
from a_estrela import busca_a_estrela

caminho, custo = busca_a_estrela(
    'Craiova', 'Bucareste',
    mapa_romenia, heuristica_bucareste,
    mostrar=False,   # True imprime o rastro de cada iteração
)
print(caminho, custo)
# ['Craiova', 'Pitesti', 'Bucareste'] 239
```

Se não houver caminho, a função devolve `(None, inf)`.

## Detalhes de implementação

- O teste de objetivo é feito ao **retirar** o nó da fronteira, e não ao gerá-lo. É isso que garante a otimalidade.
- Nós repetidos que chegam à fronteira por um caminho pior são descartados quando já existe uma versão explorada da mesma cidade.
- A fronteira é uma lista reordenada a cada iteração. É simples e bom para aprender; para grafos grandes, o ideal seria uma fila de prioridade (`heapq`).
- `a_estrela.py` inclui um teste de regressão simples: o resultado de Arad a Bucareste deve ser 418 km em 4 passos.

## Autor

[@arthurcastrox](https://github.com/arthurcastrox)