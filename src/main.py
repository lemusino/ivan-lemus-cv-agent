from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.schemas import ResponseRequest, ResponseOutput, OutputMessage, ContentBlock
from src.agent import get_response
import uuid

app = FastAPI(title="Iván Lemus CV Agent", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/v1/responses")
async def create_response(req: ResponseRequest):
    if isinstance(req.input, str):
        messages = [{"role": "user", "content": req.input}]
    else:
        messages = [{"role": m.role, "content": m.content} for m in req.input]

    reply = await get_response(messages)

    return ResponseOutput(
        id=f"resp_{uuid.uuid4().hex[:8]}",
        output=[OutputMessage(content=[ContentBlock(text=reply)])]
    )

@app.get("/.well-known/agent-card.json")
async def agent_card():
    return {
        "protocolVersion": "0.3.0",
        "name": "Agente CV de Iván Lemus",
        "description": "Agente conversacional sobre el perfil profesional de Iván Jesús Lemus Aguilar, Senior Data & Analytics y Product Manager con 15 años de experiencia.",
        "version": "1.0.0",
        "capabilities": {"streaming": False},
        "skills": [
            {
                "id": "cv-profile",
                "name": "Perfil profesional",
                "examples": [
                    "¿Cuál es tu experiencia en datos?",
                    "¿En qué proyectos de IA has trabajado?",
                    "¿Cuáles son tus habilidades principales?"
                ]
            }
        ]
    }

@app.get("/")
async def health():
    return {"status": "ok", "agent": "ivan-lemus-cv-agent", "version": "1.0.0"}