import random
import numpy as np


class q_func:

    def __init__(self, game, num_episodes, alpha, epsilon, gamma):
        self.num_episodes = num_episodes
        self.alpha = alpha
        self.epsilon = epsilon
        self.gamma = gamma
        self.game = game
        self.Q = {}

    def choose_action_epsilon_greedy(self, state):

        if state not in self.Q:
            return random.randint(0, len(self.game.action_space)-1)
        else:
            greedy_action_index = np.argmax(self.Q[state])
            l = len(self.game.action_space)
            probabilities = [1.0 - self.epsilon *
                             (1-(1/l))] + [self.epsilon/l for i in range(l-1)]
            action_choices = [greedy_action_index] + \
                [x for x in range(l) if x != greedy_action_index]
            # print('probabilities {} action_choices {}'.format(probabilities,action_choices))
            action = np.random.choice(action_choices, p=probabilities)

            return action

    def checkQ(self, state):
        if state not in self.Q:
            self.Q[state] = np.zeros(len(self.game.action_space))

    def get_state(self, pacman, ghost, food_pellets):
        return '{}, {}, {}'.format(pacman, ghost, sorted(food_pellets))

    def train_agent(self,):

        episode_steps = 0
        total_steps = 0

        for episode in range(self.num_episodes):
            self.game.init()

            pacman = self.game.pacman
            ghost = self.game.ghost
            food = self.game.food_pellets
            state = self.get_state(pacman, ghost, food)

            action = self.choose_action_epsilon_greedy(state)
            self.checkQ(state)
            total_steps += episode_steps
            episode_steps = 0

            while True:
                episode_steps += 1
                self.game.step(action)
                reward = self.game.reward

                next_pacman = self.game.pacman
                next_ghost = self.game.ghost
                next_food_pellets = self.game.food_pellets
                next_state = self.get_state(
                    next_pacman, next_ghost, next_food_pellets)

                next_action = self.choose_action_epsilon_greedy(next_state)
                self.checkQ(next_state)
                # QFUNC
                # print('state {} action {} next {} na {}'.format(state,action,next_state,next_action))
                # print(self.Q)
                self.Q[state][action] = self.Q[state][action] + self.alpha * \
                    (reward + self.gamma *
                     np.max(self.Q[next_state]) - self.Q[state][action])

                state = next_state
                action = next_action

                if self.game.is_end():
                    break
            if episode != 0 and episode % 1000 == 0:
                print('Episode: {} Steps this episode: {} Average steps: {}'.format(
                    episode, episode_steps, round(total_steps/episode, 2)))
                if episode % 10000 == 0:
                    print(
                        '-----------------------------------------------------------------------')

    def test_agent(self,):

        self.game.init()
        self.game.display()

        while True:

            pacman = self.game.pacman
            ghost = self.game.ghost
            food = self.game.food_pellets
            state = self.get_state(pacman, ghost, food)

            action = self.choose_action_epsilon_greedy(state)
            self.game.step(action)
            self.game.display()

            if self.game.is_end():
                break
