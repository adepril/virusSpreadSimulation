from tkinter import *
import random

#courbes
from matplotlib import pyplot as plt
fig = plt.figure()


WIN_W = 700
WIN_H = 600
POPULATION = 100
contamines_au_depart = 3
rayon_contamination = 12
duree_maladie = 500
SIZE=5
go=True
COULEUR_CONTAMINE = "red"
COULEUR_SAINT = "DarkOliveGreen2"
COULEUR_RETABLI = "green"

# construction de la fenetre 
mainWindow = Tk()
mainWindow.title("Animation")
mainWindow.geometry(str(WIN_W)+'x'+str(WIN_H))

bottomFrame = Frame(mainWindow)
label1 = Label(bottomFrame)
label1.grid(row = 0, column = 1, padx = 2)
label2 = Label(bottomFrame)
label2.grid(row = 0, column = 2, padx = 2)
label3 = Label(bottomFrame)
label3.grid(row = 0, column = 3, padx = 2)
bottomFrame.pack(side = TOP)

topFrame = Frame(mainWindow)
canvas = Canvas(topFrame, width=WIN_W, height=WIN_H, bg='white', bd=2)
canvas.grid(row = 0, column = 1)
topFrame.pack(side = BOTTOM)

class Individu:
    def __init__(self, canvas, id, x, y, vspd, hspd, color="green", size=5):
        self.id = id
        self.x = x 
        self.y = y
        self.vspd = vspd
        self.hspd = hspd
        self.size = size
        self.duree_infection = 0
        
        if (len(contamines) < contamines_au_depart):
            self.cont = True # contamine
            self.color = COULEUR_CONTAMINE
            contamines.append(self)
        else:
            self.cont = False  # non contamine
            self.color = color
            nonContamines.append(self)
    
        # création de la représentation graphique de l'individu
        self.instance = canvas.create_oval(self.x-size, self.y-size, self.x+size, self.y+size, fill = self.color)

    def update(self, _canvas):
        self.x += self.hspd
        self.y += self.vspd

        if (self.x+self.size < 0 or self.x+self.size > WIN_W):
            self.hspd *= -1

        if (self.y + self.size< 0 or self.y + self.size > WIN_H):
            self.vspd *= -1

        # update la position de l'individu
        canvas.coords(self.instance, self.x-self.size, self.y-self.size, self.x+self.size, self.y+self.size)
        # update la couleur de l'individu
        canvas.itemconfig(self.instance, fill=self.color)
       
    def analyser(self):
        if (self in nonContamines):
            #print("ID : ",self.id)
            for contamine in contamines:
                dist = ((self.x - contamine.x)**2 + (self.y - contamine.y)**2)**0.5
                if(dist < rayon_contamination):
                    self.cont = True
                    self.color = COULEUR_CONTAMINE
                    contamines.append(self)
                    nonContamines.remove(self)
                    break        

        if self.cont:
            self.duree_infection += 1
            if self.duree_infection > duree_maladie:
                #retablissement
                self.cont = False
                self.color = COULEUR_RETABLI 
                contamines.remove(self)
                immunises.append(self)


individus = []
contamines = []
nonContamines = []
immunises = []
nb_cont = []
nb_nonCont = []
nb_immun = []

#Création de la population
for i in range(0, POPULATION):
    x = random.randint(0,WIN_W)
    y = random.randint(0,WIN_H)
    vspd = random.random()*2-1
    hspd = random.random()*2-1
    individus.append(Individu(canvas, i, x, y, vspd, hspd, color = COULEUR_SAINT, size=SIZE))


# boucle d'animation
def draw():
    global go
    for i in range(0, len(individus)):
        individus[i].analyser()
        label2.configure(text='Non contaminés : '+str(len(nonContamines)))
        label3.configure(text='Contaminés : '+str(len(contamines)))
        individus[i].update(canvas)
    
    nb_cont.append(len(contamines))
    nb_nonCont.append(len(nonContamines))
    nb_immun.append(len(immunises ))

    if (len(contamines)) > 0 and (len(nonContamines)>0):
        mainWindow.after(10, draw)
    else:
        go=False

#Chronometre
sec = 0
def tick():
    if go:
        global sec
        sec += 1
        sec = round(sec)
        label1.configure(text='Jours : '+str(sec))
        mainWindow.after(1000, tick)


#lancement du programme 
draw()
tick()
mainWindow.mainloop()

plt.plot(nb_cont, c=(0.58, 0.78, 0), label='Infectés')
plt.plot(nb_nonCont, c=(0, 0.58, 0.78), label='Susceptibles d''être infectés')
plt.plot(nb_immun, c=(0.58, 0.78, 0.58), label='Rétablies')
plt.legend()
plt.show()
