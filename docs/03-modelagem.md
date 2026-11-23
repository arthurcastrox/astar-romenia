# 3. Modelagem e Diagramas

Os diagramas estão em [Mermaid](https://mermaid.js.org/), que o GitHub renderiza direto neste arquivo. Versões em imagem estão em [`img/`](img/).

| # | Diagrama | Responde a |
|---|----------|------------|
| 3.1 | Grafo do problema | Qual é o mapa e qual é o caminho ótimo? |
| 3.2 | Componentes (módulos) | Quais arquivos existem e quem depende de quem? |
| 3.3 | Classes (modelo conceitual) | Quais conceitos o domínio tem e como se relacionam? |
| 3.4 | Sequência | Como as partes conversam durante uma busca? |
| 3.5 | Atividades (fluxograma do A\*) | Qual é a lógica passo a passo do algoritmo? |
| 3.6 | Árvore de busca | O que o A\* fez de fato de Arad a Bucareste? |

## 3.1 Grafo do problema

Cada cidade mostra o valor de `h(n)` (km em linha reta até Bucareste). Cada aresta mostra a distância da estrada em km. O caminho ótimo de Arad a Bucareste está em vermelho.

```mermaid
flowchart TB
    Arad["Arad<br/>h=366"]
    Zerind["Zerind<br/>h=374"]
    Oradea["Oradea<br/>h=380"]
    Sibiu["Sibiu<br/>h=253"]
    Timisoara["Timisoara<br/>h=329"]
    Lugo["Lugo<br/>h=244"]
    Mehadia["Mehadia<br/>h=241"]
    Drobeta["Drobeta<br/>h=242"]
    Craiova["Craiova<br/>h=160"]
    RV["Rimnicu Vilcea<br/>h=193"]
    Fagaras["Fagaras<br/>h=176"]
    Pitesti["Pitesti<br/>h=100"]
    Bucareste["Bucareste<br/>h=0"]
    Giurgiu["Giurgiu<br/>h=77"]
    Urziceni["Urziceni<br/>h=80"]
    Hirsova["Hirsova<br/>h=151"]
    Eforie["Eforie<br/>h=161"]
    Vaslui["Vaslui<br/>h=199"]
    Iasi["Iasi<br/>h=226"]
    Neamt["Neamt<br/>h=234"]

    Arad ---|75| Zerind
    Arad ---|140| Sibiu
    Arad ---|118| Timisoara
    Zerind ---|71| Oradea
    Oradea ---|151| Sibiu
    Sibiu ---|99| Fagaras
    Sibiu ---|80| RV
    Timisoara ---|111| Lugo
    Lugo ---|70| Mehadia
    Mehadia ---|75| Drobeta
    Drobeta ---|120| Craiova
    Craiova ---|146| RV
    Craiova ---|138| Pitesti
    RV ---|97| Pitesti
    Fagaras ---|211| Bucareste
    Pitesti ---|101| Bucareste
    Bucareste ---|90| Giurgiu
    Bucareste ---|85| Urziceni
    Urziceni ---|98| Hirsova
    Urziceni ---|142| Vaslui
    Hirsova ---|86| Eforie
    Vaslui ---|92| Iasi
    Iasi ---|87| Neamt

    classDef origem fill:#fde68a,stroke:#b45309,color:#111
    classDef objetivo fill:#bbf7d0,stroke:#15803d,color:#111
    classDef caminho fill:#fecaca,stroke:#b91c1c,color:#111
    class Arad origem
    class Bucareste objetivo
    class Sibiu,RV,Pitesti caminho
    linkStyle 1,6,13,15 stroke:#dc2626,stroke-width:4px
```

## 3.2 Diagrama de componentes

```mermaid
flowchart TB
    subgraph dados["Dados"]
        mapa["<b>mapa.py</b><br/>mapa_romenia<br/>heuristica_bucareste"]
    end

    subgraph nucleo["Núcleo"]
        astar["<b>a_estrela.py</b><br/>busca_a_estrela()<br/>resumo_fronteira()<br/>main()"]
    end

    subgraph fases["Fases didáticas"]
        f1["fase1 explorar.py"]
        f2["fase2_caminhos.py"]
        f3["fase3_fronteira.py"]
        f4["fase4_expandir.py"]
        f5["fase5_busca.py"]
    end

    subgraph testes["Qualidade"]
        t["<b>tests/test_a_estrela.py</b><br/>unittest"]
    end

    astar -->|"import"| mapa
    f1 -->|"import"| mapa
    f2 -->|"import"| mapa
    f3 -->|"import"| mapa
    f4 -->|"import"| mapa
    f5 -->|"import"| mapa
    t -->|"import"| astar
    t -->|"import"| mapa
    t -.->|"executa como processo"| fases
```

O módulo `mapa.py` só guarda dados e não imprime nada. Por isso os testes e todas as fases podem importá-lo sem efeito colateral.

## 3.3 Diagrama de classes (modelo conceitual)

O código é escrito de forma funcional, com dicionários, tuplas, listas e conjuntos, o que combina com o objetivo didático. O diagrama abaixo é o **modelo conceitual** do domínio: ele mostra os conceitos e a tabela logo depois diz como cada um aparece no código.

```mermaid
classDiagram
    class Mapa {
        +cidades : dict
        +vizinhos(cidade) list
    }
    class Estrada {
        +destino : str
        +distancia_km : int
    }
    class Heuristica {
        +valores : dict
        +h(cidade) int
    }
    class NoDeBusca {
        +f : int
        +g : int
        +cidade : str
        +caminho : list
    }
    class Fronteira {
        +nos : list
        +adicionar(no)
        +ordenar_por_f()
        +retirar_menor_f() NoDeBusca
        +esta_vazia() bool
    }
    class BuscaAEstrela {
        +explorados : set
        +executar(inicio, objetivo, mostrar) tuple
    }

    Mapa "1" o-- "*" Estrada : cada cidade tem
    BuscaAEstrela ..> Mapa : consulta vizinhos
    BuscaAEstrela ..> Heuristica : consulta h(n)
    BuscaAEstrela "1" *-- "1" Fronteira : mantém
    Fronteira "1" o-- "*" NoDeBusca : ordena por f
```

| Conceito | Representação no código |
|----------|-------------------------|
| `Mapa` | `mapa_romenia`: `dict` de `cidade -> [(vizinho, km), ...]` |
| `Estrada` | Tupla `(cidade_vizinha, distancia_km)` |
| `Heuristica` | `heuristica_bucareste`: `dict` de `cidade -> km em linha reta` |
| `NoDeBusca` | Tupla `(f, g, cidade, caminho)`, com `f` na posição 0 para ordenar |
| `Fronteira` | `list` de nós, reordenada por `f` a cada iteração |
| `explorados` | `set` de cidades já expandidas |
| `BuscaAEstrela` | Função `busca_a_estrela(inicio, objetivo, grafo, heuristica, mostrar)` |

## 3.4 Diagrama de sequência

Fluxo de `python a_estrela.py`, de Arad a Bucareste.

```mermaid
sequenceDiagram
    actor U as Usuário
    participant M as main()
    participant B as busca_a_estrela()
    participant F as fronteira (list)
    participant G as grafo (mapa_romenia)
    participant H as heuristica_bucareste

    U->>M: python a_estrela.py
    M->>B: busca_a_estrela('Arad', 'Bucareste', grafo, h)
    B->>H: h['Arad']
    H-->>B: 366
    B->>F: cria [(366, 0, 'Arad', ['Arad'])]

    loop enquanto a fronteira não estiver vazia
        B->>F: sort por f e pop(0)
        F-->>B: nó de menor f
        alt cidade já explorada
            B->>B: descarta o nó
        else cidade é o objetivo
            B-->>M: (caminho, g)
        else expandir
            B->>B: explorados.add(cidade)
            B->>G: grafo.get(cidade)
            G-->>B: [(vizinho, km), ...]
            loop cada vizinho não explorado
                B->>H: h[vizinho]
                H-->>B: h
                B->>F: append((f, g, vizinho, caminho + [vizinho]))
            end
        end
    end

    M-->>U: caminho, custo e conferência com o livro
```

## 3.5 Diagrama de atividades (fluxograma do A\*)

```mermaid
flowchart TD
    A(["Início"]) --> B["Criar fronteira com o nó da origem<br/>f = h(origem), g = 0<br/>explorados = vazio"]
    B --> C{"Fronteira<br/>vazia?"}
    C -- sim --> X(["Devolver None, infinito<br/>(sem caminho)"])
    C -- não --> D["Ordenar a fronteira por f<br/>e retirar o nó de menor f"]
    D --> E{"Cidade já<br/>explorada?"}
    E -- sim --> C
    E -- não --> F["Imprimir iteração<br/>g, h e f (se mostrar=True)"]
    F --> G{"Cidade é<br/>o objetivo?"}
    G -- sim --> Y(["Devolver caminho e g<br/>(custo ótimo)"])
    G -- não --> H["Marcar cidade como explorada"]
    H --> I["Para cada vizinho não explorado:<br/>novo_g = g + km da estrada<br/>novo_f = novo_g + h(vizinho)<br/>adicionar nó à fronteira"]
    I --> J["Imprimir fronteira ordenada<br/>(se mostrar=True)"]
    J --> C
```

## 3.6 Árvore de busca (Arad → Bucareste)

O número antes do nome é a ordem de expansão. Nós em cinza foram gerados mas nunca expandidos, porque o A\* achou Bucareste com `f = 418` antes de precisar deles. Craiova e Bucareste aparecem duas vezes, por caminhos diferentes. Arad não volta a ser gerada a partir de Sibiu, porque já está em `explorados`.

```mermaid
flowchart TD
    N1["<b>1º Arad</b><br/>g=0 · h=366 · f=366"]
    N2["<b>2º Sibiu</b><br/>g=140 · h=253 · f=393"]
    Nt["Timisoara<br/>g=118 · h=329 · f=447"]
    Nz["Zerind<br/>g=75 · h=374 · f=449"]
    N3["<b>3º Rimnicu Vilcea</b><br/>g=220 · h=193 · f=413"]
    N4["<b>4º Fagaras</b><br/>g=239 · h=176 · f=415"]
    No["Oradea<br/>g=291 · h=380 · f=671"]
    N5["<b>5º Pitesti</b><br/>g=317 · h=100 · f=417"]
    Nc1["Craiova<br/>g=366 · h=160 · f=526"]
    Nb1["Bucareste via Fagaras<br/>g=450 · h=0 · f=450"]
    N6["<b>6º Bucareste</b><br/>g=418 · h=0 · f=418<br/>OBJETIVO"]
    Nc2["Craiova<br/>g=455 · h=160 · f=615"]

    N1 -->|"140"| N2
    N1 -->|"118"| Nt
    N1 -->|"75"| Nz
    N2 -->|"80"| N3
    N2 -->|"99"| N4
    N2 -->|"151"| No
    N3 -->|"97"| N5
    N3 -->|"146"| Nc1
    N4 -->|"211"| Nb1
    N5 -->|"101"| N6
    N5 -->|"138"| Nc2

    classDef expandido fill:#dbeafe,stroke:#1d4ed8,color:#111
    classDef objetivo fill:#bbf7d0,stroke:#15803d,color:#111
    classDef naoExpandido fill:#e5e7eb,stroke:#6b7280,color:#374151
    class N1,N2,N3,N4,N5 expandido
    class N6 objetivo
    class Nt,Nz,No,Nc1,Nb1,Nc2 naoExpandido
```

Note o nó "Bucareste via Fagaras" (`f = 450`): ele foi gerado na 4ª iteração, mas só seria retirado da fronteira depois do nó `f = 418`. É por isso que o teste de objetivo é feito ao **retirar** o nó, e não ao gerá-lo (RN04).
