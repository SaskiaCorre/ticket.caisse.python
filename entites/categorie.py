class Categorie:
    def __init__(self, id_categorie: int, nom: str):
        self.id = id_categorie
        self.nom = nom

    def __str__(self):
        return f"Catégorie: {self.nom}"
    
    @property
    def nom_categorie(self) -> str:
        return f"{self.nom}"