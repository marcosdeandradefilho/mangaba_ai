#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script de instalação das dependências do pacote Mangaba.

Execute este script para garantir que todas as dependências
estejam instaladas corretamente.
"""

import subprocess
import sys

def instalar_dependencias():
    """Instala todas as dependências necessárias."""
    print("Instalando dependências do Mangaba...")
    
    dependencias = [
        "google-generativeai>=0.8.3",
        "googlesearch-python>=1.2.1",
        "requests>=2.32.3",
        "aiohttp>=3.10.5",
        "tenacity>=8.5.0"
    ]
    
    for dep in dependencias:
        print(f"Instalando {dep}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
            print(f"✓ {dep} instalado com sucesso!")
        except subprocess.CalledProcessError:
            print(f"✗ Falha ao instalar {dep}")
            return False
    
    print("\nTodas as dependências foram instaladas com sucesso!")
    return True

if __name__ == "__main__":
    instalar_dependencias() 