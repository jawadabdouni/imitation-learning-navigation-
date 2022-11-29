import pygame



red = (255, 0, 0)
green = (0, 255, 0)
bleu = (0, 0, 255)
grey = (0, 0, 0)
yallow = (255, 255, 0)





class Map:

    def __init__(self, start, goal, size, name, PositionObs, Taille, echel):
        self.echel = echel
        self.name = name
        self.start = (echel * start[0], echel * start[1])
        self.goal = (echel * goal[0], echel * goal[1])
        self.size = (echel * size[0], echel * size[1])
        self.PositionObs = PositionObs
        self.Taille = Taille
        pygame.display.set_caption(self.name)
        self.Map = pygame.display.set_mode(self.size)
        self.rect=[]

    def DrawMap(self):
        self.Map.fill((255, 255, 255))
        pygame.draw.circle(self.Map, green, self.start, 8, 0)
        pygame.draw.circle(self.Map, red, self.goal, 8, 0)

        for i in range(len(self.PositionObs)):
            rectangle = pygame.Rect((self.echel * self.PositionObs[i][0], self.echel * self.PositionObs[i][1]),
                                    (self.echel * self.Taille[i][0], self.echel * self.Taille[i][1]))
            self.rect.append(rectangle)
        for rectangle in self.rect:
            pygame.draw.rect(self.Map, grey, rectangle)
        pygame.display.update()

        #self.get_Matrice_Map()
        for k in range(1,53):
            pygame.draw.line(self.Map, red, (0,k*20), (1060,k*20), 1)
        for k in range(1,53):
            pygame.draw.line(self.Map, red, (k*20,0), (k*20,1060), 1)
        pygame.display.update()

    def get_Matrice_Map(self):
        matrice=[]
        for i in range(53):
            ligne=[]
            for j in range(53):
                X=10+i*20
                Y=10+j*20
                colid = [r.collidepoint(X,Y) for r in self.rect]
                if sum(colid) == 0:
                    ligne.append(0)
                else:
                    ligne.append(1)
            matrice.append(ligne)
        return matrice