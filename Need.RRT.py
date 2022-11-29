import random
import pygame
import time







red = (255, 0, 0)
green = (0, 255, 0)
bleu = (0, 0, 255)
grey = (0, 0, 0)
yallow = (255, 255, 0)
echel= 2








class RRT_Methode:

    def __init__(self, pas,Map):

        self.pas = echel * pas
        self.MAP=Map.Map
        self.start=Map.start
        self.goal=Map.goal
        self.rect=Map.rect

    def Rand(self):
        pointdone = True
        while pointdone:
            x, y = random.uniform(0, echel * 530), random.uniform(0, echel * 530)
            colid = (r.collidepoint(x, y) for r in self.rect)
            if sum(colid) == 0:
                pointdone = False
        return (x, y)

    def distance(self, p1, p2):
        return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5

    def near_point(self, point,points):
        #print("nombre de point:     ",len(points))
        distances = [self.distance(point, p) for p in points]
        return points[distances.index(min(distances))]

    def arriver(self, point):
        if self.distance(point, self.goal) > (self.pas - 0.000000000001):
            return True
        else:
            return False

    def give_point_new(self, point1, point2):
        if self.distance(point1, point2) > self.pas:
            u = self.pas / self.distance(point1, point2)
            x1, y1, x2, y2 = point1[0], point1[1], point2[0], point2[1]
            x3, y3 = x1 + u * (x2 - x1), y1 + u * (y2 - y1)

            if self.arriver((x3, y3)):
                return (x3, y3)
            else:
                return self.goal
        else:
            if self.arriver(point2):
                return point2
            else:
                return self.goal

    def freetrajet(self, point1, point2):
        x1, y1, x2, y2 = point1[0], point1[1], point2[0], point2[1]
        a = (y2 - y1) / (x2 - x1)
        b = y1 - a * x1
        u = (x2 - x1) / 100
        for i in range(100):
            x = x1 + i * u
            y = a * x + b
            colid = (r.collidepoint(x, y) for r in self.rect)
            if sum(colid)>0:
                return False
        return True

    def avancer(self,points,conextion):
        prand = self.Rand()
        pnear = self.near_point(prand,points)
        pnew = self.give_point_new(pnear, prand)
        if self.freetrajet(pnear, pnew):
            pygame.draw.circle(self.MAP, red, pnew, 4, 0)
            pygame.draw.line(self.MAP, bleu, pnear, pnew, 2)
            points.append(pnew)
            conextion[pnew] = pnear
            pygame.display.update()
            return (self.arriver(pnew))
        else:
            return True

    def get_trajet(self, point,conexion):
        traget = [point]
        point_test = point
        while point_test != self.start:
            traget.append(conexion[point_test])
            point_test = traget[-1]
        return traget[::-1]

    def couttrajet(self, trajet):
        cout = 0
        for i in range(len(trajet) - 1):
            cout += self.distance(trajet[i], trajet[i + 1])
        return cout

    def Draw_trajet(self, traget):
        for i in range(len(traget)-1):
            pygame.draw.circle(self.MAP, green, traget[i], 6, 0)
            pygame.draw.line(self.MAP, green, traget[i], traget[i+1], 4)
        pygame.draw.circle(self.MAP, green, traget[-1], 10, 0)
        pygame.display.update()
        #time.sleep(1.1)

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
        print( t,cout,len(points))