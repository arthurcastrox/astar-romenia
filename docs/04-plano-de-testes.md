# 4. Plano de Testes e Rastreabilidade

## 4.1 Estratégia

| Item | Definição |
|------|-----------|
| Ferramenta | `unittest` (biblioteca padrão; sem dependências, conforme RNF01) |
| Arquivo | [`tests/test_a_estrela.py`](../tests/test_a_estrela.py) |
| Execução | `python -m unittest discover -s tests -v` |
| Nível | Unidade (dados e função de busca) e sistema (execução dos scripts) |
| Critério de aprovação | 20 de 20 testes passando |

**Oráculo de testes.** Para provar que o A\* é ótimo, os testes comparam o resultado com um **Dijkstra independente**, escrito dentro do próprio arquivo de testes. Se o A\* e o Dijkstra concordam em todas as origens, o resultado é confiável sem depender do valor do livro.

## 4.2 Casos de teste

| ID | Classe | Descrição | Resultado esperado | Requisito |
|----|--------|-----------|--------------------|-----------|
| TC-01 | `TestDadosDoMapa` | Contar cidades e estradas | 20 cidades, 23 estradas | RF01 |
| TC-02 | `TestDadosDoMapa` | Verificar simetria do mapa | Toda estrada existe nos dois sentidos, com o mesmo km | RF01, RN01 |
| TC-03 | `TestDadosDoMapa` | Verificar distâncias | Todas maiores que zero | RF01, RN02 |
| TC-04 | `TestDadosDoMapa` | Cobertura da heurística | `h` definido exatamente para as cidades do mapa | RF02 |
| TC-05 | `TestDadosDoMapa` | Valores da heurística | `h(Bucareste) = 0`; demais positivos | RF02, RN03 |
| TC-06 | `TestBuscaAEstrela` | Arad → Bucareste | `Arad, Sibiu, Rimnicu Vilcea, Pitesti, Bucareste`; 418 km; 4 passos | RF04, RF08 |
| TC-07 | `TestBuscaAEstrela` | Outras origens | Timisoara 536, Oradea 429, Craiova 239, Iasi 319 km | RF04 |
| TC-08 | `TestBuscaAEstrela` | Origem igual ao objetivo | `['Bucareste']`, custo 0 | RF04 |
| TC-09 | `TestBuscaAEstrela` | Todas as cidades alcançam Bucareste | Caminho existe e termina em Bucareste (inclui Giurgiu) | RF04 |
| TC-10 | `TestBuscaAEstrela` | Custo confere com o caminho | Custo devolvido = soma das estradas do caminho | RF03, RF04 |
| TC-11 | `TestBuscaAEstrela` | Grafo desconexo | `(None, inf)`, sem exceção | RF06 |
| TC-12 | `TestBuscaAEstrela` | Reuso com outro grafo | Caminho `S, A, B, G`, custo 6 | RF07 |
| TC-13 | `TestOtimalidade` | A\* contra Dijkstra | Mesmo custo para todas as 20 origens | RNF02 |
| TC-14 | `TestOtimalidade` | Admissibilidade | `h(n)` ≤ custo real até Bucareste, para toda cidade | RNF02, RN03 |
| TC-15 | `TestOtimalidade` | Consistência | `h(a)` ≤ `custo(a,b) + h(b)` para toda estrada | RNF02 |
| TC-16 | `TestSaida` | Rastro ligado | Imprime as 6 iterações e a fronteira | RF05 |
| TC-17 | `TestSaida` | Rastro desligado | Nenhuma saída | RF05 |
| TC-18 | `TestScripts` | Execução dos scripts | Os 6 scripts terminam com código 0 | RNF01, RNF03 |
| TC-19 | `TestScripts` | Conferência com o livro | Saída contém "Conferido: igual ao livro" | RF08 |
| TC-20 | `TestDesempenho` | Tempo de resposta | 20 buscas em menos de 1 s | RNF06 |

## 4.3 Matriz de rastreabilidade

| Requisito | Casos de teste |
|-----------|----------------|
| RF01 | TC-01, TC-02, TC-03 |
| RF02 | TC-04, TC-05 |
| RF03 | TC-10 |
| RF04 | TC-06, TC-07, TC-08, TC-09, TC-10 |
| RF05 | TC-16, TC-17 |
| RF06 | TC-11 |
| RF07 | TC-12 |
| RF08 | TC-06, TC-19 |
| RNF01 | TC-18 |
| RNF02 | TC-13, TC-14, TC-15 |
| RNF03 | TC-18 |
| RNF04 | Não automatizado: execução manual em Linux, Windows e macOS |
| RNF05 | Não automatizado: revisão dos documentos em `docs/` |
| RNF06 | TC-20 |

## 4.4 Defeitos encontrados durante os testes

Ao escrever a suíte, os testes de integridade dos dados (TC-02, TC-04, TC-09) revelaram dois defeitos no `mapa.py`, ambos já corrigidos:

| ID | Defeito | Efeito | Correção |
|----|---------|--------|----------|
| DEF-01 | Na heurística, a chave estava escrita `'Girgiu'`; no mapa, `'Giurgiu'`. | `KeyError` ao buscar a partir de Giurgiu, pois a cidade ficava sem `h(n)`. | Chave corrigida para `'Giurgiu'`. |
| DEF-02 | A estrada Bucareste–Urziceni (85 km) existia só no sentido Urziceni → Bucareste. | Mapa assimétrico, contra RN01: partindo de Bucareste, a estrada para Urziceni não existia. | Adicionado `('Urziceni', 85)` à lista de Bucareste. |

Nenhum dos dois alterava o resultado de Arad a Bucareste (418 km), por isso passaram despercebidos até a suíte de testes cobrir todas as origens.

## 4.5 Resultado da última execução

```
Ran 20 tests

OK
```
