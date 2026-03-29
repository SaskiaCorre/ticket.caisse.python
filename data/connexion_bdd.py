import sqlite3
from entites.produit import Produit
from entites.vendeur import Vendeur
from entites.categorie import Categorie
from composants.ticket import Ticket
from typing import Optional

# GESTIONNAIRE DE BASE DE DONNÉES SQLITE

class DatabaseManager:
    # Fait le lien entre la base SQLite et les Objets Python   
    def __init__(self, db_name="caisse.db"):
        self.db_name = db_name

    def initialiser_bdd(self):
        # Créer les tables et insère des données de test
        # Le bloc 'with' gère automatiquement la fermeture de la connexion
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            
            # Création des tables
            cursor.execute('''CREATE TABLE IF NOT EXISTS categorie (id INTEGER PRIMARY KEY, 
                                                                    nom TEXT)
                           ''')
            
            cursor.execute('''CREATE TABLE IF NOT EXISTS produit (id INTEGER PRIMARY KEY, 
                                                                  nom TEXT, 
                                                                  tarif REAL, 
                                                                  id_categorie INTEGER, 
                                                                  FOREIGN KEY(id_categorie) REFERENCES categorie(id))
                           ''')
            
            cursor.execute('''CREATE TABLE IF NOT EXISTS vendeur (id INTEGER PRIMARY KEY, 
                                                                  nom TEXT, 
                                                                  prenom TEXT)
                           ''')
            
            cursor.execute('''CREATE TABLE IF NOT EXISTS ticket (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                                                 date_creation TEXT, 
                                                                 id_vendeur INTEGER, 
                                                                 FOREIGN KEY(id_vendeur) REFERENCES vendeur(id))
                           ''')
            
            cursor.execute('''CREATE TABLE IF NOT EXISTS produit_ticket (id_ticket INTEGER, 
                                                                         id_produit INTEGER, 
                                                                         quantite INTEGER, 
                                                                         PRIMARY KEY(id_ticket, id_produit))
                           ''')
            
            # Jeu de données inséré uniquement au 1er lancement
            cursor.execute("SELECT COUNT(*) FROM vendeur")
            if cursor.fetchone()[0] == 0:
                
                # Insertion des données
                cursor.execute("INSERT INTO categorie VALUES (1, 'Alimentaire'), (2, 'Bricolage')")
                
                cursor.execute("INSERT INTO produit VALUES (101, 'Café Arabica', 5.50, 1), (102, 'Marteau Pro', 12.90, 2), (103, 'Pâtes 500g', 1.20, 1)")
                
                cursor.execute("INSERT INTO vendeur VALUES (1, 'DUPONT', 'Jean')")
            
            conn.commit()

    def get_produit(self, id_produit: int) -> Optional[Produit]:
        # Récupérer une ligne SQL pour la transformer en Objet Produit
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT p.id, p.nom, p.tarif, c.id, c.nom 
                FROM produit p 
                JOIN categorie c ON p.id_categorie = c.id 
                WHERE p.id = ?
            ''', (id_produit,))
            row = cursor.fetchone()
            
            if row:
                return Produit(row[0], row[1], row[2], Categorie(row[3], row[4]))
            return None

    def get_vendeur(self, id_vendeur: int) -> Optional[Vendeur]:
        # Récupérer une ligne SQL pour la transformer en Objet Vendeur
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, nom, prenom FROM vendeur WHERE id = ?", (id_vendeur,))
            row = cursor.fetchone()
            return Vendeur(row[0], row[1], row[2]) if row else None
            
    def sauvegarder_ticket(self, ticket: Ticket):
        # Sauvegarder l'Objet Ticket complet (et ses lignes) dans les tables SQL
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            # Sauvegarder l'en-tête du ticket
            cursor.execute("INSERT INTO ticket (date_creation, id_vendeur) VALUES (?, ?)", 
                           (ticket.date_creation.isoformat(), ticket.vendeur.id))
            
            # MAJ de l'objet avec l'ID auto-généré
            ticket.id = cursor.lastrowid 
            
            # Sauvegarder des lignes de produits
            for ligne in ticket.lignes:
                cursor.execute("INSERT INTO produit_ticket (id_ticket, id_produit, quantite) VALUES (?, ?, ?)",
                               (ticket.id, ligne.produit.id, ligne.quantite))
            conn.commit()