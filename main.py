
import pygame
import pygame_menu
import Tree
import Search
import time

from collections import deque
from pygame import gfxdraw

pygame.init()
pygame.font.init()


VALUES = deque([10, 5, 7, 11, 12, 8, 9, 8, 5, 12, 11, 12, 9, 8, 7, 10])
# VALUES = deque([5, 2, 1, 4, 10, 12, 5, 13, -3, 22, 9, 12, 11, 10, 21, 20])

COLOR = (255, 255, 255)
THICKNESS = 1
RAYON = 25


Launch = True
Algo = 1
CURRENT_PLAYER = "Max"
player = CURRENT_PLAYER
PLAYER = 1


def launch_game():
    menu.clear()
    menu.disable()


def set_player(player_value, value):
    global CURRENT_PLAYER
    global PLAYER
    global player

    CURRENT_PLAYER = player_value[0][0]
    PLAYER = player_value[0][1]
    player = CURRENT_PLAYER


def set_algo(value, algo):
    global Algo
    Algo = algo


def render_tree(root: Tree.Node):
    if root is not None:
        render_tree(root.left_child)
        draw_noeud(surface, root.position, root.value)
        if root.parent is not None:
            draw_link(surface, root.position, root.parent.position)
        render_tree(root.right_child)
    return True


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


WIDTH = 1600
HEIGHT = 900
DEPTH = 5

surface = pygame.display.set_mode((WIDTH, HEIGHT))  # pygame.RESIZABLE
surface.fill((23, 28, 38))


menu = pygame_menu.Menu('Algorithm Simulation', WIDTH, HEIGHT,
                        theme=pygame_menu.themes.THEME_BLUE)

menu.add.selector(
    'Algorithm :',
    [
        ('Mini-Max', 1),
        ('Nega-Max', 2),
        ('Nega-Max with Alpha Beta', 3)
    ],
    onchange=set_algo,
)

menu.add.selector(
    'Player :',
    [
        ('Max', 1),
        ('Min', -1)
    ],
    onchange=set_player,
)

menu.add.button('Play', launch_game)
menu.add.button('Quit', pygame_menu.events.EXIT)
menu.mainloop(surface)

surface.fill((23, 28, 38))

root = build_tree()
render_tree(root)

while Launch:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Launch = False

    for i in range(DEPTH):
        text = f"{player}"
        text_font = pygame.font.SysFont("Comic Sans MS", 20)
        text_render = text_font.render(text, False, (255, 255, 255))
        surface.blit(text_render, (10, (i+2.5)*75))
        if player == "Max":
            player = "Min"
        else:
            player = "Max"

    pygame.display.flip()

    if Algo == 1:
        bestValue = Search.SearchAlgorithm.MiniMax(
            surface, root, DEPTH, player=PLAYER)
    elif Algo == 2:
        bestValue = Search.SearchAlgorithm.NegaMax(
            surface, root, DEPTH, player=PLAYER)
    else:
        bestValue = Search.SearchAlgorithm.NegaMaxAlphaBeta(
            surface, root, DEPTH, PLAYER, root.alpha, root.beta)

    text = f"Pour le joueur {CURRENT_PLAYER} le meilleur score est : {bestValue}"
    text_font = pygame.font.SysFont("Comic Sans MS", 20)
    text_render = text_font.render(text, False, (255, 255, 255))
    surface.blit(text_render, (10, 10))
    pygame.display.flip()
    time.sleep(10)
    Game = False
    Launch = False
