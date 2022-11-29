import Need.ARRTstar as ARRTstar
import pygame
import time

NT=30
red = (255, 0, 0)
green = (0, 255, 0)
bleu = (0, 0, 255)
grey = (0, 0, 0)
yallow = (255, 255, 0)
echel= 2
Pas=10*echel


class VARRTstar_Methode(ARRTstar.A_RRT_STAR_Methode):
    def RandRef(self,points):
        flag = True
        Prand = self.Rand()
        while flag:
            Pnear = self.near_point(Prand,points)
            #Pnew=self.give_point_new(Pnear,Prand)
            if self.freetrajet(Pnear, Prand):
                flag = False
            else:
                Prand = self.Rand()
        return Prand, Pnear


    def ChooseRand(self,points):
        Prand, Pnear = self.RandRef(points)
        d = self.distance(Prand, Pnear) + 1 * self.distance(Prand, self.goal)
        for k in range(NT):
            #print("le K est : ",k)
            Pr=self.Rand()
            Pn = self.near_point(Pr,points)
            di = self.distance(Pr, Pn) + 1 * self.distance(Pr, self.goal)
            if self.distance(Pr,self.goal)>2*Pas:
                if di < d and self.freetrajet(Pn, Pr) and self.distance(Pn, Pr) > 2*self.pas:
                    Prand, Pnear, d = Pr, Pn, di
            else:
                if di < d and self.freetrajet(Pn, Pr):
                    Prand, Pnear, d = Pr, Pn, di
        return Prand, Pnear


    def avancer(self,points,conextion):

        prand, pnear = self.ChooseRand(points)
        self.pas=9*self.pas*self.distance(pnear,prand)/self.distance(pnear,self.goal)
        pnew = self.give_point_new(pnear, prand)
        self.pas=Pas
        X=self.freetrajet(pnear, pnew)
        #print(prand,"****",pnew)
        #print("la valeur de X est :", X)
        if X:
            pointsnears = self.get_Near(pnew,points)
            pnear = self.chose_parent_RRT_star(pnear, pnew, pointsnears,conextion)
            s = int(self.distance(pnear,pnew) / 15)
            if s==0:
                S=[(round(pnew[0],4),round(pnew[1],4))]
                points.append(S[-1])
                conextion[S[-1]] = pnear

            else:
                S = [(round((k * pnew[0] + (s - k) * pnear[0]) / s,4) , round(((k * pnew[1] + (s - k) * pnear[1]) / s),4)) for k in
                 range(0, s + 1)]
            for k in range(1,len(S)):
                points.append(S[k])
                conextion[S[k]] = S[k-1]
                #pygame.draw.circle(MAP, green, S[k], 4, 0)


            pygame.draw.circle(self.MAP, red, pnew, 4, 0)
            pygame.draw.line(self.MAP, bleu, pnear, pnew, 1)
            pygame.display.update()
            pointsnears = self.get_Near(pnew,points)
            self.Rewer(S[-1], pointsnears,conextion)
            #pygame.display.update()
            return (self.arriver(pnew))
        else:
            #print("jawad")
            return True


POINTS1=[]
POINTS2=[]
Connection1={}
Connection2={}










