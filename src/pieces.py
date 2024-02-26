import pygame
from constants import MOVE_COLOR, SHOOT_COLOR, WALL_COLOR

style = "Spatial"
whiteQueenPath = f"../images/whiteQueen{style}.svg"
blackQueenPath = f"../images/blackQueen{style}.svg"
queenImages = [pygame.image.load(whiteQueenPath),
               pygame.image.load(blackQueenPath)]
# arrowImage = pygame.image.load("../images/arrow.svg")
whiteArrowPath = f"../images/whiteArrow.svg"
blackArrowPath = f"../images/blackArrow.svg"
arrowImages = [pygame.image.load(whiteArrowPath),
               pygame.image.load(blackArrowPath)]

PADDING = 0.1  # padding as a percentage of the tile size


class Piece:
    type = None

    def __init__(self, scale, color=None):
        self.color = color
        self.scale = scale

    def draw(self, screen, x, y):
        if self.color is None:
            return
        screen.fill(self.color,
                    (x * self.scale + self.scale * PADDING,
                     y * self.scale + self.scale * PADDING,
                     self.scale * (1 - PADDING * 2),
                     self.scale * (1 - PADDING * 2)))

    def __str__(self):
        return self.type if self.type else "None"

    def __repr__(self):
        return self.__str__()


class Queen(Piece):
    type = "queen"

    def draw(self, screen, x, y):
        image = queenImages[0 if self.color == "white" else 1]
        scale_with_padding = self.scale * (1 - PADDING * 2)
        image = pygame.transform.scale(image, (scale_with_padding, scale_with_padding))
        screen.blit(image, (x * self.scale + self.scale * PADDING,
                            y * self.scale + self.scale * PADDING))


class Arrow(Piece):
    type = "arrow"

    def draw(self, screen, x, y):
        image = arrowImages[0 if self.color == "white" else 1]
        grow = self.scale * 0.17

        image = pygame.transform.scale(image, (self.scale + grow, self.scale + grow))
        screen.blit(image, (x * self.scale - grow // 2,
                            y * self.scale - grow // 2))


class Selection(Piece):
    type = "selection"

    def draw(self, screen, x, y):
        if self.color:
            color = SHOOT_COLOR
        else:
            color = MOVE_COLOR
        pygame.draw.circle(screen, color,
                           (x * self.scale + self.scale // 2,
                            y * self.scale + self.scale // 2),
                           self.scale // 4)
