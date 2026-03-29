from typing import List
import datetime
from entites.vendeur import Vendeur
from entites.produit import Produit
from composants.ligne_ticket import LigneTicket

# CLASSE METIER - LOGIQUE COMPLEXE 

class Ticket:
    # Classe principale gérant la logique du ticket de caisse, composisé de LigneTicket
    def __init__(self, id_ticket: int, vendeur: Vendeur):
        self.id = id_ticket
        self.vendeur = vendeur
        self.date_creation = datetime.datetime.now()
        self.lignes: List[LigneTicket] = []

    def ajouter_produit(self, produit: Produit, quantite: int = 1):
        # Ajoute / augmente la quantité d'un produit au ticket
        for ligne in self.lignes:
            if ligne.produit.id == produit.id:
                ligne.quantite += quantite
                return
        
        nouvelle_ligne = LigneTicket(produit, quantite)
        self.lignes.append(nouvelle_ligne)

    @property
    def total_ttc(self) -> float:
        # Calcule dynamique du total du ticket
        return sum(ligne.sous_total for ligne in self.lignes)
