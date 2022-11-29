import time

import MAP as M
import pygame
import pandas as pd
import numpy as np
import random

from tkinter import *

from sklearn.model_selection import train_test_split,cross_val_score,KFold
from sklearn.pipeline import make_pipeline
from xgboost import XGBClassifier
from sklearn.preprocessing import StandardScaler,MaxAbsScaler
from sklearn.compose import make_column_transformer

from sklearn.ensemble import RandomForestClassifier,AdaBoostClassifier,ExtraTreesClassifier
from sklearn.neighbors import KNeighborsClassifier



#**************************** DEF VARIABLE***************************************************

red = (255, 0, 0)
green = (0, 255, 0)
bleu = (0, 0, 255)
grey = (0, 0, 0)
yallow = (255, 255, 0)

echel=2
NuObs=70

MAP=None
Matrice=None

#**************************** PHASE D ENTRAINMENT ***************************************************

#subsample=0.8,min_child_weight=7,max_depth=4,gamma=2.5,colsample_bytree=0.8

Data=pd.read_excel("xTRAITER.xlsx")
Ydata=np.ravel(Data.iloc[:,10:])
Xdata=Data.iloc[:,:10]

model4=XGBClassifier(subsample=0.8,min_child_weight=7,max_depth=4,gamma=2.5,colsample_bytree=0.8)
preposeseur=make_column_transformer((StandardScaler(),["C0","C1","C2","C3","C4","C5","C6","C7"]),(MaxAbsScaler(),["Dx","Dy"]))
model=make_pipeline(preposeseur,model4)

model.fit(Xdata,Ydata)
cv=KFold(2)
print(cross_val_score(model,Xdata,Ydata,cv=cv))

#**************************** PHASE D TEST ROBOT ***************************************************

def Draw_position(p,coleur):
    rectangle = pygame.Rect(p, (20, 20))
    pygame.draw.rect(MAP.Map, coleur, rectangle)
    pygame.display.update()


def get_sortie_capteur(p,map):
    global Matrice
    matrice=Matrice


    I = [0 for j in range(8)]
    M = 53

#                    I0                  #

    x, y = int(p[0] / 20), int(p[1] / 20)
    k = 1
    while (k < M):
        yv = y - k
        if yv < 0:
            k = M
        else:

            if matrice[x][yv] == 0:
                I[0] = k
            else:
                k = M
        k = k + 1

#                    I1                  #

    x, y = int(p[0] / 20), int(p[1] / 20)
    k = 1
    while (k < M):
        yv = y - k
        xv = x + k
        if yv < 0 or xv > 52:
            k = M
        else:

            if matrice[xv][yv] == 0:
                I[1] = k
            else:
                k = M
        k = k + 1

#                    I2                  #

    x, y = int(p[0] / 20), int(p[1] / 20)
    k = 1
    while (k < M):
        yv = y
        xv = x + k
        if xv > 52:
            k = M
        else:

            if matrice[xv][yv] == 0:
                I[2] = k
            else:
                k = M
        k = k + 1

#                    I3                  #

    x, y = int(p[0] / 20), int(p[1] / 20)
    k = 1
    while (k < M):
        yv = y + k
        xv = x + k
        if yv > 52 or xv > 52:
            k = M
        else:

            if matrice[xv][yv] == 0:
                I[3] = k
            else:
                k = M
        k = k + 1

#                    I4                  #

    x, y = int(p[0] / 20), int(p[1] / 20)
    k = 1
    while (k < M):
        yv = y + k
        xv = x
        if yv > 52:
            k = M
        else:

            if matrice[xv][yv] == 0:
                I[4] = k
            else:
                k = M
        k = k + 1

#                    I5                  #

    x, y = int(p[0] / 20), int(p[1] / 20)
    k = 1
    while (k < M):
        yv = y + k
        xv = x - k
        if xv < 0 or yv > 52:
            k = M
        else:

            if matrice[xv][yv] == 0:
                I[5] = k
            else:
                k = M
        k = k + 1

#                    I6                  #

    x, y = int(p[0] / 20), int(p[1] / 20)
    k = 1
    while (k < M):
        yv = y
        xv = x - k
        if xv < 0:
            k = M
        else:

            if matrice[xv][yv] == 0:
                I[6] = k
            else:
                k = M
        k = k + 1

#                    I7                  #

    x, y = int(p[0] / 20), int(p[1] / 20)
    k = 1
    while (k < M):
        yv = y - k
        xv = x - k
        if xv < 0 or yv < 0:
            k = M
        else:

            if matrice[xv][yv] == 0:
                I[7] = k
            else:
                k = M
        k = k + 1




    I.append((-p[0]+map.goal[0])/10)
    I.append((-p[1]+map.goal[1])/10)

    #print(I, "     ", (x, y), "    ", (xdirection, ydirection), "    ", p)
    I=pd.DataFrame(np.array(I).reshape(1,10),columns = [["C0","C1","C2","C3","C4","C5","C6","C7","Dx","Dy"]])
    return I


def nonColision(point):
    colid = (r.collidepoint(point) for r in MAP.rect)
    if sum(colid) == 0 and abs(point[0])<1041 and abs(point[1])<1041:
        return True
    else:
        return False


def get_action(donnes_capteur,pos,position):
    y_proba=model.predict_proba(donnes_capteur).tolist()[0]


    etat=True
    while etat:
        Y = y_proba.index(max(y_proba))
        if Y==8:
            return Y
        else:
            y_proba[8]=0
            newpos=excuter_action(pos,Y,False)

            if nonColision(newpos) and not(newpos in position):
                return Y
            else:
                if sum(y_proba)==0:
                    et=True
                    y_proba = model.predict_proba(donnes_capteur).tolist()[0]
                    while et:
                        Y = y_proba.index(max(y_proba))
                        newpos=excuter_action(pos,Y,False)
                        if nonColision(newpos):
                            return Y
                        else:
                            y_proba[Y] = 0
                else:
                    y_proba[Y]=0
    return y_proba.index(max(y_proba))


def excuter_action(pos,action,etat):
    if action==0:
        new_pos=(pos[0],pos[1]-20)
    if action==1:
        new_pos = (pos[0]+20, pos[1] - 20)
    if action==2:
        new_pos = (pos[0]+20, pos[1])
    if action==3:
        new_pos = (pos[0] + 20, pos[1]+20)
    if action==4:
        new_pos = (pos[0] , pos[1]+20)
    if action==5:
        new_pos = (pos[0]- 20, pos[1]+20)
    if action==6:
        new_pos = (pos[0]-20, pos[1])
    if action==7:
        new_pos = (pos[0] - 20, pos[1]-20)
    if action == 8:
        new_pos = pos
    if etat==True:
        #Draw_position(new_pos,yallow)
        pygame.draw.circle(MAP.Map, green, (new_pos[0]+10,new_pos[1]+10), 5, 0)
        pygame.draw.line(MAP.Map,green,(pos[0]+10,pos[1]+10),(new_pos[0]+10,new_pos[1]+10),3)
        pygame.display.update()
        time.sleep(0.1)

    return new_pos


def Lancer_robot():
    position=[]
    actions = []
    global MAP


    k=0
    pos = excuter_action(MAP.start, 8,True)
    position.append(pos)
    donnes_capteurs = get_sortie_capteur(pos, MAP)
    action=get_action(donnes_capteurs,pos,position)
    actions.append(action)
    pos = excuter_action(pos, action,True)
    position.append(pos)
    while action!=8:
        donnes_capteurs = get_sortie_capteur(pos, MAP)
        action = get_action(donnes_capteurs,pos,position)
        actions.append(action)
        pos=excuter_action(pos,action,True)
        position.append(pos)
        if nonColision(pos):
            pass
        else:
            print("colision")
            print(action)
            print(pos)
            return "C"
        k=k+1
        if k==120:
            print("Robot dakh")
            return "R"
    return 1


def givepoint():
    x = int(random.uniform(20, 490)/20)*20
    y = int(random.uniform(20, 490)/20)*20
    return (x, y)


def Extraxt(St,Go):
    global MAP
    global Matrice
    PositionMAP = [givepoint() for i in range(NuObs)]
    TailleMAP = [(random.choice([20,30]), random.choice([20,30])) for i in range(NuObs)]
    MAP = M.Map(St, Go, (530, 530), "MAP 1", PositionMAP, TailleMAP, echel)
    MAP.DrawMap()
    Matrice = MAP.get_Matrice_Map()
    result=Lancer_robot()
    return result




res=[]
k=0
while(k<50):
    resK=[]
    print("**********************  ",k,"   ************************")
    k = k + 1
    l=0
    try:
        EX=Extraxt((10,10),(520,520))
        if EX=="C" or EX=="R" or EX==1:
            #pygame.image.save(MAP.Map, "image" + str(k) + "--" + str(l) + ".png")
            pass
        resK.append(EX)

        l=l+1

        EX = Extraxt((520, 520),(10, 10))
        if EX=="C" or EX=="R" or EX==1:
            #pygame.image.save(MAP.Map, "image" + str(k) + "--" + str(l) + ".png")
            pass
        resK.append(EX)

        l=l+1

        EX = Extraxt((10,520), (520,10))
        if EX=="C" or EX=="R" or EX==1:
            #pygame.image.save(MAP.Map, "image" + str(k) + "--" + str(l) + ".png")
            pass
        resK.append(EX)

        l=l+1

        EX = Extraxt((520,10),(10,520))
        if EX=="C" or EX=="R" or EX==1:
            #pygame.image.save(MAP.Map, "image" + str(k) + "--" + str(l) + ".png")
            pass
        resK.append(EX)

        l=l+1

        EX = Extraxt((250,10),(251,520))
        if EX=="C" or EX=="R" or EX==1:
            #pygame.image.save(MAP.Map, "image" + str(k) + "--" + str(l) + ".png")
            pass
        resK.append(EX)

        l=l+1

        EX = Extraxt((10,250),(520,250))
        if EX=="C" or EX=="R" or EX==1:
            #pygame.image.save(MAP.Map, "image" + str(k) + "--" + str(l) + ".png")
            pass
        resK.append(EX)

        l=l+1

        EX = Extraxt((250,520),(251,10))
        if EX=="C" or EX=="R" or EX==1:
            #pygame.image.save(MAP.Map, "image" + str(k) + "--" + str(l) + ".png")
            pass
        resK.append(EX)
        l=l+1

        EX = Extraxt((520,250),(10,250))
        if EX=="C" or EX=="R" or EX==1:
            #pygame.image.save(MAP.Map, "image" + str(k) + "--" + str(l) + ".png")
            pass
        resK.append(EX)

        l=l+1

        for i in resK:
            res.append(i)

    except:
        k=k-1


print(res.count("R"))
print(res.count("C"))
print(res.count(1))
print(res)

print(len(res))








