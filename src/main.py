from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from src.schemas import ResponseRequest, ResponseOutput, OutputMessage, ContentBlock
from src.agent import get_response
import uuid
import logging
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Iván Lemus CV Agent", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/v1/responses")
async def create_response(request: Request):
    # Log del raw body para debug
    raw_body = await request.body()
    logger.info(f"=== REQUEST DE BANORTE ===")
    logger.info(f"Headers: {dict(request.headers)}")
    logger.info(f"Body raw: {raw_body}")
    
    try:
        body = json.loads(raw_body)
        logger.info(f"Body parsed: {json.dumps(body, ensure_ascii=False, indent=2)}")
    except Exception as e:
        logger.error(f"Body no es JSON: {e}")
        body = {}

    # Extraer input de forma flexible
    input_data = body.get("input", "")
    
    if isinstance(input_data, str):
        messages = [{"role": "user", "content": input_data}]
    elif isinstance(input_data, list):
        messages = []
        for item in input_data:
            if isinstance(item, dict):
                role = item.get("role", "user")
                # Puede venir como string o como lista de content blocks
                content = item.get("content", "")
                if isinstance(content, list):
                    # formato Open Responses: content es lista de bloques
                    text = " ".join(
                        block.get("text", "") 
                        for block in content 
                        if isinstance(block, dict)
                    )
                    messages.append({"role": role, "content": text})
                else:
                    messages.append({"role": role, "content": str(content)})
    else:
        messages = [{"role": "user", "content": str(input_data)}]

    logger.info(f"Messages normalizados: {messages}")

    reply = await get_response(messages)
    logger.info(f"Respuesta Gemini: {reply[:100]}...")

    response = ResponseOutput(
        id=f"resp_{uuid.uuid4().hex[:8]}",
        output=[OutputMessage(content=[ContentBlock(text=reply)])]
    )
    
    logger.info(f"Response enviado: {response.model_dump()}")
    return response

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