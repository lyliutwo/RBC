import numpy as np
from rubik_cube import corner, edge, rubik_cube
import rewards

class env:
    def __init__(self, upset_steps, batch_size=1):
        self.cube = rubik_cube(id=0, random=True, random_step=upset_steps)
        self.state = self.cube.vectorize()
        self.action_space = 18
        self.observation_space = 20
        self.reward = rewards.naive_reward(self.cube)


    def step(self, action):
        '''

        :param action: the id of action from 0 to 17
        :return: new_state, reward, done
        '''
        self.cube.digit_remote(action)
        self.state = self.cube.vectorize()
        self.reward = rewards.naive_reward(self.cube)

        done = False

        if self.reward >= 2560.0 or (len(self.cube.opt_log) - self.cube.random_step) > 100:
            done = True

        return self.state, self.reward, done

    def reset(self, upset_steps):
        self.cube = rubik_cube(id=self.cube.id+1, random=True, random_step=upset_steps)
        self.state = self.cube.vectorize()
        self.reward = rewards.naive_reward(self.cube)

