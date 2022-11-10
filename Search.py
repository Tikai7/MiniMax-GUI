import Tree
import pygame
from pygame import gfxdraw
import time

pygame.font.init()

SUCCESS_COLOR = (0, 170, 255)
EXPLORED_COLOR = (255, 119, 0)
SPEED = 0.2
RAYON = 25
MAX = 1


class SearchAlgorithm:

    @staticmethod
    def MarkNode(surface, noeud: Tree.Node):
        x, y = noeud.position
        gfxdraw.aacircle(surface, x, y, RAYON, EXPLORED_COLOR)
        time.sleep(SPEED)
        pygame.display.flip()

    @staticmethod
    def MarkLine(surface, child: Tree.Node, parent: Tree.Node, BEST=False):
        x1, y1 = child.position
        x2, y2 = parent.position

        if BEST:
            EXPLORED_COLOR = SUCCESS_COLOR
        else:
            EXPLORED_COLOR = (255, 119, 0)

        gfxdraw.line(
            surface, x1, y1, x2, y2, EXPLORED_COLOR)
        time.sleep(SPEED)
        pygame.display.flip()

    @staticmethod
    def DisplayValue(surface, noeud: Tree.Node, BEST=False):
        if BEST:
            EXPLORED_COLOR = SUCCESS_COLOR
        else:
            EXPLORED_COLOR = (255, 119, 0)
        x, y = noeud.position
        gfxdraw.aacircle(surface, x, y, RAYON, EXPLORED_COLOR)
        gfxdraw.filled_circle(surface, x, y, RAYON, EXPLORED_COLOR)
        text = f"{noeud.value}"
        text_font = pygame.font.SysFont("Comic Sans MS", 15)
        text_render = text_font.render(text, False, (255, 255, 255))
        surface.blit(text_render, (x-6, y-6))
        time.sleep(SPEED)
        pygame.display.flip()

    @staticmethod
    def MiniMax(surface, noeud: Tree.Node, depth, player):
        if depth == 1:
            SearchAlgorithm.DisplayValue(surface, noeud)
        elif depth > 1:
            SearchAlgorithm.MarkNode(surface, noeud)
            succ_childs = [noeud.left_child, noeud.right_child]

            if player == MAX:
                best_value = float('-inf')
                best_path = None

                for child in succ_childs:
                    SearchAlgorithm.MarkLine(surface, child, noeud, False)
                    SearchAlgorithm.MiniMax(
                        surface, child, depth-1, -player)
                    if child.value > best_value:
                        best_value = child.value
                        best_path = child
            else:
                best_value = float('inf')
                best_path = None

                for child in succ_childs:
                    SearchAlgorithm.MarkLine(surface, child, noeud, False)
                    SearchAlgorithm.MiniMax(
                        surface, child, depth-1, -player)
                    if child.value < best_value:
                        best_value = child.value
                        best_path = child

            noeud.value = best_value
            noeud.path_child = best_path
            SearchAlgorithm.MarkLine(surface, child, noeud, True)
            SearchAlgorithm.DisplayValue(surface, noeud, True)
