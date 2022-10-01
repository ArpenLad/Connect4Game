import pygame as pg
from math import sqrt


class Circle:
    def __init__(self, x, y, r, shift, color="white"):
        self.radius = r
        self.x = x
        self.y = y
        self.color = color
        self.shift = shift
        self.pgCircle = ""
        self.hasCheker = False

    def display_circle(self, screen, doShift=True):
        if doShift:
            display_x = self.x * self.shift + 2 * self.radius
            display_y = self.y * self.shift + 2 * self.radius + 100
        else:
            display_x = self.x
            display_y = self.y
        self.pgCircle = pg.draw.circle(screen, color=self.color, center=(display_x, display_y), radius=self.radius)

    def insideCircle(self, x, y):
        x = (x - 2 * self.radius) / self.shift
        y = (y - 2 * self.radius - 100) / self.shift
        d = sqrt((x - self.x) ** 2 + (y - self.y) ** 2)
        return d < self.radius
