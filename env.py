import numpy as np
from rubik_cube import corner, edge, rubik_cube
import rewards

def reverse_action(a):
    if a < 6:
        return a + 12
    elif a < 12:
        return a
    else:
        return a - 12

class rubik_env:
    def __init__(self, upset_steps, batch_size=1):
        self.cube = rubik_cube(id=0, random=True, random_step=upset_steps)
        self.state = self.cube.vectorize()
        self.action_space = 18
        self.observation_space = 20
        self.reward = 0
        self.upset_transition = list()

        # rewards.dist_init()

    def step(self, action):
        '''

        :param action: the id of action from 0 to 17
        :return: new_state, reward, done
        '''
        r = rewards.reward(self.cube)
        self.cube.digit_remote(action)
        self.state = self.cube.vectorize()
        self.reward = rewards.reward(self.cube) - r

        done = False

        if self.cube.is_solved() or (len(self.cube.opt_log) - self.cube.random_step) > 50:
            done = True

        return self.state, self.reward, done

    def reset(self, upset_steps):
        # 考虑在reset的同时，记录每次转换过程
        # self.cube = rubik_cube(id=self.cube.id+1, random=True, random_step=upset_steps)
        self.cube = rubik_cube(id=self.cube.id+1)
        self.upset_transition = list()
        for i_action in range(upset_steps):
            s = self.cube.vectorize()
            a = np.random.randint(18)
            r = rewards.reward(self.cube)
            self.cube.digit_remote(a)
            s_ = self.cube.vectorize()
            r = rewards.reward(self.cube) - r
            self.upset_transition.append([s, a, r, s_])
            a_ = reverse_action(a)
            self.upset_transition.append([s_, a_, -r, s])

        self.state = self.cube.vectorize()
        self.reward = 0
        return self.state, self.upset_transition
