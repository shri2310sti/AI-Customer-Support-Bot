import json
import os
from typing import List, Dict, Tuple
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

# Gemini API model
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"


class GeminiService:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        self.api_key = api_key
        self.faqs = self._load_faqs()

    def _load_faqs(self) -> List[Dict]:
        try:
            with open("faqs.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def _build_system_prompt(self, concise: bool = True) -> str:
        faq_context = "\n".join([f"Q: {faq['question']}\nA: {faq['answer']}\n" for faq in self.faqs])
        reply_style = "short and concise (1-3 sentences)" if concise else "detailed and comprehensive"

        return f"""
You are a customer support assistant. Use the FAQ knowledge base as reference but not exclusively.
Always answer in a {reply_style} style.
Maintain a friendly, professional, and helpful tone.
Escalate to a human agent only if necessary.

FAQ Knowledge Base:
{faq_context}
"""

    def _determine_escalation(self, query: str, response: str) -> bool:
        indicators = [
            "connect you with a human support agent",
            "connect you with a senior support agent",
            "transfer you",
            "escalate",
            "human support",
            "senior support agent",
            "specialized issue that requires expert attention"
        ]
        return any(ind.lower() in response.lower() for ind in indicators)

    def generate_response(
        self, query: str, conversation_history: List[Dict] = None, concise: bool = True
    ) -> Tuple[str, bool]:
        try:
            context = ""
            if conversation_history:
                context = "\n".join([f"{msg['role'].title()}: {msg['content']}" for msg in conversation_history[-5:]])
                context = f"Previous conversation:\n{context}\n\n"

            full_prompt = f"{self._build_system_prompt(concise=concise)}\n{context}Customer Question: {query}\n\nPlease respond:"

            payload = {"contents": [{"parts": [{"text": full_prompt}]}]}
            resp = requests.post(GEMINI_API_URL, params={"key": self.api_key}, json=payload, timeout=30)
            resp.raise_for_status()
            data = resp.json()
            candidates = data.get("candidates", [])
            response_text = ""

            if candidates:
                content = candidates[0].get("content", {})
                parts = content.get("parts", [])
                if parts:
                    response_text = parts[0].get("text", "").strip()

            if not response_text:
                response_text = (
                    "I apologize, but I'm experiencing technical difficulties. "
                    "Let me connect you with a senior support agent."
                )

            return response_text, self._determine_escalation(query, response_text)

        except Exception:
            return (
                "I apologize, but I'm experiencing technical difficulties. "
                "Let me connect you with a senior support agent.",
                True
            )

    def get_faqs(self) -> List[Dict]:
        return self.faqs
