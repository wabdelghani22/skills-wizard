from services.import_export_service import ImportExportService

class ImportExportController:
    def __init__(self, projet_id):
        self.projet_id = projet_id
        self.service = ImportExportService(projet_id)

    # ---------- EXPORTS ----------

    def exporter_projet_en_excel(self, chemin_fichier):
        """Export Excel complet du projet"""
        self.service.export_to_excel(chemin_fichier)

    def exporter_donnees_json(self, chemin_fichier, donnees: dict):
        """Export de données custom en JSON"""
        self.service.export_to_json(chemin_fichier, donnees)

    # ---------- IMPORTS ----------

    def importer_json(self, chemin_fichier):
        """Importe un JSON brut (retourne un dict à traiter ensuite)"""
        return self.service.import_from_json(chemin_fichier)

    def importer_fiches_metiers_depuis_dossier(self, dossier_path):
        """Importe des textes de fichiers docx dans un dossier"""
        return self.service.import_job_files_from_folder(dossier_path)

    # ---------- UTILITAIRES ----------

    def extraire_texte_docx(self, chemin_fichier):
        """Extrait le texte brut d’un fichier Word"""
        return self.service.extract_text_from_docx(chemin_fichier)
