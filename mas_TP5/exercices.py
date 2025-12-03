"""
TP Bonus : Système de Livraison avec SPADE
À COMPLÉTER

Prérequis:
    pip install spade
    
Exécution:
    python main.py
"""

import spade
import asyncio
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, OneShotBehaviour
from spade.message import Message

# Pour éviter les warning logs
import logging

# Baisser le niveau de verbosité
logging.getLogger("spade").setLevel(logging.CRITICAL)
logging.getLogger("pyjabber").setLevel(logging.CRITICAL)
logging.getLogger("asyncio").setLevel(logging.CRITICAL)


# =============================================================================
# PARTIE 1 : Agent Livreur
# =============================================================================

class LivreurAgent(Agent):
    """
    Agent livreur qui répond aux appels d'offres.
    
    Attributs:
        tarif: prix par km
        position: tuple (x, y)
        disponible: True/False
    """
    
    def __init__(self, jid, password, tarif, position, disponible=True):
        super().__init__(jid, password)
        self.tarif = tarif
        self.position = position
        self.disponible = disponible
    
    def calculer_distance(self, destination):
        """Distance Manhattan vers la destination."""
        return abs(self.position[0] - destination[0]) + abs(self.position[1] - destination[1])
    
    class RecevoirCFP(CyclicBehaviour):
        """Comportement pour recevoir et traiter les CFP."""
        
        async def run(self):
            msg = await self.receive(timeout=5)
            if msg:
                performative = msg.get_metadata("performative")
                
                if performative == "cfp":
                    # TODO: Extraire la destination du msg.body
                    # Format: "livraison:(3,4)" → destination = (3, 4)
                    
                    # TODO: Si disponible:
                    #   - Calculer le coût (distance * tarif)
                    #   - Envoyer un message "propose" avec body = f"cout:{cout}"
                    # Sinon:
                    #   - Envoyer un message "refuse"
                    
                    pass  # Remplacer par votre code
                
                elif performative == "accept-proposal":
                    # TODO: Afficher "Livraison acceptée!"
                    # TODO: Envoyer un message "inform" avec body = "done"
                    
                    pass  # Remplacer par votre code
                
                elif performative == "reject-proposal":
                    # TODO: Afficher "Offre refusée"
                    
                    pass  # Remplacer par votre code
    
    async def setup(self):
        print(f"🚚 {self.jid} démarré (tarif={self.tarif}, position={self.position})")
        self.add_behaviour(self.RecevoirCFP())


# =============================================================================
# PARTIE 2 : Agent Gestionnaire
# =============================================================================

class GestionnaireAgent(Agent):
    """
    Agent gestionnaire qui coordonne les livraisons via Contract Net.
    """
    
    def __init__(self, jid, password, livreurs_jids):
        super().__init__(jid, password)
        self.livreurs_jids = livreurs_jids  # Liste des JIDs des livreurs
        self.propositions = []
    
    class LancerAppelOffres(OneShotBehaviour):
        """Comportement pour lancer un appel d'offres."""
        
        async def on_start(self):
            self.agent.propositions = []
        
        async def run(self):
            destination = self.agent.destination
            print(f"\n📢 Lancement appel d'offres pour livraison à {destination}")
            
            # TODO: Pour chaque livreur dans self.agent.livreurs_jids:
            #   - Créer un message avec performative = "cfp"
            #   - body = f"livraison:{destination}"
            #   - Envoyer le message
            
            pass  # Remplacer par votre code
            
            # Attendre les réponses
            await asyncio.sleep(2)
    
    class CollecterPropositions(CyclicBehaviour):
        """Comportement pour collecter les propositions."""
        
        async def run(self):
            msg = await self.receive(timeout=3)
            if msg:
                performative = msg.get_metadata("performative")
                
                if performative == "propose":
                    # TODO: Extraire le coût du msg.body (format: "cout:XX")
                    # TODO: Ajouter à self.agent.propositions:
                    #       {'livreur': str(msg.sender), 'cout': cout}
                    # TODO: Afficher la proposition
                    
                    pass  # Remplacer par votre code
                
                elif performative == "refuse":
                    print(f"  ❌ {msg.sender} a refusé")
                
                elif performative == "inform":
                    if msg.body == "done":
                        print(f"  ✅ Livraison confirmée par {msg.sender}")
    
    class SelectionnerMeilleur(OneShotBehaviour):
        """Comportement pour sélectionner la meilleure offre."""
        
        async def run(self):
            await asyncio.sleep(3)  # Attendre les propositions
            
            print(f"\n🔍 Évaluation des {len(self.agent.propositions)} propositions...")
            
            if not self.agent.propositions:
                print("  Aucune proposition reçue!")
                return
            
            # TODO: Trouver la proposition avec le coût minimum
            # TODO: Pour chaque proposition:
            #   - Si c'est le gagnant: envoyer "accept-proposal"
            #   - Sinon: envoyer "reject-proposal"
            # TODO: Afficher le gagnant
            
            pass  # Remplacer par votre code
    
    async def setup(self):
        print(f"📋 {self.jid} démarré")
        self.add_behaviour(self.CollecterPropositions())
    
    def lancer_livraison(self, destination):
        """Lancer une livraison vers une destination."""
        self.destination = destination
        self.add_behaviour(self.LancerAppelOffres())
        self.add_behaviour(self.SelectionnerMeilleur())


# =============================================================================
# PARTIE 3 : Fonction principale
# =============================================================================

async def main():
    """Lancer la simulation."""
    print("=" * 60)
    print("🚚 SIMULATION SYSTÈME DE LIVRAISON SPADE")
    print("=" * 60)
    
    # TODO: Créer 3 agents livreurs avec les JIDs:
    #   - "livreur_a@localhost" (tarif=2.0, position=(0,0), disponible=True)
    #   - "livreur_b@localhost" (tarif=1.5, position=(5,5), disponible=True)
    #   - "livreur_c@localhost" (tarif=1.0, position=(10,0), disponible=False)
    # Password: "password" pour tous
    
    # TODO: Créer l'agent gestionnaire avec JID "gestionnaire@localhost"
    # Passer la liste des JIDs des livreurs
    
    # TODO: Démarrer tous les agents avec await agent.start()
    
    # TODO: Attendre un peu puis lancer une livraison vers (3, 4)
    # gestionnaire.lancer_livraison((3, 4))
    
    # TODO: Attendre la fin (await asyncio.sleep(10))
    
    # TODO: Arrêter tous les agents avec await agent.stop()
    
    pass  # Remplacer par votre code
    
    print("\n" + "=" * 60)
    print("✅ SIMULATION TERMINÉE")
    print("=" * 60)


if __name__ == "__main__":
    # embedded_xmpp_server=True lance automatiquement le serveur XMPP
    spade.run(main(), embedded_xmpp_server=True)
