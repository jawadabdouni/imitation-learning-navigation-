import Need.RRT as RRT
import pygame
import time
import math

NT=30
red = (255, 0, 0)
green = (0, 255, 0)
bleu = (0, 0, 255)
grey = (0, 0, 0)
yallow = (255, 255, 0)
landa=500



class RRT_STAR_Methode(RRT.RRT_Methode):

    def get_cost_point(self, point,conexion):
        trag = self.get_trajet(point,conexion)
        return self.couttrajet(trag)

    def get_Near(self, pnew,points):
        d = self.distance(self.start, self.goal)
        K = landa * (math.log(len(points)) / len(points)) ** (1 / d)
        pointsnears = []
        for p in points:
            if self.distance(p, pnew) < K and p != pnew:
                pointsnears.append(p)
        return pointsnears

    def chose_parent_RRT_star(self, pnear, pnew, pointsnears,conexion):
        d = self.get_cost_point(pnear,conexion) + self.distance(pnear, pnew)
        pn = pnear
        for p in pointsnears:
            dp = self.get_cost_point(p,conexion) + self.distance(p, pnew)
            if dp < d and self.freetrajet(p, pnew):
                d = dp
                pn = p
        return pn

    def Rewer(self, pnew, pointnears,conextion):
        for p in pointnears:
            parentP = conextion[p]
            d1 = self.get_cost_point(parentP,conextion) + self.distance(p, parentP)
            d2 = self.get_cost_point(pnew,conextion) + self.distance(p, pnew)
            if d1 > d2 and self.freetrajet(p, pnew):
                conextion[p] = pnew
                pygame.draw.line(self.MAP, (255, 255, 255), p, parentP, 2)
                pygame.draw.line(self.MAP, bleu, p, pnew, 2)

    def avancer(self,points,conextion):

        prand = self.Rand()
        pnear = self.near_point(prand,points)
        pnew = self.give_point_new(pnear, prand)
        if self.freetrajet(pnear, pnew):
            pointsnears = self.get_Near(pnew,points)
            pnear = self.chose_parent_RRT_star(pnear, pnew, pointsnears,conextion)
            points.append(pnew)
            conextion[pnew] = pnear
            pygame.draw.circle(self.MAP, red, pnew, 5, 0)
            pygame.draw.line(self.MAP, bleu, pnear, pnew, 2)
            self.Rewer(pnew, pointsnears,conextion)
            pygame.display.update()
            return (self.arriver(pnew))
        else:
            return True

    def Excute(self):

        conextion = {}
        points = [self.start]
        conextion[self.start] = self.start

        t = time.time()
        etat = True
        while etat:
            etat = self.avancer(points,conextion)
        t = time.time() - t
        traget = self.get_trajet(self.goal,conextion)
        pygame.display.update()
        self.Draw_trajet(traget)
        cout = self.couttrajet(traget)
        print("***********************************************************")
        print(t, cout, len(points))


        """for point, parent in conextion.items():
            pygame.draw.line(MAP, bleu, point, parent, 2)
            pygame.draw.circle(MAP, red, parent, 4, 0)
            pygame.draw.circle(MAP, red, point, 4, 0)
            pygame.display.update()"""

    def ExcTest(self):

        conextion = {}
        points = [self.start]
        conextion[self.start] = self.start

        t = time.time()
        etat = True
        while etat:
            etat = self.avancer(points,conextion)
        t = time.time() - t
        traget = self.get_trajet(self.goal,conextion)
        pygame.display.update()
        self.Draw_trajet(traget)
        cout = self.couttrajet(traget)

        return (t, cout, len(points))