from PyQt5.QtWidgets import (
    QDialog, QLabel, QVBoxLayout, QHBoxLayout,
    QSpinBox, QCheckBox, QDialogButtonBox, QPushButton
)

class DialogParametresEmploi(QDialog):
    def __init__(self, nom_emploi, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Paramètres de génération")
        self.setMinimumWidth(300)
        self.arret_demande = False  # ⚠️ Pour détecter un arrêt

        layout = QVBoxLayout()

        # 🔹 Affichage du nom de l'emploi
        self.label_titre = QLabel(f"<b>Paramètres pour : {nom_emploi}</b>")
        layout.addWidget(self.label_titre)

        # 🔹 Pourcentage soft skills
        layout_soft = QHBoxLayout()
        self.label_soft = QLabel("Pourcentage de soft skills :")
        self.spin_soft = QSpinBox()
        self.spin_soft.setRange(0, 100)
        self.spin_soft.setValue(30)
        layout_soft.addWidget(self.label_soft)
        layout_soft.addWidget(self.spin_soft)
        layout.addLayout(layout_soft)

        # 🔹 Est-ce un poste de management ?
        self.check_management = QCheckBox("Poste de management")
        layout.addWidget(self.check_management)

        # 🔹 Boutons
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        layout.addWidget(self.buttonBox)

        self.btn_arreter = QPushButton("Arrêter ici")
        self.buttonBox.addButton(self.btn_arreter, QDialogButtonBox.ActionRole)

        self.setLayout(layout)

        # Connexions
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.btn_arreter.clicked.connect(self.stop_and_close)

    def stop_and_close(self):
        self.arret_demande = True
        self.reject()  # On ferme sans accepter

    def get_data(self):
        return {
            "pourcentage_soft": self.spin_soft.value(),
            "est_management": self.check_management.isChecked()
        }
