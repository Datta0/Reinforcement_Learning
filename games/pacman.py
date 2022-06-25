import random
import numpy as np


class Pacman:

    def __init__(self, grid_size, num_food_pellets):
        self.grid_size = grid_size
        self.num_food_pellets = num_food_pellets
        # Directions, Up Down Right Left and stay
        self.action_space = [(1, 0), (-1, 0), (0, 1), (0, -1), (0, 0)]
        self.init()

    def init(self,):
        # 1 to self.grid_size-1 cuz the borders are walls
        locs = [(i, j) for i in range(1, self.grid_size-1)
                for j in range(1, self.grid_size-1)]
        random.shuffle(locs)

        self.pacman = locs.pop()  # set pacman's location
        self.food_pellets = set()

        self.set_food()

        self.create_ghost()
        self.reward = 0
        self.score = 0

    def set_food(self,):
        (r, c) = self.pacman  # row and col of pacman's location

        valid_locs = [(i, j) for i in range(1, self.grid_size-1) for j in range(
            1, self.grid_size-1) if (i, j) != (r, c)]  # Initialise food pellet positions randomly
        random.shuffle(valid_locs)
        for i in range(self.num_food_pellets):
            self.food_pellets.add(valid_locs.pop())

        self.food_pellets_left = self.num_food_pellets

    def create_ghost(self,):
        (r, c) = self.pacman
        # Initialize the ghost in same column as pacman
        if r != 1:
            self.ghost = (1, c)
        else:
            self.ghost = (self.grid_size-2, c)
        self.ghost_action = random.choice(self.action_space)

    def display(self,):
        print("Current score: {}".format(self.score))

        for r in range(self.grid_size):
            for c in range(self.grid_size):
                if (r, c) == self.pacman:
                    print('P', end='')
                elif (r, c) == self.ghost:
                    print('G', end='')
                elif (r, c) in self.food_pellets:
                    print('o', end='')
                elif self.is_boundary((r, c)):
                    print('*', end='')
                else:
                    print(' ', end='')
            print('')

    def is_end(self,):
        if self.reward == -100:
            return True
        return False

    def is_boundary(self, pos):
        if pos[0] == 0 or pos[0] == self.grid_size-1 or pos[1] == 0 or pos[1] == self.grid_size-1:
            return True

    def get_state(self,):
        return '{} {} {} {}'.format(self.pacman, self.ghost, self.food_pellets, sorted(self.food_pellets_left))

    def step(self, action):
        # save current positions of pacman and ghost
        pacman, ghost = self.pacman, self.ghost
        # print('pacman {} action {} ghost {}'.format(pacman,action,ghost))
        # Move pacman acc to action
        (px, py) = self.action_space[action]
        (r, c) = self.pacman
        self.pacman = (r+px, c+py)

        # Move ghost acc to ghost_action ie random
        (gx, gy) = self.ghost_action
        (gr, gc) = self.ghost
        self.ghost = (gr+gx, gc+gy)

        if self.is_boundary(self.ghost):
            self.create_ghost()

        # If both at same place or both crossed through the other this move or pacman hits boundary, end game
        if self.pacman == self.ghost or (pacman, self.ghost) == (ghost, self.pacman) or self.is_boundary(self.pacman):
            self.reward = -100
        elif self.pacman in self.food_pellets:
            self.food_pellets_left -= 1
            self.food_pellets.remove(self.pacman)
            self.reward = 10
            if self.food_pellets_left == 0:
                self.set_food()
        else:
            self.reward = 0
        self.ghost_action = random.choice(self.action_space)
        self.score += self.reward
