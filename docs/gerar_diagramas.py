# -*- coding: utf-8 -*-
"""Gera as imagens PNG em docs/img/ a partir dos blocos ```mermaid dos .md.

Os arquivos .md são a fonte da verdade; as imagens são derivadas deles.
O nome de cada imagem vem do título (##) que vem antes do bloco.

Requisitos (só para gerar as imagens, o projeto A* não precisa disso):
    npm install -g @mermaid-js/mermaid-cli     # comando mmdc
    e um Chrome/Chromium instalado

Uso, a partir da raiz do projeto:
    python docs/gerar_diagramas.py
"""
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
import unicodedata

DOCS = pathlib.Path(__file__).resolve().parent
IMG = DOCS / 'img'


def slug(texto):
    texto = unicodedata.normalize('NFKD', texto).encode('ascii', 'ignore').decode()
    texto = re.sub(r'[^a-zA-Z0-9]+', '-', texto).strip('-').lower()
    return texto


def blocos_mermaid(arquivo):
    """Devolve (nome_da_imagem, codigo) para cada bloco mermaid do arquivo."""
    titulo, dentro, codigo = '', False, []
    for linha in arquivo.read_text(encoding='utf-8').splitlines():
        if not dentro and linha.startswith('#'):
            titulo = linha.lstrip('#').strip()
        elif not dentro and linha.strip() == '```mermaid':
            dentro, codigo = True, []
        elif dentro and linha.strip() == '```':
            dentro = False
            yield slug(titulo), '\n'.join(codigo) + '\n'
        elif dentro:
            codigo.append(linha)


def main():
    mmdc = shutil.which('mmdc')
    if not mmdc:
        sys.exit('mmdc não encontrado. Instale com: npm install -g @mermaid-js/mermaid-cli')

    IMG.mkdir(exist_ok=True)
    config = {}
    if os.environ.get('PUPPETEER_EXECUTABLE_PATH'):
        config['executablePath'] = os.environ['PUPPETEER_EXECUTABLE_PATH']
    if hasattr(os, 'geteuid') and os.geteuid() == 0:  # Chrome recusa rodar como root com sandbox
        config['args'] = ['--no-sandbox']

    with tempfile.TemporaryDirectory() as tmp:
        cfg = pathlib.Path(tmp) / 'puppeteer.json'
        cfg.write_text(json.dumps(config))
        total = 0
        for md in sorted(DOCS.glob('*.md')):
            for nome, codigo in blocos_mermaid(md):
                entrada = pathlib.Path(tmp) / f'{nome}.mmd'
                entrada.write_text(codigo, encoding='utf-8')
                saida = IMG / f'{nome}.png'
                subprocess.run([mmdc, '-i', str(entrada), '-o', str(saida),
                                '-p', str(cfg), '-b', 'white', '-s', '2'],
                               check=True)
                print('gerado:', saida.relative_to(DOCS.parent))
                total += 1
    print(f'{total} diagramas gerados.')


if __name__ == '__main__':
    main()
