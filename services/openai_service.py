import openai
import os
import json
from typing import List
from dotenv import load_dotenv

load_dotenv()  # Charge les variables depuis le fichier .env

openai.api_key = os.getenv("OPENAI_API_KEY")

class OpenAIService:
    def __init__(self, model="gpt-4o", temperature=0.7):
        self.model = model
        self.temperature = temperature
        self.conversation_history = []

    def set_config(self, model=None, temperature=None):
        """Met à jour dynamiquement les paramètres (optionnel)"""
        if model:
            self.model = model
        if temperature is not None:
            self.temperature = temperature

    def set_history(self, history: List[dict]):
        self.conversation_history = history

    def reset_history(self):
        self.conversation_history = []

    def add_message(self, role: str, content: str):
        self.conversation_history.append({
            "role": role,
            "content": content.strip()
        })

    def ask(self, prompt: str, role="user", save_in_history=True) -> str:
        """Prompt avec historique conversationnel"""
        if save_in_history:
            self.add_message(role, prompt)

        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=self.conversation_history,
                temperature=self.temperature
            )
            reply = response["choices"][0]["message"]["content"]
            if save_in_history:
                self.add_message("assistant", reply)
            return reply

        except openai.error.OpenAIError as e:
            return f"[Erreur OpenAI] {str(e)}"

    
    def ask_once(self, prompt: str) -> str:
        """Envoie un prompt sans historique (mode stateless)"""
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature
            )
            
            return response.choices[0].message.content.strip()

        except Exception as e:
            return f"[Erreur OpenAI] {str(e)}"

    def export_history(self) -> str:
        """Exporte l’historique complet (JSON str)"""
        return json.dumps(self.conversation_history, ensure_ascii=False, indent=2)

    def import_history(self, history_json: str):
        """Recharge un historique depuis un JSON (str)"""
        try:
            self.conversation_history = json.loads(history_json)
        except Exception as e:
            print(f"Erreur lors de l’import JSON : {e}")
