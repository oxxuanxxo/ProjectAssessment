from fastapi import FastAPI, Body, HTTPException
from models import ConversationDocument, Prompt
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
import os
import openai
import hashlib

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    openai.api_key = os.getenv('OPENAI_API_KEY')
    client = AsyncIOMotorClient("mongodb://mongodb:27017")
    db = client.chat_hist  
    await init_beanie(database=db, document_models=[ConversationDocument])  

@app.post("/conversations", summary="Create a new conversation")
async def create_conversation(conversation: ConversationDocument = Body(..., example={
    "name": "Example Conversation",
    "messages": [{"content": "Hello, world!", "role": "user"}]
})):  
    await conversation.save()
    return conversation.dict()


@app.get("/conversations/{conversation_id}", response_model=ConversationDocument)
async def get_conversation(conversation_id: str):
    conversation = await ConversationDocument.get(conversation_id)
    if conversation:
        return conversation
    raise HTTPException(status_code=404, detail="Conversation not found")

@app.put("/conversations/{conversation_id}")
async def update_conversation(conversation_id: str, updated_conversation: ConversationDocument):
    conversation = await ConversationDocument.get(conversation_id)
    if conversation:
        conversation.name = updated_conversation.name 
        await conversation.save_changes()
        return conversation
    raise HTTPException(status_code=404, detail="Conversation not found")

@app.delete("/conversations/{conversation_id}")
async def delete_conversation(conversation_id: str):
    conversation = await ConversationDocument.get(conversation_id)
    if conversation:
        await conversation.delete()
        return {"detail": "Conversation deleted"}
    raise HTTPException(status_code=404, detail="Conversation not found")


@app.post("/prompts/{conversation_id}")
async def create_prompt(conversation_id: str, prompt: Prompt):
    conversation = await ConversationDocument.get(conversation_id)
    if conversation:
        # Include the conversation history in the prompt
        full_prompt = f"{conversation.history}\n{prompt.content}"
        response = openai.Completion.create(
            engine="davinci",
            prompt=full_prompt,
            max_tokens=150
        )
        conversation.history += f"\n{response.choices[0].text}"
        conversation.history = anonymize_data(conversation.history)  
        await conversation.save_changes()
        return {"content": response.choices[0].text}
    raise HTTPException(status_code=404, detail="Conversation not found")


def anonymize_data(data):
    if 'username' in data:
        data['username'] = hashlib.sha256(data['username'].encode()).hexdigest()
    if 'email' in data:
        data['email'] = hashlib.sha256(data['email'].encode()).hexdigest()
    return data


@app.get("/")
def read_root():
    return {"Hello": "World"}
