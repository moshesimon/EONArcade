import gym
from gym import spaces
import numpy as np
from gym_game.envs.arcade_game import ArcadeGame

class CustomEnv(gym.Env):

    def __init__(self):
        self.game = ArcadeGame()
        self.action_space = spaces.Discrete(3)
        
