from time import sleep

import gym
import pybulletgym.envs

env = gym.make('FetchPickAndPlace-v0')
env.render(mode="human")
env.reset()
for _ in range(1000):
    env.render()
    env.step(env.action_space.sample())
    sleep(1)