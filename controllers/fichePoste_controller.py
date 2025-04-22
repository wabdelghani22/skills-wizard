# controllers/fiche_poste_controller.py

#from services.fiche_poste_service import FichePosteService
from services.fichePoste_service import FichePosteService
class FichePosteController:
    def __init__(self, projet_id):
        self.service = FichePosteService(projet_id)

    def sauvegarder_activites(self, emploi_id, activites):
        self.service.sauvegarder_activites(emploi_id, activites)

    
