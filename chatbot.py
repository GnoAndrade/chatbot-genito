from dotenv import load_dotenv
import os
import requests
from typing import List, Dict
import asyncio
from bs4 import BeautifulSoup
import aiohttp
from openai import AsyncOpenAI
import json

load_dotenv()

# Configuración de APIs
SERPER_API_KEY = os.getenv('SERPER_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

class Chatbot:
    def __init__(self):
        self.conversation_history = []
        self.client = AsyncOpenAI(api_key=OPENAI_API_KEY)

    async def search_internet(self, query: str) -> List[str]:
        """Realiza búsqueda en internet usando Serper API"""
        headers = {
            'X-API-KEY': SERPER_API_KEY,
            'Content-Type': 'application/json'
        }
        # Aseguramos que ningún header sea None
        headers = {k: v for k, v in headers.items() if k is not None and v is not None}
        
        payload = {
            'q': query,
            'num': 5
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post('https://google.serper.dev/search', headers=headers, json=payload) as response:
                results = await response.json()
                return [result['link'] for result in results.get('organic', [])][:5]


    async def extract_text(self, url: str) -> str:
        """Extrae el texto principal de una URL"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    # Eliminar scripts y estilos
                    for script in soup(['script', 'style']):
                        script.decompose()
                    return ' '.join(soup.stripped_strings)
        except:
            return ""

    async def get_ai_response(self, user_input: str, context: str) -> str:
        """Obtiene respuesta del modelo LLM"""
        messages = self.conversation_history + [
            {"role": "system", "content": f"Contexto de búsqueda web: {context}"},
            {"role": "user", "content": user_input}
        ]
        
        response = await self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            stream=True
        )
        
        full_response = ""
        print("\nChatbot: ", end="", flush=True)
        
        async for chunk in response:
            if chunk.choices[0].delta.content:
                print(chunk.choices[0].delta.content, end="", flush=True)
                full_response += chunk.choices[0].delta.content
                
        return full_response

    async def process_user_input(self, user_input: str):
        """Procesa la entrada del usuario y genera una respuesta"""
        print("\nBuscando información en internet...")
        
        # Realizar búsqueda
        urls = await self.search_internet(user_input)
        
        # Extraer texto de las URLs
        texts = []
        for url in urls:
            text = await self.extract_text(url)
            if text:
                texts.append(text[:1000])
        
        # Crear contexto combinando el historial y la nueva información
        context = "\n".join(texts)
        
        # Obtener y mostrar respuesta
        response = await self.get_ai_response(user_input, context)
        
        # Actualizar historial con formato específico para mantener contexto
        self.conversation_history.extend([
            {
                "role": "user",
                "content": f"Pregunta anterior: {user_input}"
            },
            {
                "role": "assistant",
                "content": f"Respuesta anterior: {response}"
            }
        ])
        
        # Limitar el historial a las últimas 5 interacciones para mantener relevancia
        if len(self.conversation_history) > 10:
            self.conversation_history = self.conversation_history[-10:]
        
        # Mostrar fuentes
        print("\n\nFuentes consultadas:")
        for url in urls:
            print(f"- {url}")


async def main():
    chatbot = Chatbot()
    print("¡Bienvenido al Chatbot! (Escribe 'salir' para terminar)")
    
    while True:
        user_input = input("\nTú: ").strip()
        if user_input.lower() == 'salir':
            break
        await chatbot.process_user_input(user_input)

if __name__ == "__main__":
    asyncio.run(main())
