from entites.categorie import Categorie

class Produit:
    def __init__(self, id_produit: int, nom: str, tarif: float, categorie: Categorie, description: str = ""):
        self.id = id_produit
        self.nom = nom
        self.tarif = tarif
        self.categorie = categorie
        self.description = description

    def __str__(self):
        return f"{self.nom} ({self.categorie.nom}) - {self.tarif:.2f}€"
