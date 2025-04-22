from services.openai_service import OpenAIService
from db import crud

class OpenAIController:
    def __init__(self):
        #self.service = OpenAIService() 
        self.openai_service = OpenAIService()

    def generer_fiche_metier(self, emploi_id, prompt: str):
        """Génère une fiche métier pour un emploi donné et sauvegarde l’historique"""
        # Charger l'historique existant (si besoin)
        history_records = crud.get_prompt_history(emploi_id)
        history = []
        for row in history_records:
            history.append({"role": "user", "content": row[2]})
            history.append({"role": "assistant", "content": row[3]})
        self.openai_service.set_history(history)

        # Envoyer le nouveau prompt
        reponse = self.openai_service.ask(prompt)

        # Sauvegarder dans la base
        crud.save_prompt_history(emploi_id, prompt, reponse)

        return reponse

    def generer_sans_historique(self, prompt: str):
        """Génère une réponse unique (stateless) sans historique"""
        return self.openai_service.ask_once(prompt)

    def reinitialiser_historique(self):
        """Vide l'historique local (non base)"""
        self.openai_service.reset_history()

    def get_historique_json(self):
        """Export JSON de l’historique courant (à des fins de debug ou backup)"""
        return self.openai_service.export_history()

    def charger_historique_json(self, historique_json: str):
        """Importer un historique OpenAI depuis un JSON (utilitaire avancé)"""
        self.openai_service.import_history(historique_json)

   

    def generer_cartographie(self, prompt: str) -> str:
        return self.openai_service.ask_once(prompt)
