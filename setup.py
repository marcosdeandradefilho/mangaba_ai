"""
Setup configuration for Mangaba.AI
"""
from setuptools import setup, find_packages

# Carrega o README para a descrição longa
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Carrega as dependências do requirements.txt
with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="mangaba-ai",
    version="0.1.0",
    author="Mangaba.AI Team",
    author_email="contact@mangaba.ai",
    description="Framework para desenvolvimento de agentes autônomos",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mangaba-ai/mangaba-ai",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
) 