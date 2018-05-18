import gym
import obstacle_env

from rl_agents.agents.dqn.dqn_keras import DqnKerasAgent
from rl_agents.agents.dqn.dqn_pytorch import DqnPytorchAgent
from rl_agents.agents.dqn.graphics import ValueFunctionViewer
from rl_agents.trainer.simulation import Simulation
from rl_agents.trainer.state_sampler import ObstacleStateSampler
from rl_agents.wrappers.monitor import MonitorV2


def make_env():
    env_name = 'obstacle-v0'
    env = gym.make(env_name)
    env = MonitorV2(env, 'out/' + env_name)
    sampler = ObstacleStateSampler()
    return env, sampler


def dqn_keras(env):
    config = {
        "layers": [100, 100],
        "memory_capacity": 50000,
        "batch_size": 100,
        "gamma": 0.9,
        "epsilon": [1.0, 0.01],
        "epsilon_tau": 50000,
        "target_update": 1
    }
    return DqnKerasAgent(env, config)


def dqn_pytorch(env):
    config = {
        "layers": [100, 100],
        "memory_capacity": 50000,
        "batch_size": 100,
        "gamma": 0.9,
        "epsilon": [1.0, 0.01],
        "epsilon_tau": 50000,
        "target_update": 1
    }
    return DqnPytorchAgent(env, config)


if __name__ == "__main__":
    env, sampler = make_env()
    agent = dqn_pytorch(env)
    agent_viewer = ValueFunctionViewer(agent, sampler)
    sim = Simulation(env, agent, num_episodes=5000, agent_viewer=agent_viewer)
    sim.train()

