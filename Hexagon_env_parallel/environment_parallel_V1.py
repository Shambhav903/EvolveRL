
import sys
sys.path.append('hexagon_env')

import functools
import random
from copy import copy
import numpy as np
from gymnasium.spaces import Discrete, MultiDiscrete

from pettingzoo import ParallelEnv

from helperDisplay import clearGrid, init_hexagons, initializeAgent, render, renderAgents
from helperDisplay import predatorDirectionGenerator,preyDirectionGenerator,predator_vision,prey_vision


class Hex_Env(ParallelEnv):
    """The metadata holds environment constants.

    The "name" metadata allows the environment to be pretty printed.
    """

    metadata = {
        "name": "hex_env_parallel_v0",
    }

    def __init__(self):

        pass
    def reset(self, seed=None, options=None):
 
        observations = {
            a: 0
            for a in self.agents
        }

        # Get dummy infos. Necessary for proper parallel_to_aec conversion
        infos = {a: {} for a in self.agents}

        return observations, infos

    def step(self, actions):
        # Check termination conditions
        terminations = dict([(agent, False) for agent in self.possible_prey] + [(agent,False) for agent in self.possible_predator])
        truncations = dict([(agent, False) for agent in self.possible_prey] + [(agent,False) for agent in self.possible_predator])
        rewards = dict([(agent, 0) for agent in self.possible_prey] + [(agent,0) for agent in self.possible_predator])
        
        # Check truncation conditions (overwrites termination conditions)
        truncations = {a: False for a in self.agents}
        self.timestep += 1

        # Get observations
        observations = {
            a: 0
            for a in self.agents
        }

        infos = {a: {} for a in self.agents}

        if any(terminations.values()) or all(truncations.values()):
            self.agents = []

        return observations, rewards, terminations, truncations, infos

    def render(self):
        """Renders the environment."""
        grid = np.full((7, 7), " ")
        grid[self.prisoner_y, self.prisoner_x] = "P"
        grid[self.guard_y, self.guard_x] = "G"
        grid[self.escape_y, self.escape_x] = "E"
        print(f"{grid} \n")

    # Observation space should be defined here.
    # lru_cache allows observation and action spaces to be memoized, reducing clock cycles required to get each agent's space.
    # If your spaces change over time, remove this line (disable caching).
    @functools.lru_cache(maxsize=None)
    def observation_space(self, agent):
        # gymnasium spaces are defined and documented here: https://gymnasium.farama.org/api/spaces/
        return MultiDiscrete([7 * 7] * 3)

    # Action space should be defined here.
    # If your spaces change over time, remove this line (disable caching).
    @functools.lru_cache(maxsize=None)
    def action_space(self, agent):
        return Discrete(4)