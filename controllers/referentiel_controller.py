from services.referentiel_service import ReferentielService

class ReferentielController:
    def __init__(self, projet_id):
        self.service = ReferentielService(projet_id)

    # --- 🔹 RÉFÉRENTIEL DE COMPÉTENCES --- #

    def get_referentiel(self):
        """Retourne la liste des compétences du projet."""
        return self.service.get_referentiel()

    def ajouter_competence(self, nom, type_competence="hard", description=None, definitions_par_niveau=None):
        """
        Ajoute une compétence avec :
        - type (hard/soft)
        - description globale
        - dictionnaire par niveau (optionnel)
        """
        return self.service.ajouter_competence(nom, type_competence, description, definitions_par_niveau)

    def supprimer_competence(self, nom_competence):
        """Supprime une compétence et ses associations."""
        return self.service.supprimer_competence(nom_competence)

    def modifier_nom_competence(self, ancien_nom, nouveau_nom):
        """Renomme une compétence."""
        return self.service.modifier_nom_competence(ancien_nom, nouveau_nom)

    def modifier_description_competence(self, nom_competence, nouvelle_description):
        """Met à jour la description globale d’une compétence."""
        return self.service.modifier_description_competence(nom_competence, nouvelle_description)

    def competence_existe(self, nom):
        """Vérifie si une compétence existe déjà."""
        return self.service.competence_existe(nom)

    # --- 🔹 DICTIONNAIRE PAR NIVEAU --- #

    def get_definitions_niveaux(self, competence_id):
        """Retourne un dictionnaire des niveaux avec leurs définitions."""
        return self.service.get_definitions_niveaux(competence_id)

    def modifier_definition_niveau(self, competence_id, niveau, texte):
        """Met à jour le texte associé à un niveau donné d’une compétence."""
        return self.service.modifier_definition_niveau(competence_id, niveau, texte)

    # --- 🔹 IMPORT / EXPORT (facultatif) --- #

    def importer_referentiel(self, chemin):
        return self.service.import_referentiel_from_file(chemin)

    def exporter_referentiel(self, chemin):
        return self.service.export_referentiel_to_file(chemin)

    

