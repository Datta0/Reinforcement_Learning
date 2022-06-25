import random
import numpy as np

class TicTacToe:
    def __init__(self):
        self.state = np.zeros(9)
        self.empty_spots = np.arange(9)
        self.qtable = {}
        self.done = False
        self.reward = 0
    
    def init(self):
        self.state.fill(0)
        self.empty_spots = np.arange(9)
        player_side = np.random.choice([1,-1])
        opponent_side = -1*player_side
        self.done = False
        return str(self.state),player_side,opponent_side
    
    def check_win(self):
        self.done = True
        for i in range(3):
            if np.absolute(self.state[3*i]+self.state[3*i+1]+self.state[3*i+2]) == 3:
                return True
            if np.absolute(self.state[i]+self.state[i+3]+self.state[i+6]) == 3:
                return True
        if np.absolute(self.state[0] + self.state[4] + self.state[8]) == 3:
            return True
        if np.absolute(self.state[2] + self.state[4] + self.state[6]) == 3:
            return True
        
        self.done = False
        return False
    
    def check_draw(self):
        if np.any(self.state == 0):
            return False
        self.done = True
        return True
    
    def action(self,pos,side):
        self.state[pos] = side
        if self.check_win():
            self.reward = 5
            return self.reward
        if self.check_draw():
            self.reward = 0.5
            return self.reward
        self.reward = 0.1
        return self.reward

    
    def random_agent_step(self,side):
        # self.render()
        # print(side, self.qtable, self.empty_spots)
        pos = np.random.choice(self.empty_spots)
        self.reward = self.action(pos,side)
        return pos
        
    def safe_agent_step(self,side):
        for pos in self.empty_spots:
            self.reward = self.action(pos,side)
            if self.reward == 5:
                return pos
            else:
                self.state[pos] = 0
        
        for pos in self.empty_spots:
            self.reward= self.action(pos,-1*side)
            if self.reward == 5:
                self.reward = self.action(pos,side)
                return pos
            else:
                self.state[pos] = 0
                
        pos = self.random_agent_step(side)
        return pos
    
    def player_to_char(self,pos):
        if self.state[pos] == 1:
            return 'x'
        if self.state[pos] == -1:
            return 'o'
        return ' '
                
    def display(self):
        for i in range(3):
            print(self.player_to_char(i*3),'||',self.player_to_char(i*3 + 1),'||',self.player_to_char(i*3 +2) )
            if i != 2:
                print('===='*3)
                
        print("")
    def update_qtable(self,):
        if str(self.state) not in self.qtable:
            self.qtable[str(self.state)] = np.zeros(9)
        return self.qtable
    def chose_action(self,):
        if str(self.state) in self.qtable:
            max_pos = np.argmax(self.qtable[str(self.state)][self.empty_spots])
            return self.empty_spots[max_pos]
        else:
            self.qtable[str(self.state)] = np.zeros(9)
            return self.empty_spots[0]
