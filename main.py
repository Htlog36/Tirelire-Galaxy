"""
TIRELIRE GALAXY
Application de gestion d'argent de poche gamifiée pour enfants.

COMMENT LANCER L'APPLICATION :
1. Ouvrez votre terminal.
2. Installez les dépendances (une seule fois) :
   pip install -r requirements.txt
3. Lancez le vaisseau :
   python main.py
"""

import time
import random
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt
from rich.table import Table
from rich.theme import Theme
from rich.align import Align
from rich.progress import BarColumn, Progress, TextColumn
from rich.layout import Layout
from rich.live import Live
from rich.text import Text

# Configuration du thème galactique
custom_theme = Theme({
    "primary": "cyan",
    "secondary": "magenta",
    "accent": "bold yellow",
    "danger": "bold red",
    "success": "bold green",
    "title": "bold magenta reverse",
    "highlight": "bold white on blue",
})

console = Console(theme=custom_theme)

# État initial du Capitaine
ETAT_JOUEUR = {
    "solde": 50,
    "objectif": 100,  # Objectif pour le graphique
    "nom": "Capitaine"
}

# Données de jeu
MISSIONS = [
    {"titre": "Ranger le sas de décompression (Ta chambre)", "gain": 10, "emoji": "🧹"},
    {"titre": "Réparer le robot de cuisine (Vider le lave-vaisselle)", "gain": 5, "emoji": "🍽️"},
    {"titre": "Aider un alien à quatre pattes (Sortir le chien)", "gain": 8, "emoji": "🐕"},
    {"titre": "Étudier les cartes stellaires (Faire ses devoirs)", "gain": 15, "emoji": "📚"},
    {"titre": "Recycler les déchets spatiaux (Sortir les poubelles)", "gain": 3, "emoji": "♻️"},
]

MARCHE = [
    {"nom": "Bonbons Lunaires", "prix": 3, "emoji": "🍬"},
    {"nom": "Jus de Nébuleuse (Soda)", "prix": 5, "emoji": "🥤"},
    {"nom": "Holocube de Jeu (Jeu Vidéo)", "prix": 40, "emoji": "🎮"},
    {"nom": "Figurine de l'Alliance", "prix": 15, "emoji": "🤖"},
    {"nom": "Carburant de Vaisseau (Glace)", "prix": 4, "emoji": "🍦"},
]

def effacer_ecran():
    console.clear()

def afficher_banniere():
    titre = """
    ✨ TIRELIRE GALAXY ✨
    """
    console.print(Panel(Align.center(titre), style="title", subtitle="Gestion de Crédits Galactiques v1.0"))

def animation_chargement(message="Chargement des systèmes..."):
    with Progress(
        TextColumn("[bold blue]{task.description}"),
        BarColumn(bar_width=None, style="magenta", complete_style="cyan"),
        transient=True,
    ) as progress:
        task = progress.add_task(message, total=10)
        for _ in range(10):
            time.sleep(0.1)
            progress.advance(task)

def scanner_reserves():
    effacer_ecran()
    afficher_banniere()
    console.print("\n[bold cyan]📊 SCAN DES RÉSERVES...[/bold cyan]\n")
    
    # Affichage du solde
    solde = ETAT_JOUEUR["solde"]
    objectif = ETAT_JOUEUR["objectif"]
    pourcentage = min(100, int((solde / objectif) * 100))
    
    table = Table(show_header=False, box=None)
    table.add_row("[accent]💰 Solde Actuel :[/accent]", f"[accent bold]{solde} Crédits Galactiques[/accent]")
    table.add_row("[secondary]🎯 Objectif :[/secondary]", f"[secondary]{objectif} Crédits[/secondary]")
    console.print(Panel(table, title="État du Compte", border_style="cyan"))

    # Graphique de progression (Bar Chart manuel avec Rich)
    console.print("\n[bold]Progression vers l'objectif :[/bold]")
    
    # Création d'une barre de progression visuelle
    barre_remplie = "█" * (pourcentage // 2)
    barre_vide = "░" * ((100 - pourcentage) // 2)
    couleur = "success" if solde >= objectif else "accent"
    
    console.print(f"[{couleur}]{barre_remplie}[/{couleur}][dim]{barre_vide}[/dim] {pourcentage}%")
    
    if solde >= objectif:
        console.print("\n[bold green]🎉 FÉLICITATIONS CAPITAINE ! OBJECTIF ATTEINT ! 🎉[/bold green]")
        console.print("Vous pouvez acheter un équipement légendaire !")
    else:
        manque = objectif - solde
        console.print(f"\n[italic]Courage Capitaine ! Il manque encore {manque} crédits.[/italic]")

    Prompt.ask("\n[dim]Appuyez sur Entrée pour revenir au pont...[/dim]")

def accomplir_mission():
    effacer_ecran()
    afficher_banniere()
    console.print("\n[bold magenta]🚀 CENTRE DE MISSIONS[/bold magenta]\n")
    
    mission = random.choice(MISSIONS)
    
    console.print(Panel(
        f"[bold]{mission['emoji']} Mission Disponible :[/bold]\n\n"
        f"[cyan]{mission['titre']}[/cyan]\n\n"
        f"Récompense : [accent]+{mission['gain']} Crédits[/accent]",
        title="Ordre de Mission",
        border_style="magenta"
    ))
    
    choix = Prompt.ask("Acceptez-vous cette mission ?", choices=["o", "n"], default="o")
    
    if choix == "o":
        animation_chargement("Exécution de la mission en cours...")
        ETAT_JOUEUR["solde"] += mission["gain"]
        console.print(f"\n[success]✅ Mission accomplie ! Vous avez reçu {mission['gain']} crédits.[/success]")
    else:
        console.print("\n[warning]Mission refusée. Reposez-vous bien Capitaine.[/warning]")
    
    time.sleep(2)

def marche_spatial():
    effacer_ecran()
    afficher_banniere()
    console.print("\n[bold yellow]🛍️ MARCHÉ SPATIAL[/bold yellow]\n")
    
    table = Table(title="Articles Disponibles", border_style="yellow")
    table.add_column("N°", justify="center", style="cyan", no_wrap=True)
    table.add_column("Article", style="magenta")
    table.add_column("Prix", justify="right", style="green")
    
    for i, item in enumerate(MARCHE, 1):
        table.add_row(str(i), f"{item['emoji']} {item['nom']}", f"{item['prix']} 🪙")
        
    console.print(table)
    console.print(f"\n[accent]Votre solde : {ETAT_JOUEUR['solde']} Crédits[/accent]")
    
    choix = IntPrompt.ask("\nQuel article voulez-vous acheter ? (0 pour retour)", default=0)
    
    if 0 < choix <= len(MARCHE):
        item = MARCHE[choix - 1]
        if ETAT_JOUEUR["solde"] >= item["prix"]:
            confirm = Prompt.ask(f"Acheter [bold]{item['nom']}[/bold] pour {item['prix']} crédits ?", choices=["o", "n"], default="o")
            if confirm == "o":
                animation_chargement("Transaction galactique...")
                ETAT_JOUEUR["solde"] -= item["prix"]
                console.print(f"\n[success]🛍️ Achat confirmé ! Profitez de votre {item['nom']}.[/success]")
        else:
            console.print("\n[danger]❌ Fonds insuffisants ! Faites plus de missions, Capitaine.[/danger]")
    elif choix == 0:
        return
    else:
        console.print("\n[danger]Article inconnu.[/danger]")
        
    time.sleep(2)

def menu_principal():
    while True:
        effacer_ecran()
        afficher_banniere()
        
        console.print(f"\n[bold]Bienvenue, {ETAT_JOUEUR['nom']}.[/bold]")
        console.print(f"Solde actuel : [accent]{ETAT_JOUEUR['solde']} 🪙[/accent]\n")
        
        menu = Table.grid(padding=1)
        menu.add_column(style="cyan", justify="right")
        menu.add_column(style="magenta")
        
        menu.add_row("1.", "🚀 Accomplir une mission (Gagner des crédits)")
        menu.add_row("2.", "🛍️ Aller au Marché Spatial (Dépenser)")
        menu.add_row("3.", "📊 Scanner les réserves (Voir stats)")
        menu.add_row("4.", "❌ Quitter le vaisseau")
        
        console.print(Panel(menu, title="Tableau de Bord", border_style="blue"))
        
        choix = Prompt.ask("Ordre du Capitaine", choices=["1", "2", "3", "4"])
        
        if choix == "1":
            accomplir_mission()
        elif choix == "2":
            marche_spatial()
        elif choix == "3":
            scanner_reserves()
        elif choix == "4":
            console.print("\n[bold cyan]👋 Fermeture du sas... À bientôt Capitaine ![/bold cyan]")
            break

if __name__ == "__main__":
    # Petit délai pour l'effet dramatique au lancement
    effacer_ecran()
    animation_chargement("Initialisation du système TIRELIRE-GALAXY...")
    menu_principal()
