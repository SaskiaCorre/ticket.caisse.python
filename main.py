from composants.ticket import Ticket
from data.connexion_bdd import DatabaseManager
from affichage.afficher_ticket import AfficherTicket
from data.connexion_bdd import DatabaseManager

# --- SIMULATION EN CONSOLE AVEC SQLITE ---
if __name__ == "__main__":
    # Initialisation de la bdd
    db = DatabaseManager()
    db.initialiser_bdd()
    # Récupération des objets depuis la table SQL
    vendeur_ticket = db.get_vendeur(1)
    
    prod_1 = db.get_produit(101)
    prod_2 = db.get_produit(102)
    prod_3 = db.get_produit(103)

    if not vendeur_ticket or not prod_1 or not prod_2 or not prod_3:
        print("Erreur : Données de test introuvables en base.")
        exit()

    # Simulation d'une vente (logique métier POO)
    # L'ID est à None pour être attribué par SQLite lors de la sauvegarde
    nouveau_ticket = Ticket(id_ticket=None, vendeur=vendeur_ticket)
    
    nouveau_ticket.ajouter_produit(prod_1, 2)
    nouveau_ticket.ajouter_produit(prod_2)
    nouveau_ticket.ajouter_produit(prod_3, 5)
    nouveau_ticket.ajouter_produit(prod_1, 1) # Vérification du cumul

    # Sauvegarde du ticket en bdd
    db.sauvegarder_ticket(nouveau_ticket)

    # Affichage du ticket
    afficher_ticket = AfficherTicket(nouveau_ticket)
    print(afficher_ticket)
    print(f"✅ Le ticket a bien été sauvegardé dans SQLite avec l'ID {nouveau_ticket.id}.")
