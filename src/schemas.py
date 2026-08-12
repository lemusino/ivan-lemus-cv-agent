from pydantic import BaseModel
from typing import Optional, List, Union

class MessageInput(BaseModel):
    role: str
    content: str

class ResponseRequest(BaseModel):
    model: Optional[str] = "ivan-cv"
    input: Union[str, List[MessageInput], List[dict]]  # acepta dicts también
    previous_response_id: Optional[str] = None
    instructions: Optional[str] = None  # Banorte puede mandarlo
    
    class Config:
        extra = "allow"  # ← CLAVE: ignora campos extra en vez de rechazarlos

class ContentBlock(BaseModel):
    type: str = "output_text"  # ← cambio aquí
    text: str

class OutputMessage(BaseModel):
    type: str = "message"
    role: str = "assistant"
    status: str = "completed"  # ← agregar esto
    content: List[ContentBlock]

class ResponseOutput(BaseModel):
    id: str
    object: str = "response"
    status: str = "completed"  # ← agregar esto
    output: List[OutputMessage]