from pydantic import BaseModel
from typing import Optional, List, Union

class MessageInput(BaseModel):
    role: str
    content: str

class ResponseRequest(BaseModel):
    model: Optional[str] = "ivan-cv"
    input: Union[str, List[MessageInput]]
    previous_response_id: Optional[str] = None

class ContentBlock(BaseModel):
    type: str = "text"
    text: str

class OutputMessage(BaseModel):
    type: str = "message"
    role: str = "assistant"
    content: List[ContentBlock]

class ResponseOutput(BaseModel):
    id: str
    object: str = "response"
    output: List[OutputMessage]