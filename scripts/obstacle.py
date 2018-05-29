import multiprocessing

import gym

from rl_agents.agents.dqn.dqn_pytorch import DQNPytorchAgent
from rl_agents.agents.tree_search.mcts import MCTSAgent
from rl_agents.trainer.simulation import Simulation
from rl_agents.trainer.state_sampler import ObstacleStateSampler

import obstacle_env


def make_env():
    env_name = 'obstacle-v0'
    environment = gym.make(env_name)
    env_sampler = ObstacleStateSampler()
    return environment, env_sampler


def dqn_pytorch(environment):
    config = dict(model=dict(layers=[100, 100]),
                  gamma=0.9,
                  exploration=dict(tau=50000))
    return DQNPytorchAgent(environment, config)


def mcts(environment):
    from functools import partial
    return MCTSAgent(environment,
                     config=dict(iterations=100, temperature=150, max_depth=5),
                     prior_policy=partial(MCTSAgent.preference_policy, action_index=0, ratio=0.5))


def main():
    gym.logger.set_level(gym.logger.INFO)
    env, sampler = make_env()
    # agent = dqn_pytorch(env)
    agent = mcts(env)
    sim = Simulation(env, agent, num_episodes=80)
    sim.train()


if __name__ == "__main__":
    for i in range(4):
        p = multiprocessing.Process(target=main)
        p.start()
