from langchain_openai import OpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
import numpy as np
from datetime import datetime
from config.llm_config import LLMSettings

CHROMA_DB_DIR = LLMSettings().CHROMA_DB_DIR
OPENAI_API_KEY = LLMSettings().OPENAI_API_KEY

class LLMService:
    def __init__(self):
        self.llm = OpenAI(model='gpt-3.5-turbo-instruct', api_key=OPENAI_API_KEY)
        self.embeddings = OpenAIEmbeddings(model='text-embedding-3-small')

        self.vectorstorage = Chroma(
            embedding_function=self.embeddings,
            persist_directory=CHROMA_DB_DIR
        )


    async def process(self, chat_id: int, message: str) -> str:
        context = self._get_relevant_context(chat_id=chat_id, message=message)

        prompt = self._build_prompt(context=context, message=message)
        response = self.llm.generate(prompts=[prompt])
        bot_reply = response.generations[0][0].text

        self._save_relevant_context(chat_id=chat_id, user_message=message, bot_message=bot_reply)

        return bot_reply

    def _get_relevant_context(self, chat_id: int, message: str):
        query_emb = self.embeddings.embed_query(message) # создаём эмбеддинг из сообщения

        docs = self.vectorstorage.similarity_search_by_vector(embedding=query_emb, # поиск в векторной базе данных
            k=2, # кол-во возвращаемых фрагментов
            filter={'chat_id': str(chat_id)}) # фильтруем по чату

        return '\n'.join(doc.page_content for doc in docs)

    def _save_relevant_context(self, chat_id: int, user_message: str, bot_message: str):
        documents = [
            Document(
                page_content=user_message, # Сохраняем пользовательский запрос
                metadata={'chat_id': str(chat_id), 'type': 'user', 'time': datetime.now().isoformat()}
            ),

            Document(
                page_content=bot_message, # Сохраняем ответ от llm
                metadata={'chat_id': str(chat_id), 'type': 'bot', 'time': datetime.now().isoformat()}
            )

        ]

        self.vectorstorage.add_documents(documents=documents) # добавляем в векторную базу данных

    def _build_prompt(self, context: str, message: str) -> str:
        if context:
            return f"""Системный промпт: {context} 
                    Вопрос: {message}"""
        else:
            return message



    


