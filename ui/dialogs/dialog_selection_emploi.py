from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QPushButton, QHBoxLayout, QLineEdit, QMessageBox

class DialogSelectionEmploi(QDialog):
    def __init__(self, suggestions_ia, titre_fichier,emplois_existants, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Sélection de l'emploi")
        self.setMinimumWidth(400)
        self.titre_fichier = titre_fichier
        self.emploi_selectionne = None
        self.suggestions = suggestions_ia
        self.emplois_existants = emplois_existants
        # 🔹 Affiche le nom brut du fichier (contexte)
        
        layout = QVBoxLayout()
        if self.titre_fichier:
            label_fichier = QLabel(f"<b>Fichier analysé :</b> {self.titre_fichier}")
            layout.addWidget(label_fichier)
        layout.addWidget(QLabel("Suggestions IA :"))

        self.combo_ia = QComboBox()
        for s in self.suggestions:
            label = f"{s['titre']} ({s['famille']} / {s['sous_famille']})"
            self.combo_ia.addItem(label, s)
        self.combo_ia.addItem("Autre emploi existant...")
        self.combo_ia.addItem("Créer un nouvel emploi...")
        layout.addWidget(self.combo_ia)

        # Combo emploi existant
        self.combo_autre = QComboBox()
        for emp in self.emplois_existants:
            self.combo_autre.addItem(emp['titre'], emp)
        self.combo_autre.setVisible(False)
        layout.addWidget(self.combo_autre)

        # Création manuelle
        self.input_titre = QLineEdit()
        self.input_famille = QLineEdit()
        self.input_sous_famille = QLineEdit()
        self.input_titre.setPlaceholderText("Nom de l'emploi")
        self.input_famille.setPlaceholderText("Famille")
        self.input_sous_famille.setPlaceholderText("Sous-famille")
        self.input_titre.setVisible(False)
        self.input_famille.setVisible(False)
        self.input_sous_famille.setVisible(False)
        layout.addWidget(self.input_titre)
        layout.addWidget(self.input_famille)
        layout.addWidget(self.input_sous_famille)

        # Buttons
        buttons = QHBoxLayout()
        btn_ok = QPushButton("Valider")
        btn_cancel = QPushButton("Annuler")
        buttons.addWidget(btn_ok)
        buttons.addWidget(btn_cancel)
        layout.addLayout(buttons)

        self.setLayout(layout)

        # Events
        self.combo_ia.currentIndexChanged.connect(self.toggle_inputs)
        btn_ok.clicked.connect(self.accept_dialog)
        btn_cancel.clicked.connect(self.reject)

    def toggle_inputs(self):
        index = self.combo_ia.currentIndex()
        self.combo_autre.setVisible(self.combo_ia.itemText(index) == "Autre emploi existant...")
        is_creer = self.combo_ia.itemText(index) == "Créer un nouvel emploi..."
        self.input_titre.setVisible(is_creer)
        self.input_famille.setVisible(is_creer)
        self.input_sous_famille.setVisible(is_creer)

    def accept_dialog(self):
        choice = self.combo_ia.currentText()
        if choice == "Créer un nouvel emploi...":
            titre = self.input_titre.text().strip()
            famille = self.input_famille.text().strip()
            sous_famille = self.input_sous_famille.text().strip()
            if not titre or not famille or not sous_famille:
                QMessageBox.warning(self, "Champs manquants", "Merci de remplir tous les champs pour créer un nouvel emploi.")
                return
            self.emploi_selectionne = {"titre": titre, "famille": famille, "sous_famille": sous_famille, "nouveau": True}
        elif choice == "Autre emploi existant...":
            emp = self.combo_autre.currentData()
            self.emploi_selectionne = {"titre": emp["titre"], "famille": emp.get("famille", ""), "sous_famille": emp.get("sous_famille", ""), "nouveau": False}
        else:
            self.emploi_selectionne = self.combo_ia.currentData()
            self.emploi_selectionne["nouveau"] = False
        self.accept()

    def get_emploi_selectionne(self):
        return self.emploi_selectionne