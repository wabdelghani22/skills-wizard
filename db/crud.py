from db.database import get_connection

# --- 🔹 PROJETS ---
def create_projet(nom, secteur, type_entreprise=None, taille=None, international=False,
                filiales=None, niveau_digitalisation=None,
                  nb_niveaux=None, nb_comp_min=None, nb_comp_max=None,
                  nb_macro_min=None, nb_macro_max=None,
                  nb_micro_min=None, nb_micro_max=None):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO projets (
            nom, secteur_activite, type_entreprise, taille,
            est_international, nb_filiales, niveau_digitalisation,
            nb_niveaux, nb_competences_min, nb_competences_max,
            nb_macro_activites_min, nb_macro_activites_max,
            nb_micro_activites_min, nb_micro_activites_max
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        nom, secteur, type_entreprise, taille,
        international, filiales, niveau_digitalisation,
        nb_niveaux, nb_comp_min, nb_comp_max,
        nb_macro_min, nb_macro_max,
        nb_micro_min, nb_micro_max
    ))
    conn.commit()
    conn.close()
def get_or_create_competence(projet_id, nom, type_, definition=None):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id FROM competences WHERE projet_id = ? AND nom = ?", (projet_id, nom))
    row = cur.fetchone()

    if row:
        return row["id"]

    cur.execute("""
        INSERT INTO competences (nom, projet_id, type, dictionnaire)
        VALUES (?, ?, ?, ?)
    """, (nom, projet_id, type_, definition))
    conn.commit()
    return cur.lastrowid

def associer_competence_a_emploi(emploi_id, competence_id, niveau):
    conn = get_connection()
    cur = conn.cursor()

    # Vérifie si le lien existe déjà
    cur.execute("""
        SELECT id FROM emploi_competence
        WHERE emploi_id = ? AND competence_id = ?
    """, (emploi_id, competence_id))

    if not cur.fetchone():
        cur.execute("""
            INSERT INTO emploi_competence (emploi_id, competence_id, niveau)
            VALUES (?, ?, ?)
        """, (emploi_id, competence_id, niveau))
        conn.commit()

def update_projet_parametres(projet_id, **params):
    conn = get_connection()
    cur = conn.cursor()
    for cle, val in params.items():
        cur.execute(f"UPDATE projets SET {cle} = ? WHERE id = ?", (val, projet_id))
    conn.commit()
    conn.close()

def get_projet_by_idD(projet_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM projets WHERE id = ?", (projet_id,))
    row = cur.fetchone()
    conn.close()

    if row:
        columns = [desc[0] for desc in cur.description]
        return dict(zip(columns, row))
    return None

def get_projet_by_id(projet_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM projets WHERE id = ?", (projet_id,))
    projet = cur.fetchone()
    conn.close()
    return projet


def get_all_projets():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM projets")
    projets = cur.fetchall()
    conn.close()
    return projets

# --- 🔹 FAMILLES / SOUS-FAMILLES / EMPLOIS ---
def add_famille(nom, projet_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO familles (nom, projet_id) VALUES (?, ?)", (nom, projet_id))
    conn.commit()
    fam_id = cur.lastrowid
    conn.close()
    return fam_id  # ✅

def get_famille_by_nom(nom, projet_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM familles WHERE nom = ? AND projet_id = ?", (nom, projet_id))
    row = cur.fetchone()
    conn.close()
    return dict(zip([col[0] for col in cur.description], row)) if row else None

def ajouter_famille(nom, projet_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO familles (nom, projet_id) VALUES (?, ?)", (nom, projet_id))
    famille_id = cur.lastrowid
    conn.commit()
    conn.close()
    return famille_id

def get_sous_famille_by_nom(nom, famille_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM sous_familles WHERE nom = ? AND famille_id = ?", (nom, famille_id))
    row = cur.fetchone()
    conn.close()
    return dict(zip([col[0] for col in cur.description], row)) if row else None

def get_competences_noms_par_prefixe(projet_id, prefixe):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT nom FROM competences 
        WHERE projet_id = ? AND nom LIKE ?
        LIMIT 20
    """, (projet_id, f"{prefixe}%"))
    return [row["nom"] for row in cur.fetchall()]

def ajouter_sous_famille(nom, famille_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO sous_familles (nom, famille_id) VALUES (?, ?)", (nom, famille_id))
    sf_id = cur.lastrowid
    conn.commit()
    conn.close()
    return sf_id

def ajouter_emploi(titre, sous_famille_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO emplois (titre, sous_famille_id) VALUES (?, ?)", (titre, sous_famille_id))
    conn.commit()
    conn.close()

def get_familles_by_projet(projet_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM familles WHERE projet_id = ?", (projet_id,))
    return cur.fetchall()

def add_sous_famille(nom, famille_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO sous_familles (nom, famille_id) VALUES (?, ?)", (nom, famille_id))
    conn.commit()
    sf_id = cur.lastrowid
    conn.close()
    return sf_id  # ✅


def get_sous_familles_by_famille(famille_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM sous_familles WHERE famille_id = ?", (famille_id,))
    return cur.fetchall()

def add_emploi(titre, sous_famille_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO emplois (titre, sous_famille_id) VALUES (?, ?)", (titre, sous_famille_id))
    conn.commit()
    emploi_id = cur.lastrowid
    conn.close()
    return emploi_id  # ✅

def get_emplois_by_sous_famille(sous_famille_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM emplois WHERE sous_famille_id = ?", (sous_famille_id,))
    return cur.fetchall()

def get_sous_familles(projet_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT sf.nom
        FROM sous_familles sf
        JOIN familles f ON sf.id = f.id
        WHERE f.projet_id = ?
    """, (projet_id,))
    rows = cur.fetchall()
    return [row[0] for row in rows]  # Juste les noms

def supprimer_hierarchie_by_projet(projet_id):
    conn = get_connection()
    cur = conn.cursor()

    # Suppression dans l'ordre inverse de dépendance (enfants -> parents)
    cur.execute("""
        DELETE FROM emplois WHERE sous_famille_id IN (
            SELECT id FROM sous_familles WHERE famille_id IN (
                SELECT id FROM familles WHERE projet_id = ?
            )
        )
    """, (projet_id,))
    
    cur.execute("""
        DELETE FROM sous_familles WHERE famille_id IN (
            SELECT id FROM familles WHERE projet_id = ?
        )
    """, (projet_id,))
    
    cur.execute("DELETE FROM familles WHERE projet_id = ?", (projet_id,))
    
    conn.commit()
    conn.close()

# --- 🔹 ACTIVITÉS ---
def add_macro_activite(emploi_id, contenu):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO macro_activites (contenu, emploi_id) VALUES (?, ?)", (contenu, emploi_id))
    conn.commit()
    conn.close()

def add_micro_activite(macro_id, contenu):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO micro_activites (contenu, macro_id) VALUES (?, ?)", (contenu, macro_id))
    conn.commit()
    conn.close()

def get_macro_activites_by_emploi(emploi_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM macro_activites WHERE emploi_id = ?", (emploi_id,))
    return cur.fetchall()

def get_micro_activites_by_macro(macro_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM micro_activites WHERE macro_id = ?", (macro_id,))
    return cur.fetchall()

# --- 🔹 NIVEAUX DE COMPÉTENCE ---
def add_niveau(projet_id, libelle, position):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO niveaux_competence (projet_id, libelle, position) VALUES (?, ?, ?)", (projet_id, libelle, position))
    conn.commit()
    conn.close()

def get_niveaux_by_projet(projet_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM niveaux_competence WHERE projet_id = ? ORDER BY position ASC", (projet_id,))
    result = cur.fetchall()
    conn.close()
    return [dict(r) for r in result]  # ✅


# --- 🔹 COMPÉTENCES (avec dictionnaire) ---
def add_competence(nom, projet_id, type_competence='hard', description=None):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT OR IGNORE INTO competences (nom, projet_id, type, dictionnaire)
        VALUES (?, ?, ?, ?)
    """, (nom, projet_id, type_competence, description))
    conn.commit()
    conn.close()

def update_competence_description(competence_id, description):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE competences SET dictionnaire = ? WHERE id = ?", (description, competence_id))
    conn.commit()
    conn.close()

def get_all_competences_by_projet(projet_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM competences WHERE projet_id = ? ORDER BY nom ASC", (projet_id,))
    result = cur.fetchall()
    conn.close()
    return [dict(row) for row in result]  # ✅ ceci transforme sqlite3.Row en dict


def delete_competence(competence_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM competences WHERE id = ?", (competence_id,))
    conn.commit()
    conn.close()

# --- 🔹 DÉFINITIONS PAR NIVEAU POUR UNE COMPÉTENCE ---
def add_competence_niveau_description(competence_id, niveau_id, description):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO competence_niveaux_description (competence_id, niveau_id, description)
        VALUES (?, ?, ?)
    """, (competence_id, niveau_id, description))
    conn.commit()
    conn.close()


def get_descriptions_by_competence(competence_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT niveau_id, description
        FROM competence_niveaux_description
        WHERE competence_id = ?
    """, (competence_id,))
    result = cur.fetchall()
    conn.close()
    return [dict(r) for r in result]  # 👈 nécessaire


# --- 🔹 EMPLOI ↔ COMPÉTENCES ---
def lier_competence_emploi(emploi_id, competence_id, niveau=None):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO emploi_competence (emploi_id, competence_id, niveau)
        VALUES (?, ?, ?)
    """, (emploi_id, competence_id, niveau))
    conn.commit()
    conn.close()

def get_competences_by_emploi(emploi_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT c.nom, ec.niveau, c.type
        FROM emploi_competence ec
        JOIN competences c ON c.id = ec.competence_id
        WHERE ec.emploi_id = ?
    """, (emploi_id,))
    return cur.fetchall()


# --- 🔹 PROMPTS GPT HISTORY ---
def save_prompt_history(emploi_id, prompt, reponse):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO emploi_gpt_history (emploi_id, prompt, reponse)
        VALUES (?, ?, ?)
    """, (emploi_id, prompt, reponse))
    conn.commit()
    conn.close()

def get_prompt_history(emploi_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM emploi_gpt_history WHERE emploi_id = ?", (emploi_id,))
    return cur.fetchall()

# --- 🔹 PARAMÈTRES GLOBAUX ---
def set_parametre(cle, valeur):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT OR REPLACE INTO parametres (cle, valeur) VALUES (?, ?)", (cle, valeur))
    conn.commit()
    conn.close()

def get_parametre(cle):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT valeur FROM parametres WHERE cle = ?", (cle,))
    result = cur.fetchone()
    return result[0] if result else None


def get_prompt_by_code(code):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT contenu FROM prompts WHERE code = ?", (code,))
    row = cur.fetchone()
    return row[0] if row else ""
def ajouter_competence_referentiel(projet_id, nom):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO competences (projet_id, nom) VALUES (?, ?)",
        (projet_id, nom.strip())
    )
    conn.commit()
    conn.close()

def supprimer_competences_referentiel(projet_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM competences WHERE projet_id = ?", (projet_id,))
    conn.commit()
    conn.close()

def get_referentiel_competences_by_projet(projet_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT nom FROM competences WHERE projet_id = ?", (projet_id,))
    result = [row[0] for row in cur.fetchall()]
    conn.close()
    return result


def get_definition_niveau(niveau_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT definition FROM niveaux_competence WHERE id = ?", (niveau_id,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else ""

def update_niveau_definition(niveau_id, definition):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE niveaux_competence SET definition = ? WHERE id = ?", (definition, niveau_id))
    conn.commit()
    conn.close()

def get_competence_by_nom(nom, projet_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM competences WHERE nom = ? AND projet_id = ?", (nom, projet_id))
    row = cur.fetchone()
    conn.close()
    if row:
        columns = [desc[0] for desc in cur.description]
        return dict(zip(columns, row))
    return None


def get_competences_par_sous_famille(sous_famille_nom):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT 
            e.id AS emploi_id,
            e.titre AS emploi_titre,
            c.nom AS competence_nom,
            ec.niveau AS niveau
        FROM sous_familles sf
        JOIN emplois e ON e.sous_famille_id = sf.id
        LEFT JOIN emploi_competence ec ON ec.emploi_id = e.id
        LEFT JOIN competences c ON c.id = ec.competence_id
        WHERE sf.nom = ?
        ORDER BY c.nom, e.titre
    """, (sous_famille_nom,))
    rows = cur.fetchall()
    return rows
def get_id_emploi_par_nom(nom):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM emplois WHERE titre = ?", (nom,))
    row = cur.fetchone()
    conn.close()
    if row:
        return row["id"]
    else:
        return None

def ajouter_ou_mettre_a_jour_competence2(emploi_id, nom, type_, niveau, projet_id):
    conn = get_connection()
    cur = conn.cursor()
    print('emploi_id',emploi_id)
    print('nom',nom)
    print('type_',type_)
    print('niveau',niveau)
    print('projet_id',projet_id)
    # Vérifier si la compétence existe déjà
    cur.execute("SELECT id FROM competences WHERE nom = ? AND projet_id = ?", (nom, projet_id))
    row = cur.fetchone()
    
    if row:
        print('row["id"]',row["id"])
        #print('competence_id',competence_id)
        print('row',row)
        competence_id = row["id"]
        print('existe deja)')
    else:
        print('n existe pas)')
        cur.execute("INSERT INTO competences (nom, type, projet_id) VALUES (?, ?, ?)", (nom, type_, projet_id))
        competence_id = cur.lastrowid

    # Lier compétence à l'emploi
    cur.execute("""
        INSERT OR REPLACE INTO emploi_competence (emploi_id, competence_id, niveau)
        VALUES (?, ?, ?)
    """, (emploi_id, competence_id, str(niveau)))

    conn.commit()
    conn.close()

def set_finalite_emploi(emploi_id, finalite):
    conn = get_connection()
    conn.execute("UPDATE emplois SET finalite = ? WHERE id = ?", (finalite, emploi_id))
    conn.commit()
    conn.close()

def get_finalite_by_emploi(emploi_id):
    conn = get_connection()
    cur = conn.execute("SELECT finalite FROM emplois WHERE id = ?", (emploi_id,))
    row = cur.fetchone()
    conn.close()
    return row["finalite"] if row else ""

def get_emploi_by_id(emploi_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM emplois WHERE id = ?", (emploi_id,))
    row = cur.fetchone()
    conn.close()

    if row:
        columns = [desc[0] for desc in cur.description]
        return dict(zip(columns, row))
    return None


def supprimer_activites_pour_emploi(emploi_id):
    conn = get_connection()
    conn.execute("DELETE FROM micro_activites WHERE macro_id IN (SELECT id FROM macro_activites WHERE emploi_id = ?)", (emploi_id,))
    conn.execute("DELETE FROM macro_activites WHERE emploi_id = ?", (emploi_id,))
    conn.commit()
    conn.close()

def ajouter_macro_activite2(emploi_id, titre):
    conn = get_connection()
    cur = conn.execute("INSERT INTO macro_activites (emploi_id, titre) VALUES (?, ?)", (emploi_id, titre))
    conn.commit()
    last_id = cur.lastrowid
    conn.close()
    return last_id

def ajouter_macro_activite(emploi_id, contenu):
    conn = get_connection()  # Obtenez la connexion à la base de données
    cur = conn.cursor()
    cur.execute("INSERT INTO macro_activites (emploi_id, contenu) VALUES (?, ?)", (emploi_id, contenu))
    conn.commit()
    return cur.lastrowid  # Retourne l'ID de la macro-activité insérée


def ajouter_micro_activite2(macro_id, texte):
    conn = get_connection()
    conn.execute("INSERT INTO micro_activites (macro_id, texte) VALUES (?, ?)", (macro_id, texte))
    conn.commit()
    conn.close()
def ajouter_micro_activite(macro_id, contenu):
    conn = get_connection()
    conn.execute("INSERT INTO micro_activites (macro_id, contenu) VALUES (?, ?)", (macro_id, contenu))
    conn.commit()
    conn.close()

def get_emploi_ids_avec_competences_by_projet(projet_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT DISTINCT emploi_id
        FROM emploi_competence
        INNER JOIN emplois ON emplois.id = emploi_competence.emploi_id
        INNER JOIN sous_familles ON sous_familles.id = emplois.sous_famille_id
        INNER JOIN familles ON familles.id = sous_familles.famille_id
        WHERE familles.projet_id = ?
    """, (projet_id,))
    rows = cur.fetchall()
    conn.close()
    return [row["emploi_id"] for row in rows]

def get_fichiers_traites():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT nom_fichier FROM fichiers_traites")
    fichiers = cur.fetchall()
    conn.close()
    return [f["nom_fichier"] for f in fichiers]

def get_fichiers_deja_traite(projet_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT fichier_nom FROM fichier_emploi_mapping WHERE projet_id = ?
    """, (projet_id,))
    result = [row[0] for row in cur.fetchall()]
    conn.close()
    return result

def marquer_fichier_comme_traite(fichier_nom, emploi_id, projet_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT OR REPLACE INTO fichier_emploi_mapping (fichier_nom, emploi_id, projet_id)
        VALUES (?, ?, ?)
    """, (fichier_nom, emploi_id, projet_id))
    conn.commit()
    conn.close()

def supprimer_competence_d_un_emploi(emploi_id, nom_comp, projet_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM emploi_competence
        WHERE emploi_id = ? AND competence_id IN (
            SELECT id FROM competences WHERE nom = ? AND projet_id = ?
        )
    """, (emploi_id, nom_comp, projet_id))
    conn.commit()
    conn.close()

def est_competence_orpheline(nom_comp, projet_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT COUNT(*) FROM emploi_competence
        WHERE competence_id IN (
            SELECT id FROM competences WHERE nom = ? AND projet_id = ?
        )
    """, (nom_comp, projet_id))
    count = cursor.fetchone()[0]
    conn.close()
    return count == 0

def supprimer_competence_du_referentiel(nom_comp, projet_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM competences
        WHERE nom = ? AND projet_id = ?
    """, (nom_comp, projet_id))
    conn.commit()
    conn.close()
def update_competence_type(competence_id, nouveau_type):
    conn = get_connection()
    cursor = conn.cursor()
    req = "UPDATE competence SET type = ? WHERE id = ?"
    cursor.execute(req, (nouveau_type, competence_id))
    conn.commit()

def ajouter_ou_mettre_a_jour_competence(emploi_id, nom_comp, type_comp, niveau, projet_id):
    print(f"[DEBUG]####### Liaison compétence {nom_comp} à emploi {emploi_id} pour projet {projet_id}")
    try:
        comp_id = get_or_create_competence(projet_id, nom_comp, type_comp)
        if not comp_id:
            print(f"[ERREUR] Compétence non trouvée ou non créée : {nom_comp}")
            return

        conn = get_connection()
        cursor = conn.cursor()

        req_check = """
            SELECT 1 FROM emploi_competence
            WHERE emploi_id = ? AND competence_id = ?
        """
        cursor.execute(req_check, (emploi_id, comp_id))
        existe = cursor.fetchone()

        niveau_str = str(niveau)

        if existe:
            print(f"🔄 Mise à jour : {nom_comp} (niveau {niveau_str})")
            req_update = """
                UPDATE emploi_competence
                SET niveau = ?
                WHERE emploi_id = ? AND competence_id = ?
            """
            cursor.execute(req_update, (niveau_str, emploi_id, comp_id))
        else:
            print(f"➕ Nouvelle compétence liée : {nom_comp} (niveau {niveau_str})")
            req_insert = """
                INSERT INTO emploi_competence (emploi_id, competence_id, niveau)
                VALUES (?, ?, ?)
            """
            cursor.execute(req_insert, (emploi_id, comp_id, niveau_str))

        conn.commit()
    except Exception as e:
        print(f"[ERREUR] ajout/maj compétence '{nom_comp}' : {e}")


def ajouter_ou_mettre_a_jour_competence22(emploi_id, nom_comp, type_comp, niveau, projet_id):
    # Vérifie ou crée la compétence dans le référentiel
    comp_id = get_or_create_competence(projet_id, nom_comp, type_comp)
    conn = get_connection()
    cursor = conn.cursor()
    # Vérifie si elle est déjà liée à l'emploi
    req_check = """
        SELECT 1 FROM emploi_competence
        WHERE emploi_id = ? AND competence_id = ?
    """
    cursor.execute(req_check, (emploi_id, comp_id))
    existe = cursor.fetchone()

    if existe:
        # Mise à jour du niveau si déjà existante
        req_update = """
            UPDATE emploi_competence
            SET niveau = ?
            WHERE emploi_id = ? AND competence_id = ?
        """
        cursor.execute(req_update, (niveau, emploi_id, comp_id))
    else:
        # Ajout si nouvelle association
        req_insert = """
            INSERT INTO emploi_competence (emploi_id, competence_id, niveau)
            VALUES (?, ?, ?)
        """
        cursor.execute(req_insert, (emploi_id, comp_id, niveau))

    conn.commit()
def update_niveau_tous_emplois(competence_id, nouveau_niveau):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE emploi_competence
        SET niveau = ?
        WHERE competence_id = ?
    """, (nouveau_niveau, competence_id))
    conn.commit()
    conn.close()












