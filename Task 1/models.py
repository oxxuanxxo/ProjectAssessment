from beanie import Document
from pydantic import BaseModel

class Conversation(BaseModel):
    name: str

class ConversationDocument(Document, Conversation):
    pass

class Prompt(BaseModel):
    role: str
    content: str
