import numpy as np
import gym
from gym import spaces
import realgamesim
from stable_baselines3 import DQN
from stable_baselines3.common.env_checker import check_env
from numpy import float32,array
from collections import OrderedDict
class BulletHellEnv(gym.Env):
  """
  Custom Environment that follows gym interface.
  This is a simple env where the agent must learn to go always left. 
  """
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
    
    
    self.observation_space = spaces.Dict({
    'position': spaces.Box(low=-np.inf, high=np.inf, shape=(2,)),
    'bullet_positions': spaces.Box(low=-np.inf,high=np.inf,shape=(20,2))})
    print("IS INSTANCE???",self.observation_space.spaces,'\n',isinstance(spaces.Sequence,spaces.Tuple),'\n',self.observation_space.sample(),'\n')
    #spaces.Tuple((spaces.Discrete(2), spaces.Box(-1, 1, shape=(2,))))

    '''
   '''
    
  def reset(self):
    """
    Important: the observation must be a numpy array
    :return: (np.array) 
    """
    info={}
    self.game.reset()

   # print(self.observation_space.sample(),'\n')
    
    return self.observation_space.sample(),info

  def step(self, action):
      info ={}
      dir=[0,0]
      #print("TYPE: ",action.item(),type(action.item()))
      #print(action,type(action))
      dir = self.ACTIONS[action]
      observation,reward,terminated = self.game.step(dir)
      truncated=False
      return observation,reward,terminated,truncated,info
  
  def render(self,mode='human'):
        self.game.render()

  def close(self):
    pass

if __name__=='__main__':

        env = BulletHellEnv()
        # It will check your custom environment and output additional warnings if needed
        check_env(env)

        print("ENVIRONMENT IS VALID")

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
        model = DQN('MultiInputPolicy', env).learn(total_timesteps=10000000,progress_bar=True)
        print("DONE LEARNING")

        model.save("mlphell")
        del model  # delete trained model to demonstrate loading

        # Load the trained agent
        # NOTE: if you have loading issue, you can pass `print_system_info=True`
        # to compare the system on which the model was trained vs the current one
        # model = DQN.load("dqn_lunar", env=env, print_system_info=True)
        model = DQN.load("mlphell", env=env)


        print("SHOWING POLICY")
        for i in range(1000):
            action, _states = model.predict(env.observation_space.sample())
            action=action.item()
            print(f'ACTION: {action},STATES: {_states}')
            obs, rewards, term,trunc, info = env.step(action)
            env.render()