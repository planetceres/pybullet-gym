# Created by Giuseppe Paolo 
# Date: 20/04/2020

import gym
import pybullet
import pybulletgym
import matplotlib.pyplot as plt

env = gym.make('AntMuJoCoMazeEnv-v0')

env.render()
env.reset()

for i in range(10000):
  env.step(env.action_space.sample())

# image = env.render(mode='rgb_array', top_bottom=True)
# plt.figure()
# plt.imshow(image)
# plt.show()
