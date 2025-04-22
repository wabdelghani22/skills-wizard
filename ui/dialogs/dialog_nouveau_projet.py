from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QCheckBox, QSpinBox, QGroupBox, QFormLayout, QPushButton, QDialogButtonBox, QComboBox
)
from PyQt5.QtCore import Qt


class DialogNouveauProjet(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Créer un nouveau projet")
        self.setMinimumWidth(500)

        # === GROUPE 1 : Informations générales ===
        group_general = QGroupBox("Paramétrage projet")
        layout_general = QFormLayout()
        layout_general.setLabelAlignment(Qt.AlignLeft)

        self.input_nom = QLineEdit()
        self.input_secteur = QLineEdit()
        self.input_type = QComboBox()
        self.input_type.addItems(["TPE", "PME", "Grand Groupe", "Start-up"])
        self.input_type.setMinimumWidth(135)
        self.input_taille = QLineEdit()
        self.input_filiales = QSpinBox()
        self.input_internationale = QCheckBox("Entreprise internationale")
        self.input_digital = QSpinBox()
        self.input_digital.setRange(0, 10)

        layout_general.addRow("Nom du projet *", self.input_nom)
        layout_general.addRow("Secteur d'activité *", self.input_secteur)
        layout_general.addRow("Type d’entreprise", self.input_type)
        layout_general.addRow("Taille d’entreprise", self.input_taille)
        layout_general.addRow("Nb filiales", self.input_filiales)
        layout_general.addRow("Digitalisation (0–10)", self.input_digital)
        layout_general.addRow(self.input_internationale)
        
        # === GROUPE 2 : Paramétrage fiches et compétences ===
        #group_params = QGroupBox("Paramètres des fiches et du référentiel")
        #layout_params = QFormLayout()
        #layout_params.setLabelAlignment(Qt.AlignLeft)
        #group_params = QGroupBox("Paramètres des compétences")
        #layout_params = QFormLayout()
        #layout_params.setLabelAlignment(Qt.AlignLeft)
        
        self.input_nb_niveaux = QSpinBox()
        self.input_nb_niveaux.setRange(1, 10)
        #self.input_nb_niveaux.setMinimumWidth(135)
        self.input_comp_min = QSpinBox()
        #self.input_comp_min.setMinimumWidth(135)
        self.input_comp_max = QSpinBox()
        #self.input_comp_max.setMinimumWidth(135)
        self.input_macro_min = QSpinBox()
        #self.input_macro_min.setMinimumWidth(135)
        self.input_macro_max = QSpinBox()
        #self.input_macro_max.setMinimumWidth(135)
        self.input_micro_min = QSpinBox()
        #self.input_micro_min.setMinimumWidth(135)
        self.input_micro_max = QSpinBox()
        #self.input_micro_max.setMinimumWidth(135)
        
        layout_general.addRow("Nombre de niveaux", self.input_nb_niveaux)
        layout_general.addRow("Nb compétences (min)", self.input_comp_min)
        layout_general.addRow("Nb compétences (max)", self.input_comp_max)
        layout_general.addRow("Nb macro-activités (min)", self.input_macro_min)
        layout_general.addRow("Nb macro-activités (max)", self.input_macro_max)
        layout_general.addRow("Nb micro-activités (min)", self.input_micro_min)
        layout_general.addRow("Nb micro-activités (max)", self.input_micro_max)
        #group_params.setLayout(layout_params)
        group_general.setLayout(layout_general)


        # === Boutons OK / Annuler ===
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        # === Layout principal ===
        main_layout = QVBoxLayout()

       
        main_layout.addWidget(group_general)
        #main_layout.addWidget(group_params)
        main_layout.addWidget(self.buttons)
        #main_layout.setAlignment(Qt.AlignTop | Qt.AlignCenter)
        self.setLayout(main_layout)

    def get_data(self):
        return {
            "nom": self.input_nom.text().strip(),
            "secteur": self.input_secteur.text().strip(),
            "type_entreprise": self.input_type.currentText(),
            "taille": self.input_taille.text().strip(),
            "filiales": self.input_filiales.value(),
            "international": self.input_internationale.isChecked(),
            "digitalisation": self.input_digital.value(),
            "nb_niveaux": self.input_nb_niveaux.value(),
            "nb_comp_min": self.input_comp_min.value(),
            "nb_comp_max": self.input_comp_max.value(),
            "nb_macro_min": self.input_macro_min.value(),
            "nb_macro_max": self.input_macro_max.value(),
            "nb_micro_min": self.input_micro_min.value(),
            "nb_micro_max": self.input_micro_max.value(),
        }
