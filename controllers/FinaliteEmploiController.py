#from services.finalite_emploi_service import FinaliteEmploiService


from services.FinaliteEmploiService import FinaliteEmploiService
class FinaliteEmploiController:
    def __init__(self, projet_id):
        self.service = FinaliteEmploiService(projet_id)

    def charger_finalite(self, emploi_id):
        if not self.service.emploi_exists(emploi_id):
            raise ValueError("Emploi non trouvé")
        return self.service.get_finalite(emploi_id)

    def sauvegarder_finalite(self, emploi_id, finalite):
        if not finalite:
            raise ValueError("Finalité vide")
        if not self.service.emploi_exists(emploi_id):
            raise ValueError("Emploi non trouvé")
        self.service.set_finalite(emploi_id, finalite)
