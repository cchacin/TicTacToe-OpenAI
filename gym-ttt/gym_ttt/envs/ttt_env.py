import gym
from gym import error, spaces, utils
from gym.utils import seeding
import random, array

class TttEnv(gym.Env):
  metadata = {'render.modes': ['human']}

  def __init__(self):
    self.won = 0
    self.lost = 0
    self.observation_space = spaces.MultiDiscrete([3,3,3,3,3,3,3,3,3])
    self.action_space = spaces.Discrete(9)
    self.state = [0, 0, 0, 0, 0, 0, 0, 0, 0]
  def step(self, action):
    done = False
    reward = 0
    if self.state[action] == 0:
      self.state[action] = 1
      if self.hasPlayerWon(1):
        self.won += 1
        reward = 10
        done = True
      else:
        self.player2play()
        if self.hasPlayerWon(2):
          self.lost += 1
          reward = -10
          done = True
    else:
      reward = -1
    done = done or self.isItDone()
    return self.state, reward, done, {}
  def reset(self):
    self.render()
    self.state = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    return self.state
  def render(self, mode='human'):
    print("-----------------------------------------------------")
    print("| " + str(self.state[0]) + " " + str(self.state[1]) + " " + str(self.state[2]) + " |")
    print("| " + str(self.state[3]) + " " + str(self.state[4]) + " " + str(self.state[5]) + " |")
    print("| " + str(self.state[6]) + " " + str(self.state[7]) + " " + str(self.state[8]) + " |")
    print('won/lost: ' + str(self.won) + '/' + str(self.lost))
  def close(self):
      print('Hi')
  def availablePositions(self):
    return [i for i,x in enumerate(self.state) if x == 0]
  def isItDone(self):
    return len(self.availablePositions()) == 0
  def player2play(self):
      if self.isItDone() == False:
        self.state[random.choice(self.availablePositions())] = 2
  def hasPlayerWon(self, player):
    # check three rows
    if self.hasSameValues(0, 1, 2, player) or self.hasSameValues(3, 4, 5, player) or self.hasSameValues(6, 7, 8, player):
      return True
    # check three columns
    elif self.hasSameValues(0, 3, 6, player) or self.hasSameValues(1, 4, 7, player) or self.hasSameValues(2, 5, 8, player):
      return True
    # check both diagonals
    elif self.hasSameValues(0, 4, 8, player) or self.hasSameValues(2, 4, 6, player):
      return True
    else:
     return False
  def hasSameValues(self, pos1, pos2, pos3, value):
     if self.state[pos1] == value and self.state[pos2] == value and self.state[pos3] == value:
       return True
     else:
       return False
  def _randomPlayer2(self):
    #can player2 win?
    freePositions = [i for i,x in enumerate(self.state) if x == 0]

    if len(freePositions) == 0:
      return
    #can player win if I place it in a specific free position?
    for pos in freePositions:
      self.state[pos] = 2
      hasWon = self.hasPlayerWon(2)
      self.state[pos] = 0
      if hasWon:
        return pos

    # if can't win, just place randomly
    pos = freePositions[random.randint(0,len(freePositions)-1)]
    self.state[pos] = 2
