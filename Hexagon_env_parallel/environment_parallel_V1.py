
import functools
import random
from copy import copy
import numpy as np
from gymnasium.spaces import Discrete, MultiDiscrete
import pygame
from pettingzoo import ParallelEnv


class Hex_Env(ParallelEnv):
    """The metadata holds environment constants.

    The "name" metadata allows the environment to be pretty printed.
    """

    metadata = {
        "name": "hex_env_parallel_v0",
    }

    def __init__(self, render_mode=None):
        """
        The init method takes in environment arguments and
         should define the following attributes:
        - possible_agents
        - render_mode

        Note: as of v1.18.1, the action_spaces and observation_spaces attributes are deprecated.
        Spaces should be defined in the action_space() and observation_space() methods.
        If these methods are not overridden, spaces will be inferred from self.observation_spaces/action_spaces, raising a warning.

        These attributes should not be changed after initialization.
        """
        self.possible_prey = ["prey_" + str(r) for r in range(NO_OF_PREY)]
        self.possible_predator = ["predator_" + str(r) for r in range(NO_OF_PREDATOR)]
        self.possible_agents = self.possible_prey.copy() + self.possible_predator.copy()

        self.prey_agents = self.possible_prey.copy()
        self.predator_agents = self.possible_predator.copy()

        # optional: a mapping between agent name and ID
        self.agent_name_mapping = dict(
            zip(self.possible_agents, list(range(len(self.possible_agents))))
        )

        # optional: we can define the observation and action spaces here as attributes to be used in their corresponding methods
        self._action_spaces = dict([(agent, Discrete(7)) for agent in self.possible_prey] + [(agent,Discrete(9)) for agent in self.possible_predator])
        self._observation_spaces = dict([(agent, Discrete(36)) for agent in self.possible_prey] + [(agent,Discrete(15)) for agent in self.possible_predator])
        self.predatorAgents,self.preyAgents = initializeAgent(NO_OF_PREDATOR,NO_OF_PREY)

        self.render_mode = render_mode
        if self.render_mode == "human":
            pygame.init()
            pygame.font.init()
            self.clock = pygame.time.Clock()
            self.world = pygame.display.set_mode((1200, 700))
            self.hexagons = init_hexagons(flat_top=True)
            self.clock.tick(70)
            # clearGrid(self.hexagons)
            # renderAgents(self.preyAgents,self.predatorAgents,self.hexagons)
            # render(self.world, self.hexagons)


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
        terminations = {a: False for a in self.agents}
        
        # Check truncation conditions (overwrites termination conditions)
        truncations = {a: False for a in self.agents}
        self.timestep += 1

        # Get observations
        observations = {
            a: 0
            for a in self.agents
        }

        # Get dummy infos (not used in this example)
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


    def observe(self, agent):
        """
        Observe should return the observation of the specified agent. This function
        should return a sane observation (though not necessarily the most up to date possible)
        at any time after reset() is called.
        """
        # observation of one agent is the previous state of the other
        return np.array(self.observations[agent])

    def close(self):
        """
        Close should release any graphical displays, subprocesses, network connections
        or any other environment data which should not be kept around after the
        user is no longer using the environment.
        """
        pygame.display.quit()



    # Observation space should be defined here.
    # lru_cache allows observation and action spaces to be memoized, reducing clock cycles required to get each agent's space.
    # If your spaces change over time, remove this line (disable caching).
    @functools.lru_cache(maxsize=None)
    def observation_space(self, agent):
        for agent in self.agents:
            if (agent[3] == 'd'):
                return Discrete(15)
            else:
                return Discrete(36)

    # Action space should be defined here.
    # If your spaces change over time, remove this line (disable caching).
    @functools.lru_cache(maxsize=None)
    def action_space(self, agent):
        for agent in self.agents:
            if (agent[3] =='d'):
                return Discrete(9)
            else:
                return Discrete(7)
