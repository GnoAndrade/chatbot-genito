# Chatbot con Búsqueda Web y Respuestas en Streaming

## Descripción
Chatbot de consola que mantiene memoria de conversación, realiza búsquedas en internet y proporciona respuestas en streaming citando fuentes.

## Requisitos
- Python 3.9+
- Cuenta en OpenAI con API key
- Cuenta en Serper.dev con API key

## Dependencias
\```bash
python3 -m pip install openai aiohttp beautifulsoup4 requests python-dotenv pytest pytest-asyncio
\```

## Configuración
1. Crear archivo `.env` en la raíz del proyecto:
\```
OPENAI_API_KEY=sk-your_openai_key_here
SERPER_API_KEY=your_serper_key_here
\```

2. Las API keys deben obtenerse de:
- OpenAI: https://platform.openai.com/account/api-keys
- Serper: https://serper.dev

## Estructura del Proyecto
\```
chatbot/
├── chatbot.py
├── tests/
│   └── test_chatbot.py
└── .env
\```

## Funcionalidades
- Búsqueda en internet usando Serper API
- Extracción de texto de páginas web
- Respuestas en streaming usando GPT-3.5
- Memoria de conversación durante la ejecución
- Citación de fuentes consultadas

## Ejecución del Chatbot
\```bash
python3 chatbot.py
\```

### Uso
1. Ingresar preguntas en la consola
2. El chatbot buscará información relevante
3. Mostrará la respuesta en streaming
4. Listará las fuentes consultadas
5. Escribir 'salir' para terminar

## Ejecución de Pruebas
\```bash
python3 -m pytest tests/test_chatbot.py -v
\```

### Pruebas Implementadas
- Búsqueda en internet
- Extracción de texto
- Generación de respuestas AI
- Manejo del historial
- Límites de conversación
- Validación de API keys

## Ejemplos de Uso
\```
> Tú: ¿Cómo funciona Python?

> Chatbot: Buscando información en internet...
[Respuesta en streaming...]

Fuentes consultadas:
- https://python.org/about
- https://docs.python.org
\```

## Notas Técnicas
- Usa aiohttp para peticiones asíncronas
- BeautifulSoup4 para extracción de texto
- OpenAI API para generación de respuestas
- Serper API para búsquedas en Google
- Pytest para pruebas automatizadas
