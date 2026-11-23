# 1. Documento de Requisitos

**Projeto:** A\* na Romênia
**Versão:** 1.0
**Autor:** [@arthurcastrox](https://github.com/arthurcastrox)

## 1.1 Visão geral

O sistema implementa o algoritmo de busca informada **A\*** (A-estrela) em Python puro e o aplica ao clássico problema do mapa rodoviário da Romênia: encontrar o caminho de **menor custo** entre uma cidade de origem e **Bucareste**.

O projeto tem finalidade **didática**. Por isso, além do programa final, o código é entregue em fases incrementais que mostram como o algoritmo é construído.

## 1.2 Problema

Dado um grafo de cidades ligadas por estradas com distância em km, e uma estimativa de distância em linha reta de cada cidade até Bucareste, encontrar o caminho de custo mínimo sem explorar o mapa inteiro.

| Elemento | Definição |
|----------|-----------|
| Estado inicial | Cidade de origem escolhida (padrão: Arad) |
| Estado objetivo | Bucareste |
| Ações | Seguir uma estrada para uma cidade vizinha |
| Custo da ação | Distância da estrada, em km |
| Função de avaliação | `f(n) = g(n) + h(n)` |
| Heurística `h(n)` | Distância em linha reta de `n` até Bucareste |

## 1.3 Partes interessadas

| Parte | Interesse |
|-------|-----------|
| Estudante (autor) | Aprender e demonstrar o funcionamento do A\* |
| Professor / avaliador | Verificar a implementação, a modelagem e os artefatos de engenharia de software |
| Outros estudantes | Ler as fases em ordem para entender o algoritmo |

## 1.4 Escopo

**Dentro do escopo**

- Representação do mapa e da heurística.
- Busca A\* com rastro passo a passo.
- Execução a partir de qualquer cidade do mapa.
- Reuso da busca com outros grafos e heurísticas.
- Testes automatizados e documentação.

**Fora do escopo**

- Interface gráfica ou web.
- Leitura de mapas de arquivos externos ou de APIs.
- Outros algoritmos de busca (Dijkstra, busca gulosa, etc.), exceto o Dijkstra usado apenas como referência nos testes.
- Heurísticas para outros destinos além de Bucareste.

## 1.5 Requisitos funcionais

| ID | Requisito | Prioridade |
|----|-----------|------------|
| **RF01** | O sistema deve representar o mapa rodoviário da Romênia: 20 cidades e 23 estradas bidirecionais, com distância em km. | Alta |
| **RF02** | O sistema deve representar a heurística `h(n)`: distância em linha reta de cada cidade até Bucareste. | Alta |
| **RF03** | O sistema deve calcular `g(n)`, `h(n)` e `f(n) = g(n) + h(n)` para cada nó gerado. | Alta |
| **RF04** | O sistema deve receber uma cidade de origem e uma de destino e devolver o caminho de menor custo e o custo total em km. | Alta |
| **RF05** | O sistema deve poder exibir o rastro da busca: a cada iteração, a cidade expandida, seus `g`, `h`, `f` e a fronteira ordenada. | Média |
| **RF06** | Quando não existir caminho, o sistema deve devolver `(None, infinito)` sem lançar erro. | Média |
| **RF07** | A função de busca deve receber o grafo e a heurística como parâmetros, para ser reaproveitada com outros dados. | Média |
| **RF08** | O programa principal deve conferir o resultado de Arad a Bucareste com o valor de referência do livro (418 km em 4 passos). | Baixa |

## 1.6 Requisitos não funcionais

| ID | Requisito | Categoria |
|----|-----------|-----------|
| **RNF01** | Usar apenas Python 3.6+ e a biblioteca padrão, sem dependências externas. | Portabilidade |
| **RNF02** | O caminho devolvido deve ser ótimo: a heurística deve ser admissível e consistente. | Corretude |
| **RNF03** | O código deve ser didático: dividido em fases, com comentários em português. | Manutenibilidade |
| **RNF04** | O projeto deve rodar em Linux, Windows e macOS. | Portabilidade |
| **RNF05** | A documentação deve estar em português e versionada junto ao código. | Documentação |
| **RNF06** | A busca para o mapa da Romênia deve terminar em menos de 1 segundo. | Desempenho |

## 1.7 Regras de negócio

| ID | Regra |
|----|-------|
| **RN01** | As estradas são bidirecionais e têm a mesma distância nos dois sentidos. |
| **RN02** | A distância de cada estrada é positiva. |
| **RN03** | `h(Bucareste) = 0` e a heurística nunca superestima o custo real. |
| **RN04** | O teste de objetivo é feito ao **retirar** o nó da fronteira, e não ao gerá-lo; é isso que garante a otimalidade. |
| **RN05** | Uma cidade já expandida não é expandida de novo. |

## 1.8 Premissas e restrições

- O mapa e a heurística são os do exemplo clássico de Russell & Norvig, *Inteligência Artificial*.
- A fronteira é uma lista reordenada a cada iteração. Isso é suficiente para 20 cidades; para grafos grandes seria preciso uma fila de prioridade (`heapq`).
- Os scripts devem ser executados de dentro da pasta do projeto, por causa do `from mapa import ...`.

## 1.9 Critérios de aceitação

O sistema é considerado aceito quando:

1. `python a_estrela.py` imprime o caminho `Arad -> Sibiu -> Rimnicu Vilcea -> Pitesti -> Bucareste` com 418 km e a mensagem de conferência.
2. `python -m unittest discover -s tests` termina com todos os testes passando.
3. Para todas as origens do mapa, o custo do A\* é igual ao custo ótimo calculado por Dijkstra.
