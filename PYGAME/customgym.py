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
    self.game = realgamesim.Game(FPS=60)

    self.action_space = spaces.Discrete(9)#9 movement, 8 dodgeroll
   
    # The observation will be the coordinate of the agent
    # this can be described both by Discrete and Box space
    self.observation_space = spaces.Discrete(1)

  def reset(self):
    """
    Important: the observation must be a numpy array
    :return: (np.array) 
    """
    self.game.reset()
    return np.array([0])

  def step(self, action):
      info ={}
      dir=[0,0]
      #print("TYPE: ",action.item(),type(action.item()))
      print(action,type(action))
      dir = self.ACTIONS[action]
      observation,reward,done = self.game.step(dir)
      truncated=0
      return observation,reward,done,info
  
  def render(self,mode='human'):
        self.game.render()

  def close(self):
    pass





if __name__=='__main__':
    # Instantiate the env
   # Instantiate the env
    env = BulletHellEnv()
   
    obs = env.reset()
    n_steps = 10000
    for step in range(n_steps):
                # Box(4,) means that it is a Vector with 4 components
        print("Observation space:", env.observation_space)
        print("Shape:", env.observation_space.shape)
        # Discrete(2) means that there is two discrete actions
        print("Action space:", env.action_space)

        # The reset method is called at the beginning of an episode
        obs = env.reset()
        # Sample a random action
        action = env.action_space.sample()
        print("Sampled action:", action)
        obs, reward, done, info = env.step(action)
        # Note the obs is a numpy array
        # info is an empty dict for now but can contain any debugging info
        # reward is a scalar
        #print(obs.shape, reward, done, info)
