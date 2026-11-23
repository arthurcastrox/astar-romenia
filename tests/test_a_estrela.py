# -*- coding: utf-8 -*-
"""Testes automatizados do projeto A* na Romênia.

Rode a partir da raiz do projeto:

    python -m unittest discover -s tests -v

Cada teste cita o requisito que verifica (RFxx / RNFxx), conforme
docs/01-requisitos.md. A rastreabilidade completa está em
docs/04-plano-de-testes.md.
"""
import heapq
import io
import os
import subprocess
import sys
import time
import unittest
from contextlib import redirect_stdout

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)

from mapa import mapa_romenia, heuristica_bucareste  # noqa: E402
from a_estrela import busca_a_estrela  # noqa: E402

OBJETIVO = 'Bucareste'


def dijkstra(grafo, origem, destino):
    """Referência independente: menor custo real de origem até destino."""
    dist = {origem: 0}
    fila = [(0, origem)]
    while fila:
        d, cidade = heapq.heappop(fila)
        if cidade == destino:
            return d
        if d > dist.get(cidade, float('inf')):
            continue
        for vizinho, custo in grafo.get(cidade, []):
            nd = d + custo
            if nd < dist.get(vizinho, float('inf')):
                dist[vizinho] = nd
                heapq.heappush(fila, (nd, vizinho))
    return float('inf')


def custo_do_caminho(grafo, caminho):
    total = 0
    for a, b in zip(caminho, caminho[1:]):
        total += dict(grafo[a])[b]
    return total


class TestDadosDoMapa(unittest.TestCase):
    """RF01 e RF02: integridade dos dados de entrada."""

    def test_tc01_quantidade_de_cidades_e_estradas(self):
        """TC-01 (RF01): 20 cidades e 23 estradas bidirecionais."""
        estradas = {frozenset((a, b))
                    for a, vizinhos in mapa_romenia.items()
                    for b, _ in vizinhos}
        self.assertEqual(len(mapa_romenia), 20)
        self.assertEqual(len(estradas), 23)

    def test_tc02_mapa_simetrico(self):
        """TC-02 (RF01): toda estrada existe nos dois sentidos, com a mesma distância."""
        for a, vizinhos in mapa_romenia.items():
            for b, custo in vizinhos:
                self.assertIn((a, custo), mapa_romenia[b],
                              f'falta o sentido inverso de {a} -> {b}')

    def test_tc03_distancias_positivas(self):
        """TC-03 (RF01): nenhuma estrada com distância zero ou negativa."""
        for vizinhos in mapa_romenia.values():
            for _, custo in vizinhos:
                self.assertGreater(custo, 0)

    def test_tc04_heuristica_cobre_todas_as_cidades(self):
        """TC-04 (RF02): h(n) definido exatamente para as cidades do mapa."""
        self.assertEqual(set(heuristica_bucareste), set(mapa_romenia))

    def test_tc05_heuristica_do_objetivo_e_zero(self):
        """TC-05 (RF02): h(Bucareste) = 0 e os demais h(n) são positivos."""
        self.assertEqual(heuristica_bucareste[OBJETIVO], 0)
        for cidade, h in heuristica_bucareste.items():
            if cidade != OBJETIVO:
                self.assertGreater(h, 0, cidade)


class TestBuscaAEstrela(unittest.TestCase):
    """RF03, RF04, RF06, RF07: comportamento da busca."""

    def test_tc06_arad_para_bucareste(self):
        """TC-06 (RF04, RF08): resultado de referência do livro."""
        caminho, custo = busca_a_estrela('Arad', OBJETIVO, mapa_romenia,
                                         heuristica_bucareste, mostrar=False)
        self.assertEqual(caminho, ['Arad', 'Sibiu', 'Rimnicu Vilcea',
                                   'Pitesti', 'Bucareste'])
        self.assertEqual(custo, 418)
        self.assertEqual(len(caminho) - 1, 4)

    def test_tc07_outras_origens(self):
        """TC-07 (RF04): custos esperados a partir de outras origens."""
        esperado = {'Timisoara': 536, 'Oradea': 429, 'Craiova': 239, 'Iasi': 319}
        for origem, custo_esperado in esperado.items():
            with self.subTest(origem=origem):
                caminho, custo = busca_a_estrela(origem, OBJETIVO, mapa_romenia,
                                                 heuristica_bucareste, mostrar=False)
                self.assertEqual(custo, custo_esperado)
                self.assertEqual(caminho[0], origem)
                self.assertEqual(caminho[-1], OBJETIVO)

    def test_tc08_origem_igual_ao_objetivo(self):
        """TC-08 (RF04): origem = objetivo devolve caminho de uma cidade e custo 0."""
        caminho, custo = busca_a_estrela(OBJETIVO, OBJETIVO, mapa_romenia,
                                         heuristica_bucareste, mostrar=False)
        self.assertEqual(caminho, [OBJETIVO])
        self.assertEqual(custo, 0)

    def test_tc09_toda_cidade_alcanca_bucareste(self):
        """TC-09 (RF04): de qualquer cidade existe caminho (inclui Giurgiu)."""
        for origem in mapa_romenia:
            with self.subTest(origem=origem):
                caminho, custo = busca_a_estrela(origem, OBJETIVO, mapa_romenia,
                                                 heuristica_bucareste, mostrar=False)
                self.assertIsNotNone(caminho)
                self.assertEqual(caminho[0], origem)
                self.assertEqual(caminho[-1], OBJETIVO)

    def test_tc10_custo_informado_confere_com_o_caminho(self):
        """TC-10 (RF03, RF04): o custo devolvido é a soma real das estradas do caminho."""
        for origem in mapa_romenia:
            with self.subTest(origem=origem):
                caminho, custo = busca_a_estrela(origem, OBJETIVO, mapa_romenia,
                                                 heuristica_bucareste, mostrar=False)
                self.assertEqual(custo, custo_do_caminho(mapa_romenia, caminho))

    def test_tc11_sem_caminho(self):
        """TC-11 (RF06): grafo desconexo devolve (None, infinito)."""
        grafo = {'A': [('B', 1)], 'B': [('A', 1)], 'C': []}
        h = {'A': 0, 'B': 0, 'C': 0}
        caminho, custo = busca_a_estrela('A', 'C', grafo, h, mostrar=False)
        self.assertIsNone(caminho)
        self.assertEqual(custo, float('inf'))

    def test_tc12_reuso_com_outro_grafo(self):
        """TC-12 (RF07): a função funciona com grafo e heurística diferentes."""
        grafo = {
            'S': [('A', 1), ('B', 4)],
            'A': [('S', 1), ('B', 2), ('G', 6)],
            'B': [('S', 4), ('A', 2), ('G', 3)],
            'G': [('A', 6), ('B', 3)],
        }
        h = {'S': 5, 'A': 4, 'B': 3, 'G': 0}
        caminho, custo = busca_a_estrela('S', 'G', grafo, h, mostrar=False)
        self.assertEqual(caminho, ['S', 'A', 'B', 'G'])
        self.assertEqual(custo, 6)


class TestDesempenho(unittest.TestCase):
    """RNF06: tempo de resposta."""

    def test_tc20_busca_em_menos_de_um_segundo(self):
        """TC-20 (RNF06): buscas a partir de todas as cidades somam menos de 1 s."""
        inicio = time.perf_counter()
        for origem in mapa_romenia:
            busca_a_estrela(origem, OBJETIVO, mapa_romenia,
                            heuristica_bucareste, mostrar=False)
        self.assertLess(time.perf_counter() - inicio, 1.0)


class TestOtimalidade(unittest.TestCase):
    """RNF02: o A* só é ótimo se h for admissível e consistente."""

    def test_tc13_resultado_igual_ao_dijkstra(self):
        """TC-13 (RNF02): custo do A* = custo ótimo de Dijkstra para todas as origens."""
        for origem in mapa_romenia:
            with self.subTest(origem=origem):
                _, custo = busca_a_estrela(origem, OBJETIVO, mapa_romenia,
                                           heuristica_bucareste, mostrar=False)
                self.assertEqual(custo, dijkstra(mapa_romenia, origem, OBJETIVO))

    def test_tc14_heuristica_admissivel(self):
        """TC-14 (RNF02): h(n) nunca superestima o custo real até Bucareste."""
        for cidade, h in heuristica_bucareste.items():
            with self.subTest(cidade=cidade):
                self.assertLessEqual(h, dijkstra(mapa_romenia, cidade, OBJETIVO))

    def test_tc15_heuristica_consistente(self):
        """TC-15 (RNF02): h(a) <= custo(a,b) + h(b) para toda estrada."""
        for a, vizinhos in mapa_romenia.items():
            for b, custo in vizinhos:
                with self.subTest(estrada=f'{a}->{b}'):
                    self.assertLessEqual(
                        heuristica_bucareste[a],
                        custo + heuristica_bucareste[b])


class TestSaida(unittest.TestCase):
    """RF05: rastro passo a passo."""

    def test_tc16_rastro_ligado(self):
        """TC-16 (RF05): com mostrar=True imprime 6 iterações de Arad a Bucareste."""
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            busca_a_estrela('Arad', OBJETIVO, mapa_romenia, heuristica_bucareste)
        saida = buffer.getvalue()
        self.assertIn('--- Busca A* de Arad para Bucareste ---', saida)
        self.assertIn('1. expandindo: Arad | g(n)=0, h(n)=366 -> f(n)=366', saida)
        self.assertIn('6. expandindo: Bucareste | g(n)=418, h(n)=0 -> f(n)=418', saida)
        self.assertIn('fronteira:', saida)

    def test_tc17_rastro_desligado(self):
        """TC-17 (RF05): com mostrar=False não imprime nada."""
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            busca_a_estrela('Arad', OBJETIVO, mapa_romenia,
                            heuristica_bucareste, mostrar=False)
        self.assertEqual(buffer.getvalue(), '')


class TestScripts(unittest.TestCase):
    """RNF01, RNF03: os scripts do programa e das fases rodam sem erro."""

    SCRIPTS = ['a_estrela.py', 'fase1 explorar.py', 'fase2_caminhos.py',
               'fase3_fronteira.py', 'fase4_expandir.py', 'fase5_busca.py']

    def test_tc18_scripts_executam(self):
        """TC-18 (RNF01, RNF03): cada script termina com código 0."""
        for script in self.SCRIPTS:
            with self.subTest(script=script):
                resultado = subprocess.run(
                    [sys.executable, script], cwd=RAIZ,
                    capture_output=True, text=True, timeout=30)
                self.assertEqual(resultado.returncode, 0, resultado.stderr)

    def test_tc19_programa_completo_confere_com_o_livro(self):
        """TC-19 (RF08): a_estrela.py imprime a conferência de 418 km."""
        resultado = subprocess.run(
            [sys.executable, 'a_estrela.py'], cwd=RAIZ,
            capture_output=True, text=True, timeout=30)
        self.assertIn('Conferido: igual ao livro (418 km, 4 passos).',
                      resultado.stdout)


if __name__ == '__main__':
    unittest.main(verbosity=2)
