import gym
import sys
import pickle
import tensorflow as tf
import numpy as np
from stable_baselines.common.policies import MlpPolicy
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines import PPO2
from gym_ttt.envs import TttEnv

def main(_args):
  env = DummyVecEnv([lambda: TttEnv()])

  # model = PPO2(MlpPolicy, env)
  model = PPO2.load("ppo2_ttt", env=env)
  model.learn(total_timesteps=100000)
  model.save("ppo2_ttt")

if __name__== "__main__":
 main(sys.argv)
