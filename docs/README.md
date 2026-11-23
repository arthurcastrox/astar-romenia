# Documentação de Engenharia de Software

Artefatos do projeto **A\* na Romênia**.

| Documento | Conteúdo |
|-----------|----------|
| [01-requisitos.md](01-requisitos.md) | Visão, escopo, partes interessadas, requisitos funcionais (RF) e não funcionais (RNF), regras de negócio, critérios de aceitação |
| [02-casos-de-uso.md](02-casos-de-uso.md) | Atores, diagrama de casos de uso e especificação de UC01 a UC07 |
| [03-modelagem.md](03-modelagem.md) | Grafo do problema, componentes, classes, sequência, atividades e árvore de busca |
| [04-plano-de-testes.md](04-plano-de-testes.md) | Estratégia, 20 casos de teste, matriz de rastreabilidade, defeitos encontrados |

## Diagramas

Os diagramas estão em Mermaid dentro dos `.md` e o GitHub os renderiza automaticamente. Também há versões em imagem em [`img/`](img/):

| Imagem | Diagrama |
|--------|----------|
| [2-2-diagrama-de-casos-de-uso.png](img/2-2-diagrama-de-casos-de-uso.png) | Casos de uso |
| [3-1-grafo-do-problema.png](img/3-1-grafo-do-problema.png) | Mapa da Romênia com `h(n)` e caminho ótimo |
| [3-2-diagrama-de-componentes.png](img/3-2-diagrama-de-componentes.png) | Componentes (módulos) |
| [3-3-diagrama-de-classes-modelo-conceitual.png](img/3-3-diagrama-de-classes-modelo-conceitual.png) | Classes (modelo conceitual) |
| [3-4-diagrama-de-sequencia.png](img/3-4-diagrama-de-sequencia.png) | Sequência |
| [3-5-diagrama-de-atividades-fluxograma-do-a.png](img/3-5-diagrama-de-atividades-fluxograma-do-a.png) | Atividades (fluxograma do A\*) |
| [3-6-arvore-de-busca-arad-bucareste.png](img/3-6-arvore-de-busca-arad-bucareste.png) | Árvore de busca de Arad a Bucareste |

As imagens são geradas a partir dos `.md` por [`gerar_diagramas.py`](gerar_diagramas.py). Ao editar um diagrama, edite o `.md` e rode o script de novo (precisa de `mmdc` e Chrome; veja o cabeçalho do script).

## Rastreabilidade

Requisitos → casos de uso → casos de teste:

- Cada RF/RNF de [01-requisitos.md](01-requisitos.md) é citado em pelo menos um caso de uso (seção 2.3) ou teste (seção 4.3).
- Cada teste em `tests/test_a_estrela.py` cita o requisito que verifica no *docstring*.
