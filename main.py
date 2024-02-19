from fastapi import FastAPI
from models import ConversationDocument, Prompt
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    client = AsyncIOMotorClient("mongodb://mongodb:27017")
    db = client.chat_hist  
    await init_beanie(database=db, document_models=[ConversationDocument])  

@app.post("/conversations")
async def create_conversation(conversation: ConversationDocument):  
    await conversation.insert()
    return conversation.dict()  

@app.post("/prompts")
async def create_prompt(prompt: Prompt):
    return {"role": prompt.role, "content": prompt.content}
