from db import crud

class FinaliteEmploiService:
    def __init__(self, projet_id):
        self.projet_id = projet_id

    def get_finalite(self, emploi_id):
        return crud.get_finalite_by_emploi(emploi_id)

    def set_finalite(self, emploi_id, finalite):
        crud.set_finalite_emploi(emploi_id, finalite)

    def emploi_exists(self, emploi_id):
        return crud.get_emploi_by_id(emploi_id) is not None
