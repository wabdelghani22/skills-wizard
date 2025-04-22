from db import crud

class ReferentielService:
    def __init__(self, projet_id):
        self.projet_id = projet_id

    def enregistrer_competences(self, competences: list[str]):
        crud.supprimer_competences_referentiel(self.projet_id)
        for nom in competences:
            crud.ajouter_competence_referentiel(self.projet_id, nom)

    def charger_competences(self):
        return crud.get_referentiel_competences_by_projet(self.projet_id)

    def fusionner_competences(self, liste, nouvelles_valeurs):
        """
        Permet de remplacer plusieurs compétences par une nouvelle (fusion).
        """
        cleaned = [c for c in liste if c and c.strip()]
        return cleaned + nouvelles_valeurs

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

    def sauvegarder_competences_emploivv(self, emploi_nom, competences):
        emploi_id = crud.get_id_emploi_par_nom(emploi_nom)
        #print(f"[DEBUG] Liaison compétence {nom_comp} à emploi {emploi_id} pour projet {projet_id}")
        for c in competences:
            crud.ajouter_ou_mettre_a_jour_competence(
                emploi_id, c["nom"], c["type"], c["niveau_requis"], self.projet_id
            )
    def sauvegarder_competences_emploi(self, emploi_nom, competences):
        print(">>> Début sauvegarde")
        emploi_id = crud.get_id_emploi_par_nom(emploi_nom)
        print("emploi_id =", emploi_id)
        if not emploi_id:
            print(f"❌ Aucun emploi trouvé pour '{emploi_nom}' — rien sauvegardé")
            return

        for c in competences:
            print("Ajout ou MAJ :", c)
            crud.ajouter_ou_mettre_a_jour_competence(emploi_id, c["nom"], c["type"], c["niveau_requis"], self.projet_id)

        print(f"✅ Sauvegarde terminée pour : {emploi_nom} ({len(competences)} compétences)")

    def ajouter_et_associer_competence(self, projet_id, emploi_id, nom, type_, niveau, definition):
        competence_id = crud.get_or_create_competence(projet_id, nom, type_, definition)
        crud.associer_competence_a_emploi(emploi_id, competence_id, niveau)
        return competence_id

    def rechercher_competences_par_prefixe(self, projet_id, prefixe):
        return crud.get_competences_noms_par_prefixe(projet_id, prefixe)

    def get_emploi_ids_avec_competences(self):
        return crud.get_emploi_ids_avec_competences_by_projet(self.projet_id)


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



    def supprimer_competence_d_un_emploi(self,emploi_id, nom_comp, projet_id):
        crud.supprimer_competence_d_un_emploi(emploi_id, nom_comp, projet_id)

    def supprimer_du_referentiel_si_orphelin(self,nom_comp, projet_id):
        est_orphelin = crud.est_competence_orpheline(nom_comp, projet_id)
        if est_orphelin:
            crud.supprimer_competence_du_referentiel(nom_comp, projet_id)
    
    def sauvegarder_competences_emploi2(self, emploi_nom, competences):
        print('dans service')
        from services.job_service import JobService
        print('self.projet_id',self.projet_id)
        job_service = JobService(self.projet_id)
        print('dans service2', emploi_nom)
        emploi_id = int(emploi_nom)
        print('dans service')
        if not emploi_id:
            raise ValueError("Emploi introuvable")
        print('competences',competences) 
        for c in competences:
            try:
                print("Debug compétence:", c)  # 👈 ajoute cette ligne
                ancien_nom = str(c.get("ancien_nom", c["nom"])).strip()
                nouveau_nom = str(c["nom"]).strip()
                type_comp = str(c.get("type", "hard")).strip()
                niveau = int(c.get("niveau_requis", 1))  # ← force en entier

                comp = crud.get_competence_by_nom(ancien_nom, self.projet_id)
                print('comp crud',comp)
                if comp:
                    comp_id = comp["id"]
                    print('id comp',comp_id)
                    # Si renommage
                    print('ancien nim',ancien_nom)
                    print('nouveau_nom ',nouveau_nom)
                    if ancien_nom != nouveau_nom:
                        crud.rename_competence(ancien_nom, nouveau_nom, self.projet_id)

                    # Mise à jour type si changé
                    if type_comp and type_comp != comp["type"]:  # comp[2] = type
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


    def modifier_competence_globale(self, ancien_nom, nouveau_nom, niveau, type_):
        comp = crud.get_competence_by_nom(ancien_nom, self.projet_id)
        if not comp:
            raise ValueError("Compétence introuvable")

        comp_id = comp["id"]

        if ancien_nom != nouveau_nom:
            crud.rename_competence(ancien_nom, nouveau_nom, self.projet_id)

        if type_ != comp["type"]:
            crud.update_competence_type(comp_id, type_)

        crud.update_niveau_tous_emplois(comp_id, niveau)
