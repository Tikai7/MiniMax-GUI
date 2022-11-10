from collections import deque

MAX_DEPTH = 4
WIDTH = 1600
HEIGHT = 900


class Node:
    def __init__(self, parent, depth, name):
        self.parent = parent
        self.depth = depth
        self.value = None
        self.left_child = None
        self.right_child = None
        self.alpha = float('-inf')
        self.beta = float('inf')

        if parent != None:
            x = self.parent.position[0]
            y = self.parent.position[1]+50+depth*5

            base_distance = 370
            diviseur = 1
            if depth > 1:
                gf_x = self.parent.parent.position[0]
                base_distance = abs(x-gf_x)*1.5
                diviseur = 3

            if name == "right":
                x += base_distance//diviseur
            else:
                x -= base_distance//diviseur

            self.position = (int(x), int(y))
        else:
            self.position = (WIDTH//2, HEIGHT//4)

        if depth < MAX_DEPTH:
            self.left_child = Node(self, depth+1, "left")
            self.right_child = Node(self, depth+1, "right")

        self.path_child = None

    def add_value(self, values: deque):

        if len(values) > 0:
            if self.left_child != None:
                self.left_child.add_value(values)
            elif self.value == None:
                self.value = values.popleft()

            if self.right_child != None:
                self.right_child.add_value(values)
            elif self.value == None:
                self.value = values.popleft()
