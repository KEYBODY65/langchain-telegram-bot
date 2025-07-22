from fastapi import FastAPI
from llm_service import LLMService

app = FastAPI()
llm = LLMService()

@app.post('/process')
async def llm_process_message(chat_id: int, message: str):
    await llm.process(chat_id=chat_id, message=message)

