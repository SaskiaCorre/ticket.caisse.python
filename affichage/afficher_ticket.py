from composants.ticket import Ticket

class AfficherTicket:
    def __init__(self, ticket: Ticket):
        self.ticket = ticket
        self.lignes = ticket.lignes

    def generer_ticket_texte(self, ticket: Ticket) -> str:
        # Formatage du ticket pour le retour console
        entete = f"\n{'='*30}\n"
        entete += f"       TICKET N°{ticket.id}\n"
        entete += f"{'='*30}\n"
        entete += f"Date: {ticket.date_creation.strftime('%d/%m/%Y %H:%M')}\n"
        entete += f"Vendeur: {ticket.vendeur.nom_complet}\n"
        entete += "-" * 30 + "\n"
        
        corps = ""
        for l in self.lignes:
            corps += f"{l.produit.nom[:15]:<15} x{l.quantite:<2} {l.sous_total:>8.2f}€\n"
        
        pied = "-" * 30 + "\n"
        pied += f"TOTAL A PAYER: {ticket.total_ttc:>12.2f}€\n"
        pied += "=" * 30 + "\n"
        
        return entete + corps + pied
    
    def __str__(self) -> str:
        return self.generer_ticket_texte(self.ticket)
