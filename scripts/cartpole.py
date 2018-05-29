import gym
import numpy as np

from rl_agents.agents.linear.linear import LinearAgent
from rl_agents.agents.dqn.dqn_pytorch import DQNPytorchAgent
from rl_agents.agents.tree_search.mcts import MCTSAgent
from rl_agents.trainer.benchmark import Benchmark
from rl_agents.trainer.simulation import Simulation
from rl_agents.trainer.state_sampler import CartPoleStateSampler


def make_env():
    env_name = 'CartPole-v0'
    environment = gym.make(env_name)
    env_sampler = CartPoleStateSampler()
    return environment, env_sampler


def dqn_pytorch(environment):
    config = dict(
        model=dict(layers=[100, 100]),
        exploration=dict(tau=6000),
    )
    return DQNPytorchAgent(environment, config)


def linear(environment):
    config = {
        'K': np.array([[1, 20, 20, 30]])
    }
    return LinearAgent(environment, config)


def mcts(environment):
    config = dict(iterations=40,
                  temperature=200,
                  max_depth=10)
    return MCTSAgent(environment, config)


if __name__ == "__main__":
    gym.logger.set_level(gym.logger.INFO)
    env, sampler = make_env()
    agent = dqn_pytorch(env)
    # agent = mcts(env)
    sim = Simulation(env, agent, num_episodes=200)
    sim.test()

    # agents = [dqn_pytorch(env), mcts(env)]
    # benchmark = Benchmark(env, agents, num_episodes=5)
    # benchmark.run()
