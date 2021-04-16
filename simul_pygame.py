import pygame
from matplotlib import pyplot as plt
from random import randint, random, randrange

WIN_W = 1000
WIN_H = 800

win = pygame.display.set_mode((WIN_W, WIN_H))
pygame.display.set_caption("Simulation Covid19")
win.fill((255,255,255))

#courbes
fig = plt.figure()

# Parametres 
vitesse = 3
pop_depart = 100
cont_depart = 1
cont_rad = 20
fps = 30
duree_maladie = 8
COULEUR_CONTAMINE = (250, 50, 0)
COULEUR_SAINT = (0, 50, 250)
COULEUR_RETABLI = (0, 200, 200)

#Création des individus
individus = []
contamines = []
nb_cont = []
susceptibles = []
nb_susc = []
retablies = []
nb_ret = []


for ID in range(pop_depart):
    indiv = {}

    x = randint(30, WIN_W-30)
    indiv['x'] = x

    y= randint(30, WIN_H-30)
    indiv['y'] = y

    vx = random() * vitesse * 2
    vx -= vitesse
    indiv['vx'] = vx

    vy = (vitesse**2 - vx**2)**0.5
    signe = randrange(-1,2,2) #retourne -1 ou 1
    indiv['vy'] = signe*vy

    if len(contamines) < cont_depart:
        indiv['cont'] = True
        indiv['couleur'] = COULEUR_CONTAMINE 
        indiv['duree_infection'] = 0
        contamines.append(ID)
    else:
        indiv['cont'] = False
        indiv['couleur'] = COULEUR_SAINT 
        indiv['duree_infection'] = 0
        susceptibles.append(ID)

    individus.append(indiv)

def afficher(indiv, win):
    _couleur = indiv['couleur']
    _x = indiv['x']
    _y = indiv['y']
    pygame.draw.circle(win,_couleur, (round(_x),round(_y)), 7)
    if indiv['cont']:
        pygame.draw.circle(win,_couleur, (round(_x),round(_y)), cont_rad, 1)
    

def deplacer(indiv):
    if indiv['x'] < 20 or indiv['x'] > WIN_W-20:
        indiv['vx'] *= -1

    if indiv['y'] < 20 or indiv['y'] > WIN_H-20:
        indiv['vy'] *= -1

    indiv['x'] += indiv['vx']
    indiv['y'] += indiv['vy']

def analyser(id):
    indiv = individus[id]
    if id in susceptibles:
        for IDinfecte in contamines:
            indivInfect = individus[IDinfecte]
            dist = ((indiv['x'] - indivInfect['x'])**2 + (indiv['y'] - indivInfect['y'])**2)**0.5
            if dist < cont_rad:
                indiv['cont'] = True
                indiv['couleur'] = (250, 50, 0)
                indiv['duree_infection'] = 0
                break
          
        if indiv['cont']:
            contamines.append(id)
            susceptibles.remove(id)

    if indiv['cont']:
        indiv['duree_infection'] += 1
        if indiv['duree_infection'] > fps * duree_maladie:
            #retablissement
            indiv['cont'] = False
            indiv['couleur'] = COULEUR_RETABLI 
            contamines.remove(id)
            retablies.append(id)

#Boucle de pygame
clock = pygame.time.Clock()
sim_active = True
while sim_active:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sim_active = False
            pygame.quit()

    if not(sim_active):
        break

    win.fill((255, 255, 255))
    
    for indiv in individus:
        deplacer(indiv)

    for id in range(pop_depart):
        analyser(id)

    for indiv in individus:
        afficher(indiv, win)

    nb_cont.append(len(contamines))
    nb_susc.append(len(susceptibles))
    nb_ret.append(len(retablies ))

    pygame.display.update()
    clock.tick(fps)

plt.plot(nb_cont, c=(0.58, 0.78, 0), label='Infectés')
plt.plot(nb_susc, c=(0, 0.58, 0.78), label='Susceptibles d''être infectés')
plt.plot(nb_ret, c=(0.58, 0.78, 0.58), label='Rétablies')
plt.legend()
plt.show()

