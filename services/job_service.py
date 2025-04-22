from db import crud

class JobService:
    def __init__(self, projet_id):
        self.projet_id = projet_id

    # -------------------- HIERARCHIE -------------------- #

    def get_full_hierarchy(self):
        """Retourne la hiérarchie complète: Familles → Sous-familles → Emplois pour ce projet."""
        hierarchy = []
        familles = crud.get_familles_by_projet(self.projet_id)

        for fam in familles:
            #famille_id, famille_nom = fam
            famille_id = fam["id"]
            famille_nom = fam["nom"]

            sous_familles = crud.get_sous_familles_by_famille(famille_id)
            sf_list = []

            for sf in sous_familles:
                #sf_id, sf_nom = sf
                sf_id = sf["id"]
                sf_nom = sf["nom"]
                emplois = crud.get_emplois_by_sous_famille(sf_id)
                emploi_list = [{"id": e[0], "titre": e[1]} for e in emplois]
                sf_list.append({"id": sf_id, "nom": sf_nom, "emplois": emploi_list})

            hierarchy.append({
                "id": famille_id,
                "nom": famille_nom,
                "sous_familles": sf_list
            })

        return hierarchy
    def get_cartographie_as_json(self):
        familles = crud.get_familles_by_projet(self.projet_id)
        data = []

        for fam in familles:
            fam_id, fam_nom = fam[0], fam[1]  # ✅ sécurité

            sous_familles = []
            for sf in crud.get_sous_familles_by_famille(fam_id):
                sf_id, sf_nom = sf[0], sf[1]

                emplois_raw = crud.get_emplois_by_sous_famille(sf_id)
                emplois = [e[1] for e in emplois_raw]  # e = (id, titre)

                sous_familles.append({
                    "nom": sf_nom,
                    "emplois": emplois
                })

            data.append({
                "nom": fam_nom,
                "sous_familles": sous_familles  # ✅ underscore (pas tiret)
            })

        return {"familles": data}


    def export_hierarchy_as_dict(self):
        """Renvoie la hiérarchie complète sous forme d’un dictionnaire (pour export ou UI)."""
        return self.get_full_hierarchy()

    # services/job_service.py

    def ajouter_emploi_complet_si_nouveau(self, titre, famille, sous_famille):
        # Vérifie si la famille existe
        famille_obj = crud.get_famille_by_nom(famille, self.projet_id)
        if not famille_obj:
            famille_id = crud.ajouter_famille(famille, self.projet_id)
        else:
            famille_id = famille_obj["id"]

        # Vérifie si la sous-famille existe
        sf_obj = crud.get_sous_famille_by_nom(sous_famille, famille_id)
        if not sf_obj:
            sous_famille_id = crud.ajouter_sous_famille(sous_famille, famille_id)
        else:
            sous_famille_id = sf_obj["id"]

        # Vérifie si l’emploi existe
        emploi_existants = crud.get_emplois_by_sous_famille(sous_famille_id)
        titres_existants = [e[1] for e in emploi_existants]
        if titre not in titres_existants:
            crud.ajouter_emploi(titre, sous_famille_id)


    def add_famille(self, nom):
        return crud.add_famille(nom, self.projet_id)

    def add_sous_famille(self, nom, famille_id):
        return crud.add_sous_famille(nom, famille_id)

    def add_emploi(self, titre, sous_famille_id):
        return crud.add_emploi(titre, sous_famille_id)
    # Service : Récupère un emploi par son ID
    def get_emploi_par_id(emploi_id):
        return get_emploi_by_id(emploi_id)


    # -------------------- MÉTIERS -------------------- #

    def get_emplois_flat(self):
        """Retourne tous les emplois du projet avec leur rattachement (id, titre, famille, sous-famille)."""
        emplois = []
        familles = crud.get_familles_by_projet(self.projet_id)
        for fam in familles:
            #famille_id, famille_nom = fam
            famille_id = fam[0]
            famille_nom = fam[1]
            sous_familles = crud.get_sous_familles_by_famille(famille_id)
            for sf in sous_familles:
                sf_id = sf[0]
                sf_nom = sf[1]
                emps = crud.get_emplois_by_sous_famille(sf_id)
                for emp in emps:
                    emplois.append({
                        "id": emp[0],
                        "titre": emp[1],
                        "sous_famille": sf_nom,
                        "famille": famille_nom
                    })
        return emplois

    def emploi_existe(self, titre):
        """Vérifie si un emploi existe déjà dans le projet."""
        all_emplois = self.get_emplois_flat()
        return any(e["titre"].strip().lower() == titre.strip().lower() for e in all_emplois)

    def get_emploi_by_nom(self, nom):
        """Retourne les infos d’un emploi à partir de son nom."""
        emplois = self.get_emplois_flat()
        for e in emplois:
            if e["titre"].strip().lower() == nom.strip().lower():
                return e
        return None

    def get_job_id_by_title(self, titre):
        """Retourne l’ID d’un emploi à partir de son titre (utilisé dans les liaisons)."""
        emploi = self.get_emploi_by_nom(titre)
        print('emploi', emploi)
        return emploi["id"] if emploi else None

    def get_all_sous_familles(self):
        return crud.get_sous_familles(self.projet_id)

    def get_competences_table_for_sous_famille(self, sous_famille_nom):
        return crud.get_competences_par_sous_famille(sous_famille_nom)


