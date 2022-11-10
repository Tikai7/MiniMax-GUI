
import pygame
import Tree
import Search

from collections import deque
from pygame import gfxdraw

pygame.font.init()

VALUES = deque([10, 5, 7, 11, 12, 8, 9, 8, 5, 12, 11, 12, 9, 8, 7, 10])
COLOR = (255, 255, 255)
THICKNESS = 1
RAYON = 25


def render_tree(root: Tree.Node):
    if root is not None:
        render_tree(root.left_child)
        draw_noeud(surface, root.position, root.value)
        if root.parent is not None:
            draw_link(surface, root.position, root.parent.position)
        render_tree(root.right_child)


def build_tree():
    root = Tree.Node(None, 0, None)
    root.add_value(VALUES)
    return root


def draw_noeud(surface, position, value):
    x, y = position
    # pygame.draw.circle(surface, COLOR, position, RAYON, THICKNESS)
    gfxdraw.aacircle(surface, x, y, RAYON, COLOR)
    gfxdraw.filled_circle(surface, x, y, RAYON, COLOR)

    if value is not None:
        text = f"{value}"
        text_font = pygame.font.SysFont("Comic Sans MS", 15)
        text_render = text_font.render(text, False, (255, 255, 255))
        surface.blit(text_render, (x-5, y+RAYON*1.5))


def draw_link(surface, points_son, points_parent):
    x1, y1 = points_son
    x2, y2 = points_parent
    gfxdraw.line(
        surface, x1, y1, x2, y2, COLOR)


Launch = True
WIDTH = 1600
HEIGHT = 900

surface = pygame.display.set_mode((WIDTH, HEIGHT))  # pygame.RESIZABLE
surface.fill((23, 28, 38))

root = build_tree()
render_tree(root)

while Launch:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Launch = False

    Search.SearchAlgorithm.MiniMax(surface, root, 5, player=1)
