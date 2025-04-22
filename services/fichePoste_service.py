# services/fiche_poste_service.py

from db import crud

class FichePosteService:
    def __init__(self, projet_id):
        self.projet_id = projet_id

    def sauvegarder_activites2(self, emploi_id, activites):
        crud.supprimer_activites_pour_emploi(emploi_id)
        for macro in activites:
            macro_id = crud.ajouter_macro_activite(emploi_id, macro["titre"])
            for micro in macro["micro_activites"]:
                crud.ajouter_micro_activite(macro_id, micro)

    def sauvegarder_activites(self, emploi_id, activites):
        for macro in activites:
            # Au lieu de "macro['titre']", on utilise "macro['contenu']"
            contenu_macro = macro["titre"]  # Remplacer "titre" par "contenu"
            
            # Insertion dans la table des macro-activités
            macro_id = crud.ajouter_macro_activite(emploi_id, contenu_macro)
            
            for micro in macro["micro_activites"]:
                # Insertion des micro-activités liées à la macro-activité
                crud.ajouter_micro_activite(macro_id, micro)

