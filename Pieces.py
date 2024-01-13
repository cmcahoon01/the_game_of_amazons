import pygame
from io import BytesIO

style = "Spatial"
whiteQueenPath = f"images/whiteQueen{style}.svg"
blackQueenPath = f"images/blackQueen{style}.svg"
queenImages = [pygame.image.load(whiteQueenPath),
               pygame.image.load(blackQueenPath)]

PADDING = 0.1  # padding as a percentage of the tile size


class Piece:
    type = None

    def __init__(self, x, y, scale, color=None):
        self.x = x
        self.y = y
        self.color = color
        self.scale = scale

    def draw(self, screen):
        pass

    def __str__(self):
        return (self.type if self.type else "None") + " at " + str(self.x) + ", " + str(self.y)

    def __repr__(self):
        return self.__str__()


class Queen(Piece):
    type = "queen"

    def draw(self, screen):
        image = queenImages[0 if self.color == "white" else 1]
        scale_with_padding = self.scale * (1 - PADDING * 2)
        image = pygame.transform.scale(image, (scale_with_padding, scale_with_padding))
        screen.blit(image, (self.x * self.scale + self.scale * PADDING,
                            self.y * self.scale + self.scale * PADDING))

    def move(self, x, y):
        self.x = x
        self.y = y


class Arrow(Piece):
    type = "arrow"

    def draw(self, screen):
        pass
