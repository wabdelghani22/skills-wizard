from services.referentiel_service import ReferentielService

class CompetenceController:
    def __init__(self, projet_id):
        self.projet_id = projet_id
        self.service = ReferentielService(projet_id)

    def sauvegarder_referentiel(self, liste_competences):
        self.service.enregistrer_competences(liste_competences)

    def ajouter_competence(self, projet_id, emploi_id, nom, type_, niveau, definition=None):
        return self.service.ajouter_et_associer_competence(
            projet_id, emploi_id, nom, type_, niveau, definition
        )
    def supprimer_competence_de_emploi_et_referentiel(self, emploi_id, nom_comp, projet_id):
        from services.competence_service import supprimer_competence_d_un_emploi, supprimer_du_referentiel_si_orphelin
        supprimer_competence_d_un_emploi(emploi_id, nom_comp, projet_id)
        supprimer_du_referentiel_si_orphelin(nom_comp, projet_id)

    def get_autocomplete_competences(self, projet_id, prefixe):
        return self.service.rechercher_competences_par_prefixe(projet_id, prefixe)

    def charger_referentiel(self):
        return self.service.charger_competences()

    def fusionner_et_sauvegarder(self, ancienne_liste, nouvelles_valeurs):
        fusion = self.service.fusionner_competences(ancienne_liste, nouvelles_valeurs)
        self.service.enregistrer_competences(fusion)
        return fusion

    def charger_dictionnaire(self):
        return self.service.charger_dictionnaire()
    def sauvegarder_dictionnaire(self, dictionnaire_data, niveaux):
        self.service.sauvegarder_dictionnaire(dictionnaire_data, niveaux)
    
    def sauvegarder_competences_emploi(self, emploi_nom, competences):
        self.service.sauvegarder_competences_emploi(emploi_nom, competences)
    
    def modifier_competence_globale(self, ancien_nom, nouveau_nom, niveau, type_):
        self.service.modifier_competence_globale(self, ancien_nom, nouveau_nom, niveau, type_)
        
    def get_emploi_ids_avec_competences(self):
        return self.service.get_emploi_ids_avec_competences()
    
    def supprimer_competence_d_un_emploi(self,emploi_id, nom_comp):
        self.service.supprimer_competence_d_un_emploi(emploi_id, nom_comp, self.projet_id)

    def supprimer_du_referentiel_si_orphelin(self,nom_comp):
        est_orphelin = crud.est_competence_orpheline(nom_comp, self.projet_id)
        if est_orphelin:
            self.service.supprimer_competence_du_referentiel(nom_comp, self.projet_id)

    def supprimer_competence_de_emploi_et_referentiel(self, emploi_id, nom_comp):
        self.service.supprimer_competence_d_un_emploi(emploi_id, nom_comp, self.projet_id)
        self.service.supprimer_du_referentiel_si_orphelin(nom_comp, self.projet_id)

