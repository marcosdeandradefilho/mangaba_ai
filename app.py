import os
from fastapi import FastAPI
from mangaba import Team, Agent
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

@app.post("/analyze")
async def analyze(query: dict):
    team = Team("Jurídico")
    team.add_agents([Agent("A1", role="responder pergunta")])
    result = team.solve(query["text"])
    return {"output": result.output}
