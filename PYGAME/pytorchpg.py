
import numpy as np
import gym
from gym import spaces
import realgamesim
from stable_baselines3 import DQN
from stable_baselines3.common.env_checker import check_env
from numpy import float32,array
from collections import OrderedDict
from customgym import BulletHellEnv



env = BulletHellEnv()
# It will check your custom environment and output additional warnings if needed
check_env(env)

print("ENVIRONMENT IS VALID")

#VERIFY THAT ENV WORKS
model = DQN.load("mlphell", env=env)


print("SHOWING POLICY")
obs,info =env.reset()
print(obs)
for i in range(10000):
    action, _state = model.predict(obs, deterministic=True)
    #print(f'ACTIONl: {type(action)},STATES: {_state}')
    obs, rewards, term,trunc, info = env.step(action.item())
    env.render()