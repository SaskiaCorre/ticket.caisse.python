class Vendeur:
    def __init__(self, id_vendeur: int, nom: str, prenom: str):
        self.id = id_vendeur
        self.nom = nom
        self.prenom = prenom

    @property
    def nom_complet(self) -> str:
        return f"{self.prenom} {self.nom}"

