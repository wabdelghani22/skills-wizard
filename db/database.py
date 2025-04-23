import sqlite3
import os

#DB_PATH = os.path.join(os.path.dirname(__file__), "competence_app.db")
import sys

import sys

def get_db_path():
    """
    Renvoie le chemin vers la base de données dans %APPDATA%\competences_app\competence_app.db
    Créé le dossier s'il n'existe pas.
    """
    if sys.platform.startswith("win"):
        base_dir = os.environ.get("APPDATA", os.path.expanduser("~"))
    else:
        # fallback pour d'autres OS
        base_dir = os.path.expanduser("~")

    db_folder = os.path.join(base_dir, "competences_app")
    os.makedirs(db_folder, exist_ok=True)

    return os.path.join(db_folder, "competence_app.db")

DB_PATH = get_db_path()

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # 👈 pour accéder par nom
    return conn

def init_database():
    conn = get_connection()
    cursor = conn.cursor()

    # --- Projets ---
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS projets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            secteur_activite TEXT NOT NULL,
            type_entreprise TEXT,
            taille TEXT,
            est_international BOOLEAN,
            nb_filiales INTEGER,
            niveau_digitalisation INTEGER,

            -- Paramètres référentiel / fiches
            nb_niveaux INTEGER,
            nb_competences_min INTEGER,
            nb_competences_max INTEGER,
            nb_macro_activites_min INTEGER,
            nb_macro_activites_max INTEGER,
            nb_micro_activites_min INTEGER,
            nb_micro_activites_max INTEGER
        )
    """)


    # --- Hiérarchie métiers ---
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS familles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            projet_id INTEGER,
            FOREIGN KEY (projet_id) REFERENCES projets(id) ON DELETE CASCADE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sous_familles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            famille_id INTEGER,
            FOREIGN KEY (famille_id) REFERENCES familles(id) ON DELETE CASCADE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS emplois (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titre TEXT NOT NULL,
            sous_famille_id INTEGER,
            finalite TEXT,
            FOREIGN KEY (sous_famille_id) REFERENCES sous_familles(id) ON DELETE CASCADE
        )
    """)

    # --- Activités ---
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS macro_activites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            contenu TEXT NOT NULL,
            emploi_id INTEGER,
            FOREIGN KEY (emploi_id) REFERENCES emplois(id) ON DELETE CASCADE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS micro_activites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            contenu TEXT NOT NULL,
            macro_id INTEGER,
            FOREIGN KEY (macro_id) REFERENCES macro_activites(id) ON DELETE CASCADE
        )
    """)

    # --- Niveaux de compétence (par projet) ---
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS niveaux_competence (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            projet_id INTEGER,
            libelle TEXT NOT NULL,
            position INTEGER,
            definition TEXT,
            FOREIGN KEY (projet_id) REFERENCES projets(id) ON DELETE CASCADE
        )
    """)

    # --- Compétences (par projet) ---
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS competences (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            projet_id INTEGER,
            type TEXT CHECK(type IN ('hard', 'soft')) DEFAULT 'hard',
            dictionnaire TEXT DEFAULT NULL,
            FOREIGN KEY (projet_id) REFERENCES projets(id) ON DELETE CASCADE,
            UNIQUE(nom, projet_id)
        )
    """)

    # --- Dictionnaire des compétences : description par niveau ---
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS competence_niveaux_description (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            competence_id INTEGER,
            niveau_id INTEGER,
            description TEXT,
            FOREIGN KEY (competence_id) REFERENCES competences(id) ON DELETE CASCADE,
            FOREIGN KEY (niveau_id) REFERENCES niveaux_competence(id) ON DELETE CASCADE
        )
    """)

    # --- Emploi ↔ Compétence (avec niveau requis) ---
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS emploi_competence (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            emploi_id INTEGER,
            competence_id INTEGER,
            niveau TEXT,
            FOREIGN KEY (emploi_id) REFERENCES emplois(id) ON DELETE CASCADE,
            FOREIGN KEY (competence_id) REFERENCES competences(id) ON DELETE CASCADE
        )
    """)

    # --- Historique prompts IA ---
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS emploi_gpt_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            emploi_id INTEGER,
            prompt TEXT,
            reponse TEXT,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (emploi_id) REFERENCES emplois(id) ON DELETE CASCADE
        )
    """)

    # --- Mapping fichier ↔ emploi ---
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fichier_emploi_mapping (
            fichier_nom TEXT PRIMARY KEY,
            emploi_id INTEGER,
            projet_id INTEGER,
            FOREIGN KEY (emploi_id) REFERENCES emplois(id) ON DELETE CASCADE,
            FOREIGN KEY (projet_id) REFERENCES projets(id) ON DELETE CASCADE
        )
    """)



    # --- Paramètres globaux (prompts, préférences, etc.) ---
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS parametres (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cle TEXT UNIQUE NOT NULL,
            valeur TEXT
        )
    """)

    conn.commit()
    conn.close()
