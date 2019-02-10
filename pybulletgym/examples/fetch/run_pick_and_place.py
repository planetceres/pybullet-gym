from time import sleep

import gym
import pybulletgym.envs
import numpy as np
import pybullet as p
import matplotlib.pyplot as plt

# Load the OpenAI gym env
env = gym.make('FetchPickKnifeAndCutEnv-v0')  # type: gym.Env

# Render the display and perform reset operations that set up the state
env.render(mode="human")
env.reset()

# Find the robot's base
baseId = -1
for i in range(p.getNumBodies()):
    print(p.getBodyInfo(i))
    if p.getBodyInfo(i)[0].decode() == "base_link":
        baseId = i
        print("found base")

# Start matplotlib to show the reward progression
rewards = []

for i in range(50):
    for _ in range(100):
        # print(env.render(mode="human"))
        # env.step(env.action_space.sample())

        # fetchPos, fetchOrn = p.getBasePositionAndOrientation(baseId)
        # distance = 2
        # yaw = 90
        # p.resetDebugVisualizerCamera(distance, yaw, -40, fetchPos)

        results = env.step(np.zeros(env.action_space.high.shape))
        # sleep(.5)
        sleep(0.02)
    print('Resetting')
    env.reset()
    sleep(1)
