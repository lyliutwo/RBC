import numpy as np
import torch
from RBC_DQN import DQN
from env import rubik_env
from rubik_cube import corner, edge, rubik_cube
import rewards

# 超参数
N_STATES = 20   # 角块与棱块的环境信息
N_ACTIONS = 18     # 魔方的转动
EPSILON = 0.6   # 贪婪度 greedy
ALPHA = 0.01     # 学习率
GAMMA = 0.9    # 奖励递减值
TARGET_REPLACE_ITER = 100    # Q 现实网络的更新频率
MEMORY_CAPACITY = 2000      # 记忆库大小

def train():
    upset_steps = 1
    dqn = DQN()
    env = rubik_env(upset_steps)

    step = 10000
    for i_step in range(step):
        s = env.reset(upset_steps)
        while True:
            a = dqn.choose_action(s)
            s_, r, done = env.step(a)
            dqn.store_transition(s, a, r, s_)

            if dqn.memory_counter > MEMORY_CAPACITY:
                dqn.learn()

            if done:
                break

            s = s_

    return dqn