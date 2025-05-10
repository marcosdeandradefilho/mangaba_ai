#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Casos de uso do Mangaba.AI com protocolos A2A e MCP
"""
import asyncio
import os
from dotenv import load_dotenv
from mangaba_ai.main import MangabaAI

# Carrega as variáveis de ambiente
load_dotenv()

async def case_development_team():
    """Caso 1: Equipe de Desenvolvimento Colaborativo"""
    print("\n=== Caso 1: Equipe de Desenvolvimento Colaborativo ===")
    
    mangaba = MangabaAI(os.getenv("GEMINI_API_KEY"))
    
    # Cria agentes da equipe
    product_manager = mangaba.create_agent(
        name="product_manager",
        role="Gerente de Produto",
        goal="Definir requisitos e prioridades do produto"
    )
    
    architect = mangaba.create_agent(
        name="architect",
        role="Arquiteto de Software",
        goal="Projetar a arquitetura do sistema"
    )
    
    developer = mangaba.create_agent(
        name="developer",
        role="Desenvolvedor",
        goal="Implementar funcionalidades"
    )
    
    tester = mangaba.create_agent(
        name="tester",
        role="Testador",
        goal="Garantir a qualidade do código"
    )
    
    # Fluxo de desenvolvimento
    print("\n1. Gerente de Produto define requisitos...")
    requirements = await product_manager.execute(
        "Defina os requisitos para um sistema de gerenciamento de tarefas com IA"
    )
    print(f"\nRequisitos:\n{requirements}\n")
    
    # Envia requisitos para o arquiteto
    await product_manager.a2a.send_message(
        product_manager.name,
        architect.name,
        f"Projete a arquitetura baseada nestes requisitos: {requirements}"
    )
    
    # Arquiteto processa e envia para o desenvolvedor
    arch_messages = await architect.a2a.receive_messages(architect.name)
    for msg in arch_messages:
        architecture = await architect.execute(msg["content"])
        print(f"\nArquitetura:\n{architecture}\n")
        
        await architect.a2a.send_message(
            architect.name,
            developer.name,
            f"Implemente o sistema seguindo esta arquitetura: {architecture}"
        )
    
    # Desenvolvedor implementa e envia para o testador
    dev_messages = await developer.a2a.receive_messages(developer.name)
    for msg in dev_messages:
        implementation = await developer.execute(msg["content"])
        print(f"\nImplementação:\n{implementation}\n")
        
        await developer.a2a.send_message(
            developer.name,
            tester.name,
            f"Teste esta implementação: {implementation}"
        )
    
    # Testador executa testes
    test_messages = await tester.a2a.receive_messages(tester.name)
    for msg in test_messages:
        test_results = await tester.execute(msg["content"])
        print(f"\nResultados dos Testes:\n{test_results}\n")

async def case_research_team():
    """Caso 2: Equipe de Pesquisa Científica"""
    print("\n=== Caso 2: Equipe de Pesquisa Científica ===")
    
    mangaba = MangabaAI(os.getenv("GEMINI_API_KEY"))
    
    # Cria agentes da equipe de pesquisa
    researcher = mangaba.create_agent(
        name="researcher",
        role="Pesquisador",
        goal="Conduzir pesquisa científica"
    )
    
    data_analyst = mangaba.create_agent(
        name="data_analyst",
        role="Analista de Dados",
        goal="Analisar dados de pesquisa"
    )
    
    writer = mangaba.create_agent(
        name="writer",
        role="Escritor Científico",
        goal="Redigir artigos científicos"
    )
    
    reviewer = mangaba.create_agent(
        name="reviewer",
        role="Revisor",
        goal="Revisar e validar pesquisas"
    )
    
    # Fluxo de pesquisa
    print("\n1. Pesquisador conduz estudo...")
    research = await researcher.execute(
        "Realize uma pesquisa sobre o impacto da IA na educação"
    )
    print(f"\nPesquisa:\n{research}\n")
    
    # Envia para análise de dados
    await researcher.a2a.send_message(
        researcher.name,
        data_analyst.name,
        f"Analise estes dados de pesquisa: {research}"
    )
    
    # Analista processa e envia para o escritor
    analysis_messages = await data_analyst.a2a.receive_messages(data_analyst.name)
    for msg in analysis_messages:
        analysis = await data_analyst.execute(msg["content"])
        print(f"\nAnálise:\n{analysis}\n")
        
        await data_analyst.a2a.send_message(
            data_analyst.name,
            writer.name,
            f"Escreva um artigo científico baseado nesta análise: {analysis}"
        )
    
    # Escritor redige e envia para revisão
    writer_messages = await writer.a2a.receive_messages(writer.name)
    for msg in writer_messages:
        article = await writer.execute(msg["content"])
        print(f"\nArtigo:\n{article}\n")
        
        await writer.a2a.send_message(
            writer.name,
            reviewer.name,
            f"Revise este artigo científico: {article}"
        )
    
    # Revisor avalia
    review_messages = await reviewer.a2a.receive_messages(reviewer.name)
    for msg in review_messages:
        review = await reviewer.execute(msg["content"])
        print(f"\nRevisão:\n{review}\n")

async def case_support_team():
    """Caso 3: Equipe de Suporte ao Cliente"""
    print("\n=== Caso 3: Equipe de Suporte ao Cliente ===")
    
    mangaba = MangabaAI(os.getenv("GEMINI_API_KEY"))
    
    # Cria agentes da equipe de suporte
    support_agent = mangaba.create_agent(
        name="support_agent",
        role="Agente de Suporte",
        goal="Atender solicitações de clientes"
    )
    
    technical_agent = mangaba.create_agent(
        name="technical_agent",
        role="Agente Técnico",
        goal="Resolver problemas técnicos"
    )
    
    feedback_agent = mangaba.create_agent(
        name="feedback_agent",
        role="Agente de Feedback",
        goal="Coletar e analisar feedback"
    )
    
    # Fluxo de suporte
    print("\n1. Agente de Suporte recebe solicitação...")
    support_request = await support_agent.execute(
        "Atenda uma solicitação de suporte sobre problemas de conexão"
    )
    print(f"\nAtendimento:\n{support_request}\n")
    
    # Envia para agente técnico
    await support_agent.a2a.send_message(
        support_agent.name,
        technical_agent.name,
        f"Resolva este problema técnico: {support_request}"
    )
    
    # Agente técnico processa e envia para feedback
    tech_messages = await technical_agent.a2a.receive_messages(technical_agent.name)
    for msg in tech_messages:
        solution = await technical_agent.execute(msg["content"])
        print(f"\nSolução Técnica:\n{solution}\n")
        
        await technical_agent.a2a.send_message(
            technical_agent.name,
            feedback_agent.name,
            f"Analise o feedback desta solução: {solution}"
        )
    
    # Agente de feedback avalia
    feedback_messages = await feedback_agent.a2a.receive_messages(feedback_agent.name)
    for msg in feedback_messages:
        feedback = await feedback_agent.execute(msg["content"])
        print(f"\nAnálise de Feedback:\n{feedback}\n")

async def main():
    """Função principal que executa todos os casos."""
    try:
        # Executa cada caso de uso
        await case_development_team()
        await case_research_team()
        await case_support_team()
        
    except Exception as e:
        print(f"Erro: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main()) 