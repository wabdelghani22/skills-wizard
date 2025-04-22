from dataclasses import dataclass, field
from typing import List, Optional

# --- PHASE 0 : Projet ---

@dataclass
class Projet:
    id: Optional[int]
    nom: str
    secteur_activite: str
    type_entreprise: Optional[str]
    taille: Optional[str]
    est_international: bool
    nb_collaborateurs: Optional[int]
    nb_filiales: Optional[int]


# --- PHASE 1 : Cartographie des emplois ---

@dataclass
class Emploi:
    id: Optional[int]
    titre: str
    sous_famille_id: int

@dataclass
class SousFamille:
    id: Optional[int]
    nom: str
    famille_id: int
    emplois: List[Emploi] = field(default_factory=list)

@dataclass
class Famille:
    id: Optional[int]
    nom: str
    projet_id: int
    sous_familles: List[SousFamille] = field(default_factory=list)


# --- PHASE 2 : Activités & Compétences ---

@dataclass
class MacroActivite:
    id: Optional[int]
    contenu: str
    emploi_id: int
    micro_activites: List["MicroActivite"] = field(default_factory=list)

@dataclass
class MicroActivite:
    id: Optional[int]
    contenu: str
    macro_id: int

@dataclass
class Competence:
    id: Optional[int]
    nom: str
    projet_id: int
    type: str = "hard"  # 'hard' ou 'soft'
    dictionnaire: Optional[str] = None

@dataclass
class EmploiCompetence:
    id: Optional[int]
    emploi_id: int
    competence_id: int
    niveau: Optional[str] = None


# --- PHASE 4 : Dictionnaire des compétences ---

@dataclass
class CompetenceDictionaryEntry:
    id: Optional[int]
    competence_nom: str
    definition: Optional[str]
    exemples: Optional[str]
    domaine: Optional[str]  # exemple : "Technique", "Comportemental", etc.


# --- Optionnel : Export / Import de projet ---

@dataclass
class ProjectMetadata:
    secteur_activite: str
    type_entreprise: Optional[str]
    taille_entreprise: Optional[str]
    national: bool = True
    nb_collaborateurs: Optional[int] = None
    nb_filiales: Optional[int] = None
