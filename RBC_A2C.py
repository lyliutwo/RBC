import numpy as np

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torch.autograd as autograd
from torch.autograd import Variable

from rubik_cube import rubik_cube
from env import rubik_env

GAMMA = .95
LR = 3e-3
N_GAMES = 2000
N_STEPS = 20

N_INPUT = 20
N_ACTIONS = 18


class ActorCritic(nn.Module):
    def __init__(self):
        super(ActorCritic, self).__init__()
        self.fc1 = nn.Linear(N_INPUT, 64)
        self.fc2 = nn.Linear(64, 128)
        self.fc3 = nn.Linear(128, 64)

        self.actor = nn.Linear(64, N_ACTIONS)
        self.critic = nn.Linear(64, 1)

    def forward(self, x):
        x = self.fc1(x)
        x = F.relu(x)
        x = self.fc2(x)
        x = F.relu(x)
        x = self.fc3(x)
        x = F.relu(x)
        return x

    def get_action_probs(self, x):
        x = self(x)
        action_probs = F.softmax(self.actor(x))
        return action_probs

    def get_state_value(self, x):
        x = self(x)
        state_value = self.critic(x)
        return state_value

    def evaluate_actions(self, x):
        x = self(x)
        action_probs = F.softmax(self.actor(x))
        state_values = self.critic(x)
        return action_probs, state_values


def calc_actual_state_values(rewards, dones):
    R = []
    rewards.reverse()

    if dones[-1] == True:
        next_return = 0

    else:
        s = torch.from_numpy(state[-1]).float().unsqueeze(0)
        next_return = model.get_state_value(Variable(s)).data[0][0]

    R.append(next_return)
    dones.reverse()
    for r in range(1, len(rewards)):
        if not dones[r]:
            this_return = rewards[r] + next_return * GAMMA
        else:
            this_return = 0
        R.append(this_return)

    R.reverse()
    state_values_true = Variable(torch.FloatTensor(R)).unsqueeze(1)

    return state_values_true


def reflect(states, actions, rewards, dones):

    state_values_true = calc_actual_state_values(rewards, dones)

    s = Variable(torch.FloatTensor(states))
    action_probs, state_values_est = model.evaluate_actions(s)
    action_log_probs = action_probs.log()
    a = Variable(torch.LongTensor(actions).view(-1, 1))
    chosen_action_log_probs = action_log_probs.gather(1, a)

    advantages = state_values_true - state_values_est

    entropy = (action_probs * action_log_probs).sum(1).mean()
    action_gain = (chosen_action_log_probs * advantages).mean()
    value_loss = advantages.pow(2).mean()
    total_loss = value_loss - action_gain - 0.0001 * entropy

    optimizer.zero_grad()
    total_loss.backward()
    nn.utils.clip_grad_norm(model.parameters(), 0.5)
    optimizer.step()

def test_model(model):
    score = 0
    done = False
    env = rubik_env(upset_steps)
    state = env.reset(upset_steps)
    global action_probs
    while not done:
        score += 1
        s = torch.from_numpy(state).float().unsqueeze(0)

        action_probs = model.get_action_probs(Variable(s))

        _, action_index = action_probs.max(1)
        action = action_index.data[0]

        next_state, reward, done, thing = env.step(action)
        state = next_state

    return score



upset_steps = 1

env = rubik_env(upset_steps)


state = env.reset(upset_steps)
solved_cubes = 0
model = ActorCritic()
optimizer = optim.Adam(model.parameters(), lr=LR)

while solved_cubes < N_GAMES:
    states, actions ,rewards, dones = [], [], [], []

    for i in range(N_STEPS):
        s = Variable(torch.from_numpy(state).float().unsqueeze(0))

        action_probs = model.get_action_probs(s)
        action = action_probs.multinomial().data[0][0]
        next_state, reward, done = env.step(action)

        states.append(state)
        actions.append(action)
        rewards.append(reward)
        dones.append(done)

        if done:
            state = env.reset(upset_steps)
            solved_cubes += 1
            break
        state = next_state
    reflect(states, actions, rewards, dones)

