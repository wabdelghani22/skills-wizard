from db import crud

class CompetenceService:
    def __init__(self, projet_id):
        self.projet_id = projet_id

    # ---------------- REFERENTIEL ----------------

    def get_all_unique_competences(self):
        """Liste toutes les compétences liées au projet."""
        return crud.get_all_competences_by_projet(self.projet_id)
    
    def ajouter_et_associer_competence(self, projet_id, emploi_id, nom, type_, niveau, definition):
        competence_id = crud.get_or_create_competence(projet_id, nom, type_, definition)
        crud.associer_competence_a_emploi(emploi_id, competence_id, niveau)
        return competence_id

    def rechercher_competences_par_prefixe(self, projet_id, prefixe):
        return crud.get_competences_noms_par_prefixe(projet_id, prefixe)

    def add_competence(self, nom, type_competence='hard', dictionnaire=None):
        """Ajoute une compétence au référentiel du projet."""
        crud.add_competence(nom, self.projet_id, type_competence, dictionnaire)

    def delete_competence(self, nom):
        """Supprime une compétence du projet si elle n’est pas utilisée."""
        comp = crud.get_competence_by_name_and_project(nom, self.projet_id)
        if comp:
            crud.delete_competence(comp[0])  # comp[0] = id

    def rename_competence(self, ancien_nom, nouveau_nom):
        """Renomme une compétence dans le projet."""
        crud.rename_competence(ancien_nom, nouveau_nom, self.projet_id)

    def competence_exists(self, nom):
        """Vérifie si une compétence existe déjà dans le projet."""
        competences = self.get_all_unique_competences()
        return any(c[1].lower() == nom.lower() for c in competences)

    def get_dictionnaire_for_competence(self, nom):
        """Retourne la définition et les niveaux d’une compétence dans le dictionnaire."""
        comp = crud.get_competence_by_name_and_project(nom, self.projet_id)
        if not comp:
            return None
        comp_id = comp[0]
        definition = comp[3]  # champ dictionnaire
        niveaux = crud.get_levels_by_competence(comp_id)
        return {
            "definition": definition,
            "niveaux": niveaux
        }

    def update_dictionnaire(self, nom, definition=None, niveaux_dict=None):
        """Modifie la définition et/ou les niveaux associés à une compétence."""
        comp = crud.get_competence_by_name_and_project(nom, self.projet_id)
        if not comp:
            raise ValueError("Compétence non trouvée.")
        comp_id = comp[0]
        if definition:
            crud.update_competence_definition(comp_id, definition)
        if niveaux_dict:
            crud.delete_levels_for_competence(comp_id)
            for niveau, texte in niveaux_dict.items():
                crud.add_level_to_competence(comp_id, niveau, texte)

    # ---------------- PAR EMPLOI ----------------

    def add_competence_to_job(self, nom_competence, nom_metier, niveau=None):
        """Ajoute une compétence à un emploi (et la crée si besoin)."""
        from services.job_service import JobService
        job_service = JobService(self.projet_id)
        emploi_id = job_service.get_job_id_by_title(nom_metier)

        if not emploi_id:
            raise ValueError("Métier introuvable.")

        comp = crud.get_competence_by_name_and_project(nom_competence, self.projet_id)
        if not comp:
            self.add_competence(nom_competence)
            comp = crud.get_competence_by_name_and_project(nom_competence, self.projet_id)

        crud.lier_competence_emploi(emploi_id, comp[0], niveau)

    def get_competences_by_job(self, nom_metier):
        """Liste les compétences d’un métier."""
        from services.job_service import JobService
        job_service = JobService(self.projet_id)
        emploi_id = job_service.get_job_id_by_title(nom_metier)

        return crud.get_competences_by_emploi(emploi_id) if emploi_id else []

    def update_competence_level(self, nom_competence, nom_metier, nouveau_niveau):
        """Modifie le niveau d’une compétence pour un métier."""
        from services.job_service import JobService
        job_service = JobService(self.projet_id)
        emploi_id = job_service.get_job_id_by_title(nom_metier)

        comp = crud.get_competence_by_name_and_project(nom_competence, self.projet_id)
        if emploi_id and comp:
            crud.update_niveau_competence_emploi(emploi_id, comp[0], nouveau_niveau)

    def remove_competence_from_job(self, nom_competence, nom_metier):
        """Supprime une compétence d’un emploi."""
        from services.job_service import JobService
        job_service = JobService(self.projet_id)
        emploi_id = job_service.get_job_id_by_title(nom_metier)

        comp = crud.get_competence_by_name_and_project(nom_competence, self.projet_id)
        if emploi_id and comp:
            crud.delete_competence_from_emploi(emploi_id, comp[0])

    # ---------------- IMPORT / EXPORT ----------------

    def import_competences_from_file(self, filepath):
        """Importer des compétences depuis un fichier CSV ou Excel."""
        import pandas as pd
        try:
            df = pd.read_excel(filepath) if filepath.endswith(".xlsx") else pd.read_csv(filepath)
            for _, row in df.iterrows():
                nom = row.get("nom") or row.get("Nom") or ""
                type_comp = row.get("type", "hard")
                description = row.get("definition") or row.get("Description") or None
                self.add_competence(nom.strip(), type_comp.strip() if type_comp else 'hard', description)
            return True
        except Exception as e:
            print(f"Erreur d'import : {e}")
            return False

    def export_competences_to_file(self, filepath):
        """Exporter les compétences du projet vers un fichier Excel."""
        import pandas as pd
        try:
            competences = crud.get_all_competences_by_projet(self.projet_id)
            data = []
            for c in competences:
                niveaux = crud.get_levels_by_competence(c[0])
                data.append({
                    "id": c[0],
                    "nom": c[1],
                    "type": c[2],
                    "definition": c[3],
                    "niveaux": ", ".join([f"{n['niveau']}: {n['description']}" for n in niveaux])
                })
            df = pd.DataFrame(data)
            df.to_excel(filepath, index=False)
            return True
        except Exception as e:
            print(f"Erreur d'export : {e}")
            return False

    def charger_dictionnaire(self):
        competences = crud.get_all_competences_by_projet(self.projet_id)
        niveaux = crud.get_niveaux_by_projet(self.projet_id)
        dictionnaire = []

        for comp in competences:
            comp_id = comp["id"]
            descriptions = crud.get_descriptions_by_competence(comp_id)
            niveau_map = {desc["niveau_id"]: desc["description"] for desc in descriptions}
            dictionnaire.append({
                "nom": comp["nom"],
                "definition": comp["dictionnaire"],
                "niveaux": niveau_map
            })

        return dictionnaire, niveaux
        
    def sauvegarder_dictionnaire(self, liste_dict, niveaux):
        crud.supprimer_competences_referentiel(self.projet_id)

        for ligne in liste_dict:
            nom = ligne["nom"]
            definition = ligne.get("definition", "")
            crud.add_competence(nom, self.projet_id, description=definition)

            comp = crud.get_competence_by_nom(nom, self.projet_id)
            if not comp:
                continue
            comp_id = comp["id"]

            for niveau in niveaux:
                niveau_id = niveau["id"]
                desc = ligne.get("niveaux", {}).get(niveau_id, "")
                if desc:
                    crud.add_competence_niveau_description(comp_id, niveau_id, desc)
    def sauvegarder_competences_emploi(self, emploi_nom, competences):
        emploi_id = crud.get_id_emploi_par_nom(emploi_nom)
        for c in competences:
            crud.ajouter_ou_mettre_a_jour_competence(
                emploi_id, c["nom"], c["type"], c["niveau_requis"], self.projet_id
            )

    def supprimer_competence_d_un_emploi(self,emploi_id, nom_comp, projet_id):
        crud.supprimer_competence_d_un_emploi(emploi_id, nom_comp, projet_id)

    def supprimer_du_referentiel_si_orphelin(self,nom_comp, projet_id):
        est_orphelin = crud.est_competence_orpheline(nom_comp, projet_id)
        if est_orphelin:
            crud.supprimer_competence_du_referentiel(nom_comp, projet_id)
    def sauvegarder_competences_emploi2(self, emploi_nom, competences):
        from services.job_service import JobService
        job_service = JobService(self.projet_id)
        emploi_id = job_service.get_job_id_by_title(emploi_nom)
        print('dans comp service')
        if not emploi_id:
            raise ValueError("Emploi introuvable")

        for c in competences:
            try:
                print("Debug compétence:", c)  # 👈 ajoute cette ligne
                ancien_nom = str(c.get("ancien_nom", c["nom"])).strip()
                nouveau_nom = str(c["nom"]).strip()
                type_comp = str(c.get("type", "hard")).strip()
                niveau = c.get("niveau_requis")

                comp = crud.get_competence_by_name_and_project(ancien_nom, self.projet_id)

                if comp:
                    comp_id = comp[0]

                    # Si renommage
                    if ancien_nom != nouveau_nom:
                        crud.rename_competence(ancien_nom, nouveau_nom, self.projet_id)

                    # Mise à jour type si changé
                    if type_comp and type_comp != comp[2]:  # comp[2] = type
                        crud.update_competence_type(comp_id, type_comp)
                else:
                    # Compétence nouvelle
                    comp_id = crud.get_or_create_competence(
                        self.projet_id, nouveau_nom, type_comp, None
                    )

                # Lier ou mettre à jour pour l'emploi
                crud.ajouter_ou_mettre_a_jour_competence(
                    emploi_id, nouveau_nom, type_comp, niveau, self.projet_id
                )

            except Exception as e:
                print(f"[ERREUR] Compétence {c} : {e}")


