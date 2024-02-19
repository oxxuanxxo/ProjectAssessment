from fastapi import FastAPI
from models import ConversationDocument, Prompt
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
import os
import openai

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    openai.api_key = os.getenv('OPENAI_API_KEY')
    client = AsyncIOMotorClient("mongodb://mongodb:27017")
    db = client.chat_hist  
    await init_beanie(database=db, document_models=[ConversationDocument])  

@app.post("/conversations")
async def create_conversation(conversation: ConversationDocument):  
    await conversation.save()
    return conversation.dict()  

@app.get("/conversations/{conversation_id}", response_model=ConversationDocument)
async def get_conversation(conversation_id: str):
    return await ConversationDocument.get(conversation_id)

@app.post("/prompts")
async def create_prompt(prompt: Prompt):
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt.content,
        max_tokens=150
    )
    return {"content": response.choices[0].text}

@app.get("/")
def read_root():
    return {"Hello": "World"}
