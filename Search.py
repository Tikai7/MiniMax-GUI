import Tree
import pygame
from pygame import gfxdraw
import time

pygame.font.init()

OLD_VALUE = float('-inf')
GRAY_COLOR = (125, 142, 161)
SUCCESS_COLOR = (0, 170, 255)
SUCCESS_COLOR_B = (255, 71, 84)
EXPLORED_COLOR = (255, 119, 0)
SPEED = 0.1
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
    def MarkLine(surface, child: Tree.Node, parent: Tree.Node, BEST=False, FEUILLE=False):
        x1, y1 = child.position
        x2, y2 = parent.position

        if BEST:
            EXPLORED_COLOR = SUCCESS_COLOR
        else:
            EXPLORED_COLOR = (255, 119, 0)

        gfxdraw.line(
            surface, x1, y1, x2, y2, EXPLORED_COLOR)
        gfxdraw.filled_circle(surface, x2, y2, RAYON, (255, 255, 255))
        if not FEUILLE:
            gfxdraw.filled_circle(surface, x1, y1, RAYON, (255, 255, 255))
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
        text_font = pygame.font.SysFont("Comic Sans MS", 12)
        text_render = text_font.render(text, False, (255, 255, 255))
        surface.blit(text_render, (x-6, y-6))
        time.sleep(SPEED)
        pygame.display.flip()

    @staticmethod
    def DisplayAlphaBeta(surface, noeud: Tree.Node):
        CURRENT_COLOR = SUCCESS_COLOR if noeud.alpha != float(
            '-inf') else GRAY_COLOR
        CURRENT_COLOR_B = SUCCESS_COLOR_B if noeud.beta != float(
            'inf') else GRAY_COLOR

        x, y = noeud.position
        text = f"A : {OLD_VALUE}"
        text_font = pygame.font.SysFont("Comic Sans MS", 12)
        text_render = text_font.render(text, False, (23, 28, 38))
        surface.blit(text_render, (x-20, y-RAYON-40))

        text = f"A : {noeud.alpha}"
        text_font = pygame.font.SysFont("Comic Sans MS", 12)
        text_render = text_font.render(text, False, CURRENT_COLOR)
        surface.blit(text_render, (x-20, y-RAYON-40))

        text = f"B : {noeud.beta}"
        text_font = pygame.font.SysFont("Comic Sans MS", 12)
        text_render = text_font.render(text, False, CURRENT_COLOR_B)
        surface.blit(text_render, (x-20, y-RAYON-25))

        time.sleep(SPEED)
        pygame.display.flip()

    @ staticmethod
    def MiniMax(surface, noeud: Tree.Node, depth, player):
        if depth == 1:
            SearchAlgorithm.DisplayValue(surface, noeud)
        else:
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
            SearchAlgorithm.MarkLine(
                surface, best_path, noeud, True, True)
            SearchAlgorithm.DisplayValue(surface, noeud, False)
            SearchAlgorithm.DisplayValue(surface, best_path, True)

            return best_value

    @ staticmethod
    def NegaMax(surface, noeud: Tree.Node, depth, player):
        if depth == 1:
            if player != MAX:
                noeud.value = -noeud.value

            SearchAlgorithm.DisplayValue(surface, noeud)
        else:
            SearchAlgorithm.MarkNode(surface, noeud)
            best_value = float('-inf')
            best_path = None
            succ_childs = [noeud.left_child, noeud.right_child]
            for child in succ_childs:
                SearchAlgorithm.MarkLine(surface, child, noeud, False)
                SearchAlgorithm.NegaMax(surface, child, depth-1, -player)
                if -child.value > best_value:
                    best_value = -child.value
                    best_path = child
            noeud.value = best_value
            noeud.path_child = best_path
            SearchAlgorithm.MarkLine(
                surface, best_path, noeud, True, True)
            SearchAlgorithm.DisplayValue(surface, noeud, False)
            SearchAlgorithm.DisplayValue(surface, best_path, True)

            return best_value

    @ staticmethod
    def NegaMaxAlphaBeta(surface, noeud: Tree.Node, depth, player, alpha, beta):
        global OLD_VALUE
        first_alpha = alpha
        noeud.alpha = alpha
        noeud.beta = beta

        if depth == 1:
            if player != MAX:
                noeud.value = -noeud.value

            SearchAlgorithm.DisplayValue(surface, noeud)
            SearchAlgorithm.DisplayAlphaBeta(surface, noeud)

        else:
            SearchAlgorithm.MarkNode(surface, noeud)
            best_value = float('-inf')
            best_path = None
            SearchAlgorithm.DisplayAlphaBeta(
                surface, noeud)
            succ_childs = [noeud.left_child, noeud.right_child]
            for child in succ_childs:
                SearchAlgorithm.MarkLine(surface, child, noeud, False)
                SearchAlgorithm.NegaMaxAlphaBeta(
                    surface, child, depth-1, -player, -beta, -alpha)
                if -child.value > best_value:
                    best_value = -child.value
                    best_path = child

                if best_value > alpha:
                    OLD_VALUE = noeud.alpha
                    alpha = best_value
                    noeud.alpha = alpha
                    SearchAlgorithm.DisplayAlphaBeta(
                        surface, child)

                if beta <= alpha:
                    break

            noeud.value = best_value
            noeud.path_child = best_path
            SearchAlgorithm.MarkLine(
                surface, best_path, noeud, True, True)
            SearchAlgorithm.DisplayValue(surface, noeud, False)
            SearchAlgorithm.DisplayValue(surface, best_path, True)
            OLD_VALUE = first_alpha
            SearchAlgorithm.DisplayAlphaBeta(surface, noeud)
            return best_value
