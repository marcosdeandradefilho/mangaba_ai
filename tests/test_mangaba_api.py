import pytest
from mangaba_ai.core.agent import Agent
from mangaba_ai.core.mcp import MCP
from mangaba_ai.schemas.message import Message

@pytest.mark.asyncio
async def test_agent_message_processing():
    """Testa o processamento de mensagens pelo Agent"""
    agent = Agent()
    message = Message(
        content="Teste de mensagem",
        sender="TestUser",
        timestamp="1234567890"
    )
    
    result = await agent.process_message(message)
    
    assert result["content"] == "Teste de mensagem"
    assert result["sender"] == "TestUser"
    assert result["timestamp"] == "1234567890"
    assert result["processed"] is True

@pytest.mark.asyncio
async def test_mcp_conversation_analysis():
    """Testa a análise de conversas pelo MCP"""
    mcp = MCP()
    messages = [
        Message(
            content="Primeira mensagem",
            sender="User1",
            timestamp="1234567890"
        ),
        Message(
            content="Segunda mensagem",
            sender="User2",
            timestamp="1234567891"
        )
    ]
    
    result = await mcp.analyze_conversation(messages)
    
    assert result.message_count == 2
    assert result.participants == 2
    assert "Total de mensagens: 2" in result.summary
    assert "Participantes: 2" in result.summary
    assert len(result.processed_messages) == 2 