import copy
import numpy as np

def train(game,learning_rate,gamma,opponent_choice, num_train_games = 10000, num_val_games = 100):
    epsilon = 1
    max_epsilon = 1
    min_epsilon = 0.01
    decay_rate = 0.05
    
    for episode in range(num_train_games):
        if episode%500 == 0:
            print('--------------Episode : {} --------------'.format(episode))
        state,player_side,opponent_side = game.init()
        opponent = np.random.choice(opponent_choice)
        turn = 1
        
        if episode == 0:
            game.update_qtable()
        while not game.done:
            if turn == opponent_side:
                if opponent == 0:
                    pos = game.random_agent_step(opponent_side)
                else:
                    pos = game.safe_agent_step(opponent_side)
            else:
                threshold = np.random.uniform(0,1)
                if threshold > epsilon:
                    pos = game.chose_action()
                    game.action(pos,player_side)
                else:
                    pos = game.random_agent_step(player_side)

            game.update_qtable()
            game.qtable[state][pos] = game.qtable[state][pos] + learning_rate*(game.reward-gamma*np.max(game.qtable[str(game.state)]) - game.qtable[state][pos])
            turn *= -1
            game.empty_spots = game.empty_spots[game.empty_spots != pos]
            state = str(game.state)
        
        if episode%500 == 0 or episode==num_train_games-1:
            test(copy.deepcopy(game),game.qtable,num_test_games = num_val_games,opponent_choice=opponent_choice, flag=0)
            
        epsilon = min_epsilon + (max_epsilon - min_epsilon)*np.exp(-decay_rate*episode)
    

def test(game,qtable,num_test_games=100,opponent_choice=[0],flag=0):
    wins_random = 0
    draws_random = 0
    loss_random = 0
    wins_safe = 0
    draws_safe = 0
    loss_safe = 0
    games_random = 0

    game.init()
    game.qtable = qtable

    for eps in range(num_test_games):
        state,player_side,opponent_side = game.init()
        finish = False
        opponent = np.random.choice(opponent_choice)
        turn = 1
        
        if opponent == 0:
            games_random += 1
        while not game.done:
            if turn == opponent_side:
                if opponent == 0:
                    pos = game.random_agent_step(opponent_side)
                else:
                    pos = game.safe_agent_step(opponent_side)
            else:
                pos = game.chose_action()
                reward = game.action(pos,player_side)
            if game.done and game.reward == 5 and turn == player_side:
                if opponent == 0:
                    wins_random += 1
                else:
                    wins_safe += 1
            if game.done and game.reward == 5 and turn == opponent_side:
                if opponent == 0:
                    loss_random += 1
                else:
                    loss_safe += 1
            if game.done and game.reward == 0.5:
                if opponent == 0:
                    draws_random += 1
                else:
                    draws_safe += 1

            turn *= -1
            state = str(game.state)
            game.empty_spots = game.empty_spots[game.empty_spots != pos]

    if flag == 0:
        print('Games : ',num_test_games ,'\tWins : ',wins_random+wins_safe,'\tDraws : ',draws_random+draws_safe,'\tLosses : ',loss_random+loss_safe)
    elif flag == 1:
        print('Stats :')
        print('\t\t\t Games Played \t Games Won \t Games drawn \t Games Lost')
        print('Against Random Agent\t',games_random,'\t\t',wins_random,'\t\t',draws_random,'\t\t',loss_random)
        print('Against Safe Agent\t',num_test_games-games_random,'\t\t',wins_safe,'\t\t',draws_safe,'\t\t',loss_safe)
        print('Total\t\t\t',num_test_games,'\t\t',wins_random+wins_safe,'\t\t',draws_random+draws_safe,'\t\t',loss_random+loss_safe)