import numpy as np
import gym
from gym import spaces
import realgamesim
from stable_baselines3 import DQN
from stable_baselines3.common.env_checker import check_env


class BulletHellEnv(gym.Env):
  """
  Custom Environment that follows gym interface.
  This is a simple env where the agent must learn to go always left. 
  """
  # Because of google colab, we cannot implement the GUI ('human' render mode)
  metadata = {'render.modes': ['human']}
  
  # Define constants for clearer code
  ACTIONS ={ 
           0:[0,0], # DONT MOVE
           1:[0,-1], # MOVE UP
           2:[0,1], # MOVE DOWN
           3:[-1,0],# MOVE LEFT
           4:[1,0], # MOVE RIGHT
           
           5:[1,1],# MOVE RIGHT AND DOWN
           6:[1,-1],# MOVE RIGHT AND UP
           7:[-1,1],#MOVE LEFT AND DOWN
           8:[-1,-1]#MOVE LEFT AND UP
           
           
  }
  def __init__(self):
    super(BulletHellEnv, self).__init__()
    self.game = realgamesim.Game(FPS=60,AI_control=True)

    self.action_space = spaces.Discrete(9)#9 movement, 8 dodgeroll
   
    # The observation will be the coordinate of the agent
    # this can be described both by Discrete and Box space
    #self.observation_space = spaces.Discrete(1)
    
    s = {
    'position': spaces.Box(low=0, high=100, shape=(2,)),
    'bullet_positions': spaces.Sequence(spaces.Box(low=0,high=100,shape=(2,)))
    }
    self.observation_space = spaces.Dict(s)

  def reset(self):
    """
    Important: the observation must be a numpy array
    :return: (np.array) 
    """
    info={}
    self.game.reset()
    return {'position':np.array([0,0]), 'bullet_positions':np.array([0,0]) },info

  def step(self, action):
      info ={}
      dir=[0,0]
      #print("TYPE: ",action.item(),type(action.item()))
      #print(action,type(action))
      dir = self.ACTIONS[action]
      observation,reward,done = self.game.step(dir)
      truncated=False
      return observation,reward,done,truncated,info
  
  def render(self,mode='human'):
        self.game.render()

  def close(self):
    pass



env = BulletHellEnv()
# It will check your custom environment and output additional warnings if needed
check_env(env)

print("ENVIRONMENT IS VALID")

env = BulletHellEnv()
obs = env.reset()
#VERIFY THAT ENV WORKS
'''n_steps = 10
for _ in range(n_steps):
    # Random action
    action = env.action_space.sample()
    obs, reward, done, truncated,info = env.step(action)
    env.render()
    if done:
        obs = env.reset()'''
#TRAIN MODEL
model = DQN('MlpPolicy', env).learn(total_timesteps=1,progress_bar=True)
print("DONE LEARNING")

print("SHOWING POLICY")
for i in range(1000):
    action, _states = model.predict(np.array([0]))
    action=action.item()
    print(f'ACTION: {action},STATES: {_states}')
    obs, rewards, term,trunc, info = env.step(action)
    env.render()