from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QComboBox, QLineEdit, QHBoxLayout, QPushButton,
    QSpinBox, QCheckBox, QTableWidget, QTableWidgetItem, QHeaderView,
    QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QColor
import json  # ✅ nécessaire pour traiter la réponse IA

class DialogGenerationCompetencesParEmploi(QDialog):
    def __init__(self, titre_fichier, contenu_fichier, emplois_existants, suggestions_ia=None,
                 openai_controller=None, prompt_builder=None, json_extractor=None,
                 nb_niveaux=5, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Génération de compétences")
        self.resize(500, 600)

        self.titre_fichier = titre_fichier
        self.contenu_fichier = contenu_fichier
        self.emplois_existants = emplois_existants
        self.suggestions = suggestions_ia or []
        self.nb_niveaux = nb_niveaux
        self.emploi_selectionne = None
        self.competences = []

        # 🔗 External dependencies
        self.openai_controller = openai_controller
        self.prompt_builder = prompt_builder
        self.json_extractor = json_extractor

        self.layout = QVBoxLayout(self)

        # 🔹 Contexte : nom du fichier et suggestions IA
        if self.contenu_fichier:
            self.label_fichier = QLabel(f"<b>Nom de l'emploi extrait du fichier :</b> {self.titre_fichier}")
            self.layout.addWidget(self.label_fichier)

            self.layout.addWidget(QLabel("Suggestions IA pour associer un emploi :"))
            self.combo_emploi = QComboBox()
            for s in self.suggestions:
                label = f"{s['titre']} ({s['famille']} / {s['sous_famille']})"
                self.combo_emploi.addItem(label, s)
            self.combo_emploi.addItem("Autre emploi existant...")
            self.combo_emploi.addItem("Créer un nouvel emploi...")
            self.combo_emploi.currentIndexChanged.connect(self.toggle_inputs)
            self.layout.addWidget(self.combo_emploi)

            self.combo_autre = QComboBox()
            for emp in self.emplois_existants:
                self.combo_autre.addItem(f"{emp['titre']} ({emp.get('famille', '')}/{emp.get('sous_famille', '')})", emp)
            self.combo_autre.setVisible(False)
            self.layout.addWidget(self.combo_autre)

            self.input_titre = QLineEdit()
            self.input_famille = QLineEdit()
            self.input_sous_famille = QLineEdit()
            self.input_titre.setPlaceholderText("Nom de l'emploi")
            self.input_famille.setPlaceholderText("Famille")
            self.input_sous_famille.setPlaceholderText("Sous-famille")
            for widget in (self.input_titre, self.input_famille, self.input_sous_famille):
                widget.setVisible(False)
                self.layout.addWidget(widget)
        else:
            # 🔸 Affichage direct de l'arborescence si pas de fichier
            emploi = next((emp for emp in self.emplois_existants if emp["titre"] == self.titre_fichier), None)
            if emploi:
                famille = emploi.get("famille", "?")
                sous_famille = emploi.get("sous_famille", "?")
                label_info = QLabel(f"<b>Emploi sélectionné :</b><br>Famille : {famille}<br>Sous-famille : {sous_famille}<br>Emploi : {emploi['titre']}")
                label_info.setTextFormat(Qt.RichText)
                self.layout.addWidget(label_info)
        self.layout.addWidget(QLabel("<b>Paramètres :</b>"))
        hlayout_soft = QHBoxLayout()
        hlayout_soft.addWidget(QLabel("Pourcentage soft skills :"))
        self.spin_soft = QSpinBox()
        self.spin_soft.setRange(0, 100)
        self.spin_soft.setValue(30)
        hlayout_soft.addWidget(self.spin_soft)
        self.layout.addLayout(hlayout_soft)

        self.check_management = QCheckBox("Poste de management")
        self.layout.addWidget(self.check_management)

        self.btn_generer = QPushButton("✨ Générer les compétences")
        self.btn_generer.clicked.connect(self.generer_competences)
        self.layout.addWidget(self.btn_generer)

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Nom", "Type", "Niveau requis"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.layout.addWidget(self.table)

        btns_table = QHBoxLayout()
        self.btn_add = QPushButton("➕ Ajouter une ligne")
        self.btn_remove = QPushButton("🗑️ Supprimer la ligne")
        self.btn_add.clicked.connect(self.ajouter_ligne)
        self.btn_remove.clicked.connect(self.supprimer_ligne_selectionnee)
        btns_table.addWidget(self.btn_add)
        btns_table.addWidget(self.btn_remove)
        self.layout.addLayout(btns_table)

        btns = QHBoxLayout()
        self.btn_ok = QPushButton("Valider et sauvegarder")
        self.btn_cancel = QPushButton("Annuler")
        self.btn_ok.clicked.connect(self.accept)
        self.btn_cancel.clicked.connect(self.reject)
        btns.addStretch()
        btns.addWidget(self.btn_ok)
        btns.addWidget(self.btn_cancel)
        self.layout.addLayout(btns)

    def toggle_inputs(self):
        choice = self.combo_emploi.currentText()
        self.combo_autre.setVisible(choice == "Autre emploi existant...")
        is_new = choice == "Créer un nouvel emploi..."
        for widget in (self.input_titre, self.input_famille, self.input_sous_famille):
            widget.setVisible(is_new)

    def generer_competences(self):
        emploi = self.get_nom_emploi()
        if not emploi:
            QMessageBox.warning(self, "Emploi manquant", "Veuillez sélectionner ou créer un emploi valide.")
            return

        params = {
            "pourcentage_soft": self.spin_soft.value(),
            "est_management": self.check_management.isChecked()
        }

        try:
            prompt = self.prompt_builder(emploi, self.contenu_fichier, params)
            reponse_ia = self.openai_controller.openai_service.ask_once(prompt)
            data = json.loads(self.json_extractor(reponse_ia))
            self.remplir_table(data)
        except Exception as e:
            QMessageBox.critical(self, "Erreur IA", str(e))

    def remplir_table(self, data):
        self.table.setRowCount(0)
        for c in data:
            self.ajouter_ligne(c.get("nom", ""), c.get("type", "hard"), c.get("niveau_requis", 1))

    def ajouter_ligne(self, nom="", type_="hard", niveau=1):
        row = self.table.rowCount()
        self.table.insertRow(row)
        self.table.setItem(row, 0, QTableWidgetItem(nom))

        combo = QComboBox()
        combo.addItems(["hard", "soft"])
        combo.setCurrentText(type_)
        self.table.setCellWidget(row, 1, combo)

        spin = QSpinBox()
        spin.setRange(1, self.nb_niveaux)
        spin.setValue(int(niveau))
        self.table.setCellWidget(row, 2, spin)

    def supprimer_ligne_selectionnee(self):
        selected = self.table.selectedItems()
        if selected:
            self.table.removeRow(selected[0].row())

    def get_donnees_valides(self):
        donnees = []
        for row in range(self.table.rowCount()):
            nom_item = self.table.item(row, 0)
            nom = nom_item.text().strip() if nom_item else ""
            if not nom:
                continue
            type_ = self.table.cellWidget(row, 1).currentText()
            niveau = self.table.cellWidget(row, 2).value()
            donnees.append({"nom": nom, "type": type_, "niveau_requis": niveau})
        return donnees

    def get_nom_emploi(self):
        if not self.contenu_fichier:
            return self.titre_fichier

        choix = self.combo_emploi.currentText()
        if choix == "Créer un nouvel emploi...":
            return self.input_titre.text().strip()
        elif choix == "Autre emploi existant...":
            emp = self.combo_autre.currentData()
            return emp.get("titre")
        else:
            emp = self.combo_emploi.currentData()
            return emp.get("titre")
