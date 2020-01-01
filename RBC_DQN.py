from rubik_cube import rubik_cube
import numpy as np
import torch
import torch.nn as nn
from torch.autograd import Variable
import torch.nn.functional as F
import rewards
from env import rubik_env

# 超参数
N_STATES = 20   # 角块与棱块的环境信息
N_ACTIONS = 18     # 魔方的转动
EPSILON = 0.6   # 贪婪度 greedy
ALPHA = 0.01     # 学习率
GAMMA = 0.9    # 奖励递减值
TARGET_REPLACE_ITER = 100    # Q 现实网络的更新频率
MEMORY_CAPACITY = 2000      # 记忆库大小
BATCH_SIZE = 32

class Net(nn.Module):
    def __init__(self, ):
        super(Net, self).__init__()
        self.fc1 = nn.Linear(N_STATES, 10)
        self.fc1.weight.data.normal_(0, 0.1)    # initialization
        self.out = nn.Linear(10, N_ACTIONS)
        self.out.weight.data.normal_(0, 0.1)    # initialization

    def forward(self, x):
        x = self.fc1(x)
        x = F.relu(x)
        actions_value = self.out(x)
        return actions_value


class DQN(object):
    def __init__(self):
        self.eval_net, self.target_net = Net(), Net()

        self.learn_step_counter = 0  # 用于 target 更新计时
        self.memory_counter = 0  # 记忆库记数
        self.memory = np.zeros((MEMORY_CAPACITY, N_STATES * 2 + 2))  # 初始化记忆库
        self.optimizer = torch.optim.Adam(self.eval_net.parameters(), lr=ALPHA)  # torch 的优化器
        self.loss_func = nn.MSELoss()  # 误差公式

    def choose_action(self, x):
        x = Variable(torch.unsqueeze(torch.FloatTensor(x), 0))
        # 这里只输入一个 sample
        if np.random.uniform() < EPSILON:  # 选最优动作
            actions_value = self.eval_net.forward(x)
            # print(torch.max(actions_value, 1)[1].data.numpy())
            action = torch.max(actions_value, 1)[1].data.numpy()[0]  # return the argmax
        else:  # 选随机动作
            action = np.random.randint(0, N_ACTIONS)
        return action

    def store_transition(self, s, a, r, s_):
        transition = np.hstack((s, [a, r], s_))
        # 如果记忆库满了, 就覆盖老数据
        index = self.memory_counter % MEMORY_CAPACITY
        self.memory[index, :] = transition
        self.memory_counter = 1

    def learn(self):
        # target net 参数更新
        if self.learn_step_counter % TARGET_REPLACE_ITER == 0:
            self.target_net.load_state_dict(self.eval_net.state_dict())
        self.learn_step_counter = 1

        # 抽取记忆库中的批数据
        sample_index = np.random.choice(MEMORY_CAPACITY, BATCH_SIZE)
        b_memory = self.memory[sample_index, :]
        b_s = Variable(torch.FloatTensor(b_memory[:, :N_STATES]))
        b_a = Variable(torch.LongTensor(b_memory[:, N_STATES:N_STATES + 1].astype(int)))
        b_r = Variable(torch.FloatTensor(b_memory[:, N_STATES + 1:N_STATES + 2]))
        b_s_ = Variable(torch.FloatTensor(b_memory[:, -N_STATES:]))

        # 针对做过的动作b_a, 来选 q_eval 的值, (q_eval 原本有所有动作的值)
        q_eval = self.eval_net(b_s).gather(1, b_a)  # shape (batch, 1)
        q_next = self.target_net(b_s_).detach()  # q_next 不进行反向传递误差, 所以 detach
        q_target = b_r
        GAMMA * q_next.max(1)[0]  # shape (batch, 1)
        loss = self.loss_func(q_eval, q_target)

        # 计算, 更新 eval net
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()


dqn = DQN()  # 定义 DQN 系统
env = rubik_env(upset_steps=3)

for i_episode in range(400):
    s = env.reset(upset_steps=3)
    while True:

        a = dqn.choose_action(s)

        # 选动作, 得到环境反馈
        s_, r, done = env.step(a)


        # 存记忆
        dqn.store_transition(s, a, r, s_)

        if dqn.memory_counter > MEMORY_CAPACITY:
            dqn.learn()  # 记忆库满了就进行学习

        if done:  # 如果回合结束, 进入下回合
            break

        s = s_

