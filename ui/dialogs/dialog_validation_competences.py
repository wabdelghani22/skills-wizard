from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QHBoxLayout, QComboBox, QSpinBox
)
from PyQt5.QtWidgets import QHeaderView  # déjà probablement importé ailleurs


class DialogValidationCompetences(QDialog):
    def __init__(self, competences, nb_niveaux=5, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Validation des Compétences")
        self.resize(600, 400)

        self.competences = competences
        self.nb_niveaux = nb_niveaux

        self.layout = QVBoxLayout(self)

        self.table = QTableWidget(self)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Nom", "Type", "Niveau requis"])
        self.table.setRowCount(len(competences))

        for row, c in enumerate(competences):
            # Nom
            item_nom = QTableWidgetItem(c.get("nom", ""))
            self.table.setItem(row, 0, item_nom)

            # Type (ComboBox)
            combo_type = QComboBox()
            combo_type.addItems(["hard", "soft"])
            type_index = combo_type.findText(c.get("type", "hard"))
            if type_index >= 0:
                combo_type.setCurrentIndex(type_index)
            self.table.setCellWidget(row, 1, combo_type)

            # Niveau requis (SpinBox)
            niveau_spin = QSpinBox()
            niveau_spin.setRange(1, self.nb_niveaux)
            niveau_spin.setValue(int(c.get("niveau_requis", 1)))
            self.table.setCellWidget(row, 2, niveau_spin)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.layout.addWidget(self.table)

        # Boutons OK / Annuler
        button_layout = QHBoxLayout()

        self.btn_add = QPushButton("➕ Ajouter une ligne")
        self.btn_remove = QPushButton("🗑️ Supprimer la ligne sélectionnée")
        self.btn_ok = QPushButton("Valider")
        self.btn_cancel = QPushButton("Annuler")

        self.btn_add.clicked.connect(self.ajouter_ligne)
        self.btn_remove.clicked.connect(self.supprimer_ligne_selectionnee)
        self.btn_ok.clicked.connect(self.accept)
        self.btn_cancel.clicked.connect(self.reject)

        button_layout.addWidget(self.btn_add)
        button_layout.addWidget(self.btn_remove)
        button_layout.addStretch()  # espace flexible
        button_layout.addWidget(self.btn_ok)
        button_layout.addWidget(self.btn_cancel)
        self.layout.addLayout(button_layout)

    def ajouter_ligne(self):
        row = self.table.rowCount()
        self.table.insertRow(row)

        item_nom = QTableWidgetItem("")
        self.table.setItem(row, 0, item_nom)

        combo_type = QComboBox()
        combo_type.addItems(["hard", "soft"])
        self.table.setCellWidget(row, 1, combo_type)

        spin_niveau = QSpinBox()
        spin_niveau.setRange(1, self.nb_niveaux)
        spin_niveau.setValue(1)
        self.table.setCellWidget(row, 2, spin_niveau)

    def supprimer_ligne_selectionnee(self):
        selected = self.table.selectedItems()
        if selected:
            row = selected[0].row()
            self.table.removeRow(row)

    def get_data(self):
        data = []
        for row in range(self.table.rowCount()):
            nom_item = self.table.item(row, 0)
            nom = nom_item.text() if nom_item else ""

            combo_type = self.table.cellWidget(row, 1)
            type_ = combo_type.currentText() if combo_type else "hard"

            spin_niveau = self.table.cellWidget(row, 2)
            niveau = spin_niveau.value() if spin_niveau else 1

            if nom.strip():  # ne pas inclure de lignes vides
                data.append({
                    "nom": nom.strip(),
                    "type": type_,
                    "niveau_requis": niveau
                })

        return data
