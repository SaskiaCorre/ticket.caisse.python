from entites.produit import Produit

# CLASSE METIER - LOGIQUE COMPLEXE

class LigneTicket:
    # Représente chaque ligne d'un ticket (Produit + Quantité + avec @property, on lui attribue un sous-total)
    def __init__(self, produit: Produit, quantite: int):
        self.produit = produit
        self.quantite = quantite

    @property
    def sous_total(self) -> float:
        return self.produit.tarif * self.quantite
    