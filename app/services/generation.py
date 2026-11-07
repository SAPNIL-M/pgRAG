from abc import ABC,abstractmethod
from typing import AsyncGenerator
from google import genai
import json
import httpx
from app.core.config import settings

class LlmProvider(ABC):
    @abstractmethod
    def generate_stream(self,prompt:str)->AsyncGenerator[str,None]:
        raise NotImplementedError

class OllamaProvider(LlmProvider):
    def __init__(self,base_url:str|None=None,model:str|None=None):
        self.base_url = base_url or settings.OLLAMA_BASE_URL
        self.model = model or settings.OLLAMA_MODEL

    async def generate_stream(self, prompt: str) -> AsyncGenerator[str, None]:
        async with httpx.AsyncClient(timeout=60.0) as client:
            async with client.stream("POST",f"{self.base_url}/api/generate",json={"model":self.model,"prompt":prompt,"stream":True}) as response:
                response.raise_for_status()
                async for line in response.aiter_lines():
                    if line :
                        data=json.loads(line)
                        token = data.get("response","")
                        if token:
                            yield token

class GeminiProvider(LlmProvider):
    def __init__(self,api_key:str|None=None,model:str|None=None) -> None:
        
        self.api_key = api_key or settings.GEMINI_API_KEY
        
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not set . Please add it to your environment")

        self.model = model or settings.GEMINI_MODEL
        self.client = genai.Client(api_key=self.api_key)

    async def generate_stream(self, prompt: str) -> AsyncGenerator[str, None]:
        response = await self.client.aio.models.generate_content_stream(model=self.model,contents=prompt)
        async for chunk in response:
            if chunk.text:
                yield chunk.text

class GenerationService:
    def __init__(self,provider : LlmProvider|None = None) -> None:
        self.provider = provider or  self.resolve_provider()
    
    def resolve_provider(self)->LlmProvider:
        provider_name = settings.LLM_PROVIDER
        if provider_name == "gemini":
            return GeminiProvider()
        elif provider_name == "ollama":
            return OllamaProvider()
        else:
            raise ValueError("Please provide a valid Provider")

    async def generate_answer_stream(self,query:str,context:str)->AsyncGenerator[str,None]:
        final_prompt = build_rag_prompt(query=query,context=context)
        async for token in self.provider.generate_stream(prompt=final_prompt):
            yield token


    
        


def build_rag_prompt(query: str, context: str) -> str:
    return f"""You are a helpful assistant that answers questions strictly based on the provided document excerpts.

Instructions:
1. Answer the question using ONLY the facts directly mentioned in the Context below.
2. Do NOT extrapolate, speculate, or bring in outside knowledge.
3. For every fact or claim you provide, cite the corresponding page number using the format [Page X].
4. If the context does not contain enough information to answer the question, state: "I do not have enough information in the provided document to answer this question."

Context:
{context}

Question: {query}
Answer:"""