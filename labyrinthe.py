#Chargement de librairies et modules
# os et sys
#os.path.join pour changer le sens du "/" ou "\" en fonction de l'OS 
import os
#sys.path[0] est utilisé pour indiquer le repertoire courant
import sys
#Pygame
import pygame
#Génération aléatoire de valeurs
from random import randrange

# Démarrage de pygame
pygame.init()

# Largeur et longueur des cases
width = 40
height = 40
#Récupération des images
#Carreau de mur
wall = pygame.image.load(os.path.join(sys.path[0], "thumb", "mur.png"))
wall = pygame.transform.scale(wall, (width, height))
#Carreau de sol
floor = pygame.image.load(os.path.join(sys.path[0], "thumb", "sol.png"))
floor = pygame.transform.scale(floor, (width, height))
#Icone McGyver
mac = pygame.image.load(os.path.join(sys.path[0], "thumb", "mac.png"))
mac = pygame.transform.scale(mac, (width, height))
#Icone bouteille d'éther
ether = pygame.image.load(os.path.join(sys.path[0], "thumb", "ether.png"))
ether = pygame.transform.scale(ether, (width, height))
#Icone aiguille
needle = pygame.image.load(os.path.join(sys.path[0], "thumb", "aiguille.png"))
needle = pygame.transform.scale(needle, (width, height))
#Icone tube de platique
tube = pygame.image.load(os.path.join(sys.path[0], "thumb", "tube.png"))
tube = pygame.transform.scale(tube, (width, height))
#Icone seringue
serynge = pygame.image.load(os.path.join(sys.path[0], "thumb", "seringue.png"))
serynge = pygame.transform.scale(serynge, (width, height))
#Icone gardien (le méchant du niveau)
guardian = pygame.image.load(os.path.join(sys.path[0], "thumb", "garde.png"))
guardian = pygame.transform.scale(guardian, (width, height))

#Liste représentant les objets à récupérer; tube, aiguille et ether.
objects = ["T", "A", "E"]
#Somme des objets récupérés initialisée à 0
total = 0
#Statut par rarpport à l'issue de la partie
#Partie gagnée?
winning = False
#La rencontre avec le gardien met fin à la partie. L'a-t-on rencontré?
finish = False
#Déclaration de la variable grid qui sera notre matrice représentant les positions des éléments du jeu
grid = None
#mg et guard définissent les positions (tuple de forme [x,y]) respectives de McGyver et du gardien sur la matrice
#Initialisation à None 
mg = None
guard = None 

#Cette fonction répartit les 3 objets à récupérer sur les cases pratiquables (pas les murs)  
def distribute_objects():
    #Cette liste locale représente les 3 objets à récupérer:
    liste_objects = ["T","A","E"]
    #Tant que la liste n'est pas vide
    while liste_objects:
        #On génère une abscisse aléatoirement entre 0 et 14 inclus
        a = randrange(15)
        #On génère une ordonnée aléatoirement entre 0 et 14 inclus
        b = randrange(15) 
        #Si la position obtenue est pratiquable
        if grid[a][b] == "0":
            #On enlève un objet de la liste et on le place en grid[a][b] (car pop returns l'objet) 
            grid[a][b] = liste_objects.pop()

#On ouvre le fichier contenant notre matrice en lecture seule (on le charge)
#with permet de fermer immédiatement la ressource ouverte (structure.txt) une fois le traitement accompli
with open(os.path.join(sys.path[0], "structure.txt"),"r") as f:
    #On en distingue les lignes
    lines = f.readlines()
    #on établit une liste de char à partir de chaque ligne
    #grid est la matrice de lettres issues de structure.txt chaque lettre étant une case
    grid = [list(line.strip()) for line in lines]
#On répartit chaque objets à récupérer sur une case pratiquable de manière aléatoire
distribute_objects()

#Sachant que structure.txt est un carré de 15*15 caractères
for column in range(15):
    for row in range(15):
        if grid[column][row] == "M":
            #On appelle mg la position du caractère "M"
            mg = [column,row]
        if grid[column][row] == "G":
            #On appelle guard la position du caractère "G"
            guard = [column,row] 

#Ces variables servent à la création de la fenêtre pygame

#largeur de fenêtre
WINDOW_WIDTH = 600
#Hauteur de fenêtre
WINDOW_HEIGHT = 600
#Nom de fenêtre
pygame.display.set_caption("McGyver IS BACK")
#Déclaration de la variable de fenêtre
win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 0, 32)
#run à True pour la boucle while du jeu qui se base sur la valeur de run
run = True

#Cette méthode gère les déplacements
def move(press):
    #global permet d'utiliser les variables définies hors de move()
    global mg
    global grid
    global total
    global finish
    global winning

    #Si on rencontre le gardien c'est la fin de la partie, on n'accepte plus les input
    # on sort de la méthode (on n'a plus à se déplacer) par return
    if finish:
        return

    #En fonction de la touche sur laquelle on a appluyé si la case sur laquelle on veut aller
    # est bien dans l'étendue autorisée (abscisse et ordonnée de 0 à 14)
    # et n'est pas un mur alors
    # Si c'est celle du gardien on évalue le total(des objets ramassés) pour savoir si on a gagné ou perdu
    #Et on immobilise le joueur si le jeu est fini (while->event->move->redraw).    
    if press == "U":
        #Ordonnée -1
        if (mg[1] - 1) >= 0 and (mg[1] - 1) < 15  and grid[mg[0]][mg[1]-1] != "X":
            if grid[mg[0]][mg[1]-1] == "G":
                if total == 3:
                    winning = True
                finish = True

            if grid[mg[0]][mg[1]-1] in objects:
                total = total + 1
            grid[mg[0]][mg[1]-1] = "M"
            grid[mg[0]][mg[1]] = "0"
            mg = [mg[0],mg[1]-1]

    if press == "D":
        #Ordonnée +1
        if (mg[1] + 1) >= 0 and (mg[1] + 1) < 15 and grid[mg[0]][mg[1]+1] != "X":
            if grid[mg[0]][mg[1]+1] == "G":
                if total == 3:
                    winning = True
                finish = True

            if grid[mg[0]][mg[1]+1] in objects:
                total = total + 1
            grid[mg[0]][mg[1]+1] = "M"
            grid[mg[0]][mg[1]] = "0"
            mg = [mg[0],mg[1]+1]

    if press == "L":
        #Abscisse -1
        if (mg[0] - 1) >= 0 and grid[mg[0]-1][mg[1]] != "X":
            if grid[mg[0]-1][mg[1]] == "G":
                if total == 3:
                    winning = True
                finish = True           
            
            if grid[mg[0]-1][mg[1]] in objects:
                total = total + 1
            grid[mg[0]-1][mg[1]] = "M"
            grid[mg[0]][mg[1]] = "0"
            mg = [mg[0]-1,mg[1]]
        
    if press == "R":
        #Abscisse +1
        if (mg[0] + 1) < 15 and grid[mg[0]+1][mg[1]] != "X":
            if grid[mg[0]+1][mg[1]] == "G":
                if total == 3:
                    winning = True
                finish = True
            
            if grid[mg[0]+1][mg[1]] in objects:
                total = total + 1          
            grid[mg[0]+1][mg[1]] = "M"
            grid[mg[0]][mg[1]] = "0"
            mg = [mg[0]+1,mg[1]]

    #Lorsque la case est pratiquable et que ce n'est pas celle du gardien
    #On met "M" (McGyver) à la place du vide ("0") sur la case de destination
    #On remplace "M" par "0" sur la case d'origine (où nous nous trouvons)
    #Si elle contient un objet on incrémente la variable total

    #On prend en compte le déplacement en affichant la modification des position
    #dans la fenêtre pygame en appelant redraw()
    redraw()

#redraw() fonction gère l'affichage des cases du décor, des personnages et des déplacements
#dans la fenêtre pygame
def redraw():
    #Pour chaque case générée à partir de la matrice ? en fonction de carractère correspondant dans structure.txt
    #On lui assigne une image et une surface (une hauteur et une largeur)
    for i in range(15):
        for j in range(15):
            if grid[i][j] == "0":
                win.blit(floor, (i*width, j*height))
            if grid[i][j] == "X":
                win.blit(wall, (i*width, j*height))
            if grid[i][j] == "M":
                win.blit(mac, (i*width, j*height))
            if grid[i][j] == "G":
                win.blit(guardian, (i*width, j*height))
            if grid[i][j] == "E":
                win.blit(ether, (i*width, j*height))
            if grid[i][j] == "A":
                win.blit(needle, (i*width, j*height))
            if grid[i][j] == "T":
                win.blit(tube, (i*width, j*height))
            if total == 3:
                win.blit(serynge, (14*width, 0*height))
            #La fenêtre affiche aussi en fin de partie si on a gagné ou perdu à la moitié de l'écran
            if finish:
                myfont = pygame.font.SysFont("monospace", 15)
                if winning:
                    label = myfont.render("YOU WIN!", 1, (0,255,0))
                    win.blit(label, (WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
                else:
                    label = myfont.render("GAME OVER WEAK SCOTTISH!!!", 1, (255,0,0))
                    win.blit(label, (WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
    #On met à jour ce qui s'affiche à l'écran (appelé à chaque nouveau déplacement)
    pygame.display.update()

#Pendant toute l'exécution du programme on va écouter des événements
while run:
    for event in pygame.event.get():
        #Clic de fermeture de fenêtre
        if event.type == pygame.QUIT:
            run = False

        #Pression sur une flèche de direction
        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()

            if keys[pygame.K_LEFT]:
                move("L")

            if keys[pygame.K_RIGHT]:
                move("R")

            if keys[pygame.K_UP]:
                move("U")

            if keys[pygame.K_DOWN]:
                move("D")