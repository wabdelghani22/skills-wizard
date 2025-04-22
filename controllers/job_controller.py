from services.job_service import JobService
from db import crud

class JobController:
    def __init__(self, projet_id):
        self.service = JobService(projet_id)

    # ----------- HIERARCHIE -----------

    def get_hierarchie_emplois(self):
        """Retourne la hiérarchie complète pour affichage/arbre."""
        return self.service.get_full_hierarchy()
    
    def recuperer_hierarchie_as_json(self):
        return self.service.get_cartographie_as_json()
    
  

    def get_hierarchie_as_dict(self):
        """Retourne la hiérarchie sous forme de dictionnaire (ex: pour export JSON)."""
        return self.service.export_hierarchy_as_dict()

    def ajouter_famille(self, nom):
        """Ajoute une famille de métier."""
        self.service.add_famille(nom)

    def ajouter_sous_famille(self, nom, famille_id):
        """Ajoute une sous-famille à une famille existante."""
        self.service.add_sous_famille(nom, famille_id)

    def ajouter_emploi(self, titre, sous_famille_id):
        """Ajoute un emploi à une sous-famille donnée."""
        self.service.add_emploi(titre, sous_famille_id)

    # controllers/job_controller.py

    def ajouter_emploi_si_nouveau(self, titre, famille, sous_famille):
        self.service.ajouter_emploi_complet_si_nouveau(titre, famille, sous_famille)


    # ----------- MÉTIERS -----------

    def get_liste_emplois(self):
        """Retourne tous les emplois du projet (flat + rattachement)."""
        return self.service.get_emplois_flat()

    def emploi_existe(self, titre):
        """Vérifie si un emploi existe déjà (utile à la création/import)."""
        return self.service.emploi_existe(titre)

    def get_emploi_par_nom(self, nom):
        """Retourne un emploi complet à partir de son nom."""
        return self.service.get_emploi_by_nom(nom)

    def get_id_emploi(self, titre):
        """Retourne l’ID d’un emploi à partir de son titre."""
        return self.service.get_job_id_by_title(titre)

    def sauvegarder_hierarchie_depuis_json(self, data, projet_id):
        crud.supprimer_hierarchie_by_projet(projet_id)
        service = JobService(projet_id)

        for famille in data.get("familles", []):
            fam_id = service.add_famille(famille["nom"])
            for sf in famille.get("sous_familles", []):
                sf_id = service.add_sous_famille(sf["nom"], fam_id)
                for emploi in sf.get("emplois", []):
                    service.add_emploi(emploi, sf_id)

    def get_all_sous_familles(self):
        return self.service.get_all_sous_familles()

    def get_competence_table_for_sous_famille(self, sous_famille_nom):
        return self.service.get_competences_table_for_sous_famille(sous_famille_nom)



