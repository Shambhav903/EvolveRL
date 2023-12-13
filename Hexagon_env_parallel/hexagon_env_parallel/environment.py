import functools
import random
from copy import copy
import numpy as np
from gymnasium.spaces import Discrete, MultiDiscrete
import pygame
from pettingzoo import ParallelEnv


from hexagon_env_parallel.helperDisplay import clearGrid, init_hexagons, initializeAgent, render, renderAgents
from hexagon_env_parallel.helperDisplay import predatorDirectionGenerator,preyDirectionGenerator,predator_vision,prey_vision,direction_generator

NO_OF_PREY = 5
NO_OF_PREDATOR = 5
GRID_SIZE = (79,39)
# prey energy gain while staying
ALPHA = 15   # natural growth
# predator energy gain while eating
DELTA = 50   # 
# predator energy loss while moving
GAMMA = 1
PREY_REWARD = 20
PREDATOR_REWARD = 20

class Hex_Env(ParallelEnv):

    metadata = {
        "name": "hex_env_parallel_v0",
    }

    def __init__(self, render_mode=None):

        
        
        self.possible_prey = ["prey_" + str(r) for r in range(NO_OF_PREY)]
        self.possible_predator = ["predator_" + str(r) for r in range(NO_OF_PREDATOR)]
        self.possible_agents = self.possible_prey.copy() + self.possible_predator.copy()

        self.prey_agents = self.possible_prey.copy()
        self.predator_agents = self.possible_predator.copy()
        # optional: a mapping between agent name and ID
        self.agent_name_mapping = dict(
            zip(self.possible_agents, list(range(len(self.possible_agents))))
        )

        self.new_predators = 0
        self.new_prey = 0

        self.dead_predators = 0
        self.dead_preys = 0
        self.timestep = 0
        

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
            self.clock.tick(15)


    def reset(self, seed=None, options=None):

        self.agents = self.possible_agents[:]
        self.rewards = {agent: 0 for agent in self.agents}
        self._cumulative_rewards = {agent: 0 for agent in self.agents}
        self.terminations = {agent: False for agent in self.agents}
        self.truncations = {agent: False for agent in self.agents}
        self.infos = {agent: {} for agent in self.agents}
        self.state = {agent: None for agent in self.agents}
        self.observations = dict([(agent,[0]*36)  for agent in self.prey_agents]+[(agent,[0]*15)  for agent in self.predator_agents])
        self.num_moves = 0
        self.prey_agents = self.possible_prey.copy()
        self.predator_agents = self.possible_predator.copy()

        return self.observations, self.infos
    
    def predatorBehaviourCheck(self):
        """ if predator overlaps then prey is dead 
            if predator consumes prey then the energy of predator increases by 40
            every tick the energy of predator decreases by 1
            * for action if action taken by prey is to not move, then energy increases by 20
            * if predator or prey energy > 100 then divides and energy also divides,new offspring is born on a neighbouring hex
            * 
            if overlap dead
            decreases predator energy by gamma on each tick (-1)
            consuming increases energy by Delta             (+50)
            if energy of predator in > 100 then multiply predator and divide energy
            prey ko energy badhaune if stay action completed ( yo arko action wala function ma helne)
            prey multiply garne if energy > 100 ( this too handled by action function)
        """
        
        for predator in self.predatorAgents:
            predator[3] -= GAMMA
            index_predator = self.predatorAgents.index(predator)
            agent_predator = self.predator_agents[index_predator]
            if predator[3] <= 0:
                self.predatorDeath(predator)
            else:
                for prey in self.preyAgents:
                    if (predator[0],predator[1]) == (prey[0],prey[1]):
                        self.preyDeath(prey)
                        predator[3] += DELTA   # increase energy of predator
                        self.rewards[agent_predator] = PREDATOR_REWARD
                        break
                if predator[3] >= 100:
                    self.predatorSpawn(predator)  #spawns a new predator beside current predator
                    
    
    def predatorSpawn(self,predator):
        self.new_predators+=1
        predator[3] = int(predator[3]/2)
        x,y = direction_generator(predator[0],predator[1],random.randint(1,6))
        self.predatorAgents.append([x,y,(-1,0),int(predator[3]/2),predator[4]])
        self.predator_agents.append("predator_"+str(999-self.new_predators))

    def predatorDeath(self,predator):
        """
        1. takes in predator data, 
        2. finds it's index_predator in predator data list
        3. using index, removes the predator from predator name list
        """
        self.dead_predators+=1
        index_predator = self.predatorAgents.index(predator)
        agent_predator = self.predator_agents[index_predator]
        self.predator_agents.pop(index_predator)
        self.predatorAgents.remove(predator)
        self.agents.remove(agent_predator)
        
    def preyDeath(self,prey):
        self.dead_preys += 1
        index_prey = self.preyAgents.index(prey)
        agent_prey = self.prey_agents[index_prey]
        self.preyAgents.remove(agent_prey)
        self.terminations[agent_prey] == True
    
    def preySpawn(self,prey):
        self.dead_preys += 1
        index_prey = self.preyAgents.index(prey)
        agent_prey = self.prey_agents[index_prey]

        self.preyAgents.remove(prey)
        self.terminations[agent_prey] == True
        pass

    def step(self, actions):
        # Check termination conditions
        terminations = dict([(agent, False) for agent in self.possible_prey] + [(agent,False) for agent in self.possible_predator])
        truncations = dict([(agent, False) for agent in self.possible_prey] + [(agent,False) for agent in self.possible_predator])
        rewards = dict([(agent, 0) for agent in self.possible_prey] + [(agent,0) for agent in self.possible_predator])
        
        # Check truncation conditions (overwrites termination conditions)
        truncations = {a: False for a in self.agents}
        
        # to take actions for all agents
        for i in actions.keys():
            if i[3] == 'd':    # implies that i is predator
                index = self.predator_agents.index(i)
                x,y,dir =predatorDirectionGenerator(self.predatorAgents[index][0],self.predatorAgents[index][1],self.predatorAgents[index][4],actions[i])
                self.predatorAgents[index][0] = x
                self.predatorAgents[index][1] = y           
                self.predatorAgents[index][4] = dir
            else:
                index = self.prey_agents.index(i)
                # if stayed at same place increase energy
                if actions[i] == 7 :
                    self.preyAgents[index][3] += 15
                    self.rewards[i] = PREY_REWARD
                else:
                    # elif moved from a place then move to that place
                    x,y = preyDirectionGenerator(self.preyAgents[index][0],self.preyAgents[index][1],actions[i])
                    self.preyAgents[index][0] = x
                    self.preyAgents[index][1] = y
                
        # check behaviour after actions have been taken
        # change energy level for predator 
        self.predatorBehaviourCheck()
        # change energy level for prey if completed the stay at a place

        self.timestep += 1
        
        # Get observations

        # Set up observations
        observations = {
            a: 0
            for a in self.agents
        }

        infos = {a: {} for a in self.agents}

        if all(terminations.values()) or all(truncations.values()):
            self.agents = []

        return observations, rewards, terminations, truncations, infos

    def render(self):
        if self.render_mode is None:
            print('no agent specified')
            return
        
        if len(self.prey_agents) > 0 and len(self.predator_agents) > 0:
            clearGrid(self.hexagons)
            renderAgents(self.preyAgents,self.predatorAgents,self.hexagons)
            render(self.world, self.hexagons)

        else:
            string = "Game over"
            print(string)
            self.close()

    def observe(self, agent):
        return np.array(self.observations[agent])

    def close(self):
        pygame.display.quit()

    @functools.lru_cache(maxsize=None)
    def observation_space(self, agent):
        if (agent[3] == 'd'):
            return Discrete(15)
        else:
            return Discrete(36)
        
    @functools.lru_cache(maxsize=None)
    def action_space(self, agent):
        if (agent[3] =='d'):
            return Discrete(9)
        else:
            return Discrete(7)
