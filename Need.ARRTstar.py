import Need.RRTSTAR as RRTSTAR
import pygame
import time



NT=30
red = (255, 0, 0)
green = (0, 255, 0)
bleu = (0, 0, 255)
grey = (0, 0, 0)
yallow = (255, 255, 0)
echel= 2




class A_RRT_STAR_Methode(RRTSTAR.RRT_STAR_Methode):

    def RandRef(self,points):
        flag = True
        Prand = self.goal
        while flag:
            Pnear = self.near_point(Prand,points)
            Pnew=self.give_point_new(Pnear,Prand)
            if self.freetrajet(Pnear, Pnew):
                flag = False
            else:
                Prand = self.Rand()
        return Prand, Pnear,Pnew

    def ChooseRand(self,points):

        Prand, Pnear,Pnews = self.RandRef(points)
        d = self.distance(Prand, Pnear) + 1 * self.distance(Prand, self.goal)
        for k in range(NT):
            Pr = self.Rand()
            Pn = self.near_point(Pr,points)
            Pnew=self.give_point_new(Pn,Pr)
            di = self.distance(Pr, Pn) + 1 * self.distance(Pr, self.goal)
            if di < d and self.freetrajet(Pn, Pnew) and self.distance(Pn, Pr) > 2 * self.pas:
                Prand, Pnear, d ,Pnews= Pr, Pn, di,Pnew
        return Pnear,Pnews

    def avancer(self,points,conexion):

        pnear,pnew = self.ChooseRand(points)
        pointsnears = self.get_Near(pnew,points)
        pnear = self.chose_parent_RRT_star(pnear, pnew, pointsnears,conexion)
        pygame.draw.circle(self.MAP, green, pnew, 3, 0)
        pygame.draw.line(self.MAP, bleu, pnear, pnew, 1)
        points.append(pnew)
        conexion[pnew] = pnear
        self.Rewer(pnew, pointsnears,conexion)
        pygame.display.update()
        return (self.arriver(pnew))


    def Excute(self):
        conextion={}
        points=[self.start]
        conextion[self.start] = self.start

        t = time.time()
        etat = True
        while etat:
            etat = self.avancer(points,conextion)
        t = time.time() - t
        traget = self.get_trajet(self.goal,conextion)
        self.Draw_trajet(traget)
        cout = self.couttrajet(traget)
        print("***********************************************************")
        print(t, cout, len(points))
        return traget
        """for p in points:
            pygame.draw.circle(MAP, green, p, 4, 0)
            pygame.draw.line(MAP, bleu, p, conextion[p], 2)
            pygame.display.update()
        pygame.draw.circle(MAP, green, Start, 8, 0)"""


    def ExcTest(self):
        conextion={}
        points=[self.start]
        conextion[self.start] = self.start

        t = time.time()
        etat = True
        while etat:
            etat = self.avancer(points,conextion)
        t = time.time() - t
        traget = self.get_trajet(self.goal,conextion)
        self.Draw_trajet(traget)
        cout = self.couttrajet(traget)
        #print("***********************************************************")
        return (t, cout, len(points))
