import numpy as np
import random
from collections import defaultdict

class Agent:
    def __init__(self, actions, state):
        self.episode_set = 1000
        self.episode = self.episode_set
        self.state = state
        self.actions = actions
        self.learning_rate = 0.01
        self.discount_factor = 0.9
        self.epsilon = 0.1
        self.q_table = defaultdict(lambda: [0.0]*len(actions))

        self.old_state = state
        self.new_state = 0

    def learn(self, state, action, reward, next_state):
        current_q = self.q_table[state][action]
        # using Bellman Optimality Equation to update q function
        new_q = reward + self.discount_factor * max(self.q_table[next_state])
        self.q_table[state][action] += self.learning_rate * (new_q - current_q)

    def arg_max(self,state_action):
        max_index_list = []
        max_value = state_action[0]
        for index, value in enumerate(state_action):
            if value > max_value:
                max_index_list.clear()
                max_value = value
                max_index_list.append(index)
            elif value == max_value:
                max_index_list.append(index)
        return random.choice(max_index_list)

    def get_action(self, state):
        if np.random.rand() < self.epsilon:
            # take random action
            action = np.random.choice(self.actions)
        else:
            # take action according to the q function table
            state_action = self.q_table[state]
            action = self.arg_max(state_action)
        return action
    def agent_play_start(self, state):
        action = self.get_action(state)
        self.state = state
        return action
    def agent_play_end(self,action,new_state,reward):
        self.learn(self.state, action, reward, str(new_state))
        self.state = new_state
        if reward != 0:
            self.episode -= 1
        if self.episode <= 0:
            savefile_dict(self.q_table)
            self.episode = self.episode_set
