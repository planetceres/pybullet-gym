from time import sleep

import gym
import pybulletgym.envs
import numpy as np
import pybullet as p

from utils import Plotter

env_list = [
    # 'FetchReach-v2',
    # 'FetchSlide-v2',
    'FetchPush-v2',
    # 'FetchPickAndPlace-v2',
    # 'FetchPickKnifeAndPlace-v2',
    # 'FetchMountainCar-v2'
]

for env_name in env_list:
    sleep(1)
    print(f'Testing {env_name}')
    # Load the OpenAI gym env
    env = gym.make(env_name, mode='human')  # type: gym.Env
    if hasattr(env.env, 'action_space_only_unlocked'):
        env.env.action_space_only_unlocked = True

    # Render the display and perform reset operations that set up the state
    # env.reset()
    # In order to loop this, we need it to run rgb_array not human. This is due to the global env variables
    # being initialized and then being confused on re-init
    # env.render(mode="rgb_array")
    env.render(mode="human")
    env.reset()

    plotter = Plotter()

    for i in range(2000):
        for _ in range(5):
            print(env.render(mode="human"))
            # results = env.step(env.action_space.sample())
            # fetchPos, fetchOrn = env.env._p.getBasePositionAndOrientation(baseId)
            # distance = 1.5
            # yaw = 90
            # env.env._p.resetDebugVisualizerCamera(distance, yaw, -45, fetchPos)

            # results = env.step(np.zeros(env.action_space.high.shape))
            action = env.action_space.sample()
            print(action)
            results = env.step(action)

            plotter.live_plotter(results[1], 'Reward')
            sleep(.1)

        print('Resetting')
        env.reset()
