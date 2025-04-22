from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QSpinBox, QComboBox,
    QCheckBox, QPushButton, QGroupBox, QMessageBox
)

class DialogNouveauProjet(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Créer un nouveau projet")
        self.setMinimumWidth(500)

        layout = QVBoxLayout()

        # 🟦 Groupe Informations générales
        group_general = QGroupBox("Informations générales")
        general_layout = QVBoxLayout()

        self.input_nom_projet = QLineEdit()
        self.input_secteur = QLineEdit()
        self.combo_type_entreprise = QComboBox()
        self.combo_type_entreprise.addItems(["", "TPE", "PME", "ETI", "Grand Groupe", "Start-up"])
        self.input_taille = QLineEdit()
        self.spin_collaborateurs = QSpinBox()
        self.spin_collaborateurs.setMaximum(100000)
        self.spin_filiales = QSpinBox()
        self.spin_filiales.setMaximum(1000)
        self.check_internationale = QCheckBox("Entreprise internationale")
        self.spin_digitalisation = QSpinBox()
        self.spin_digitalisation.setRange(0, 10)

        general_layout.addWidget(QLabel("Nom du projet"))
        general_layout.addWidget(self.input_nom_projet)
        general_layout.addWidget(QLabel("Secteur d'activité"))
        general_layout.addWidget(self.input_secteur)
        general_layout.addWidget(QLabel("Type d'entreprise"))
        general_layout.addWidget(self.combo_type_entreprise)
        general_layout.addWidget(QLabel("Taille de l'entreprise"))
        general_layout.addWidget(self.input_taille)
        general_layout.addWidget(QLabel("Nombre de collaborateurs"))
        general_layout.addWidget(self.spin_collaborateurs)
        general_layout.addWidget(QLabel("Nombre de filiales"))
        general_layout.addWidget(self.spin_filiales)
        general_layout.addWidget(self.check_internationale)
        general_layout.addWidget(QLabel("Niveau de digitalisation"))
        general_layout.addWidget(self.spin_digitalisation)

        group_general.setLayout(general_layout)
        layout.addWidget(group_general)

        # 🟩 Groupe Paramètres compétences
        group_param = QGroupBox("Paramètres compétences & fiches")
        param_layout = QVBoxLayout()

        self.spin_nb_niveaux = QSpinBox()
        self.spin_nb_comp_min = QSpinBox()
        self.spin_nb_comp_max = QSpinBox()
        self.spin_macro_min = QSpinBox()
        self.spin_macro_max = QSpinBox()
        self.spin_micro_min = QSpinBox()
        self.spin_micro_max = QSpinBox()

        for spin in [self.spin_nb_niveaux, self.spin_nb_comp_min, self.spin_nb_comp_max,
                     self.spin_macro_min, self.spin_macro_max, self.spin_micro_min, self.spin_micro_max]:
            spin.setMaximum(20)

        param_layout.addWidget(QLabel("Nombre de niveaux de compétence"))
        param_layout.addWidget(self.spin_nb_niveaux)
        param_layout.addWidget(QLabel("Compétences par poste (min / max)"))
        param_layout.addWidget(self.spin_nb_comp_min)
        param_layout.addWidget(self.spin_nb_comp_max)
        param_layout.addWidget(QLabel("Macro-activités par poste (min / max)"))
        param_layout.addWidget(self.spin_macro_min)
        param_layout.addWidget(self.spin_macro_max)
        param_layout.addWidget(QLabel("Micro-activités par macro (min / max)"))
        param_layout.addWidget(self.spin_micro_min)
        param_layout.addWidget(self.spin_micro_max)

        group_param.setLayout(param_layout)
        layout.addWidget(group_param)

        # 🟡 Boutons
        buttons = QHBoxLayout()
        self.btn_ok = QPushButton("Créer")
        self.btn_cancel = QPushButton("Annuler")
        buttons.addWidget(self.btn_cancel)
        buttons.addWidget(self.btn_ok)
        layout.addLayout(buttons)

        self.setLayout(layout)

        self.btn_ok.clicked.connect(self.accept)
        self.btn_cancel.clicked.connect(self.reject)

    def get_data(self):
        return {
            "nom": self.input_nom_projet.text().strip(),
            "secteur": self.input_secteur.text().strip(),
            "type_entreprise": self.combo_type_entreprise.currentText(),
            "taille": self.input_taille.text().strip(),
            "collaborateurs": self.spin_collaborateurs.value(),
            "filiales": self.spin_filiales.value(),
            "international": self.check_internationale.isChecked(),
            "digitalisation": self.spin_digitalisation.value(),
            "nb_niveaux": self.spin_nb_niveaux.value(),
            "nb_comp_min": self.spin_nb_comp_min.value(),
            "nb_comp_max": self.spin_nb_comp_max.value(),
            "nb_macro_min": self.spin_macro_min.value(),
            "nb_macro_max": self.spin_macro_max.value(),
            "nb_micro_min": self.spin_micro_min.value(),
            "nb_micro_max": self.spin_micro_max.value(),
        }
