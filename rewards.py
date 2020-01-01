import numpy as np

import rubik_cube
from rubik_cube import rubik_cube, corner, edge

corner_distance = np.ones([8, 24]) * 2
edge_distance = np.ones([12, 24]) * 2
opt_list = ["R", "L", "U", "D", "F", "B"]


def make_corner_distance():
    for i in range(8):
        corner_distance[i, i] = 0

    adj = [[], [], [], [], [], [], [], []]
    adj[0] = [[1, 0], [1, 1], [3, 0], [3, -1], [4, 1], [4, -1], \
            [2, 0], [5, 0], [7, 0]]
    adj[1] = [[2, 0], [2, -1], [0, 0], [0, 1], [5, 1], [5, -1], \
            [3, 0], [6, 0], [4, 0]]
    adj[2] = [[3, 0], [3, 1], [1, 0], [1, -1], [6, 1], [6, -1], \
            [0, 0], [7, 0], [5, 0]]
    adj[3] = [[0, 0], [0, -1], [2, 0], [2, 1], [7, 1], [7, -1], \
            [1, 0], [4, 0], [6, 0]]
    adj[4] = [[5, 0], [5, 1], [7, 0], [7, -1], [0, 1], [0, -1], \
            [6, 0], [1, 0], [3, 0]]
    adj[5] = [[6, 0], [6, -1], [4, 0], [4, 1], [1, 1], [1, -1], \
            [7, 0], [2, 0], [0, 0]]
    adj[6] = [[7, 0], [7, 1], [5, 0], [5, -1], [2, 1], [2, -1], \
            [4, 0], [3, 0], [1, 0]]
    adj[7] = [[4, 0], [4, -1], [6, 0], [6, 1], [3, 1], [3, -1], \
            [5, 0], [0, 0], [2, 0]]

    for i in range(8):
        for p, o in adj[i]:
            j = (p + o * 8) % 24
            corner_distance[i, j] = 1


def make_edge_distance():
    for i in range(12):
        edge_distance[i, i] = 0

    adj = [[], [], [], [], [], [], [], [], [], [], [], []]
    adj[0] = [[1, 0], [2, 0], [3, 0], [8, 0], [4, 0], [9, 0]]
    adj[1] = [[2, 0], [3, 0], [0, 0], [9, 1], [5, 0], [10, 1]]
    adj[2] = [[3, 0], [0, 0], [1, 0], [10, 0], [6, 0], [11, 0]]
    adj[3] = [[0, 0], [1, 0], [2, 0], [11, 1], [7, 0], [8, 1]]
    adj[4] = [[5, 0], [6, 0], [7, 0], [8, 0], [0, 0], [9, 0]]
    adj[5] = [[6, 0], [7, 0], [4, 0], [9, 1], [1, 0], [10, 1]]
    adj[6] = [[7, 0], [4, 0], [5, 0], [10, 0], [2, 0], [11, 0]]
    adj[7] = [[4, 0], [5, 0], [6, 0], [11, 1], [3, 0], [8, 1]]
    adj[8] = [[3, 1], [0, 0], [7, 1], [4, 0], [11, 0], [9, 0]]
    adj[9] = [[0, 1], [1, 0], [4, 1], [5, 0], [8, 0], [10, 0]]
    adj[10] = [[1, 1], [2, 0], [5, 1], [6, 0], [9, 0], [11, 0]]
    adj[11] = [[2, 1], [3, 0], [6, 1], [7, 0], [10, 0], [8, 0]]

    for i in range(12):
        for p, o in adj[i]:
            j = p + o * 12
            edge_distance[i, j] = 1

    dis = [[], [], [], [], [], [], [], [], [], [], [], []]
    dis[0] = [[0, 1], [2, 1], [4, 1], [6, 1]]
    dis[1] = [[1, 1], [3, 1], [5, 1], [7, 1]]
    dis[2] = [[0, 1], [2, 1], [4, 1], [6, 1]]
    dis[3] = [[1, 1], [3, 1], [5, 1], [7, 1]]
    dis[4] = [[0, 1], [2, 1], [4, 1], [6, 1]]
    dis[5] = [[1, 1], [3, 1], [5, 1], [7, 1]]
    dis[6] = [[0, 1], [2, 1], [4, 1], [6, 1]]
    dis[7] = [[1, 1], [3, 1], [5, 1], [7, 1]]
    dis[8] = [[8, 1], [9, 1], [10, 1], [11, 1]]
    dis[9] = [[8, 1], [9, 1], [10, 1], [11, 1]]
    dis[10] = [[8, 1], [9, 1], [10, 1], [11, 1]]
    dis[11] = [[8, 1], [9, 1], [10, 1], [11, 1]]

    for i in range(12):
        for p, o in dis[i]:
            j = p + o * 12
            edge_distance[i, j] = 3



'''
def make_corner_distance():
    corner_list = list()
    for id in range(24):
        position = id % 8
        if id < 8:
            orientation = 0
        elif id < 16:
            orientation = 1
        else:
            orientation = -1

        Corner = rubic_cube.corner(id=position, orientation=orientation)
        corner_list.append(Corner)

    # 0
    for i in range(8):
        corner_distance[i, i] = 0

    # 1
    corner_list_0 = corner_list[:8]
    corner_list_1 = corner_list[8:16]
    corner_list_2 = corner_list[16:]

    c_0 = rubik_cube(0)
    c_1 = rubik_cube(1)
    c_2 = rubik_cube(2)

    for opt in opt_list:
        for stride in [1, 2, 3]:
            c_0.copy_corner(corner_list_0)
            c_1.copy_corner(corner_list_1)
            c_2.copy_corner(corner_list_2)

            c_0.remote(opt=opt, stride=stride)
            for corner in c_0.corners:
                init = corner.id
                if corner.orientation == 0:
                    dest = corner.position
                elif corner.orientation == 1:
                    dest = corner.position + 8
                elif corner.orientation == -1:
                    dest = corner.position + 16
                if corner_distance[init, dest] > 1:
                    corner_distance[init, dest] = 1

            c_1.remote(opt=opt, stride=stride)
            for corner in c_1.corners:
                init = corner.id + 8
                if corner.orientation == 0:
                    dest = corner.position
                elif corner.orientation == 1:
                    dest = corner.position + 8
                elif corner.orientation == -1:
                    dest = corner.position + 16
                if corner_distance[init, dest] > 1:
                    corner_distance[init, dest] = 1

            c_2.remote(opt=opt, stride=stride)
            for corner in c_2.corners:
                init = corner.id + 16
                if corner.orientation == 0:
                    dest = corner.position
                elif corner.orientation == 1:
                    dest = corner.position + 8
                elif corner.orientation == -1:
                    dest = corner.position + 16
                if corner_distance[init, dest] > 1:
                    corner_distance[init, dest] = 1

    # 2
    while 10 in corner_distance:
        for i in range(24):
            for j in range(24):
                for k in range(24):
                    new_distance = corner_distance[i, j] + corner_distance[j, k]
                    if new_distance < corner_distance[i, k]:
                        corner_distance[i, k] = new_distance

'''

'''
def make_edge_distance():
    edge_list = list()
    for id in range(24):
        position = id % 12
        if id < 12:
            orientation = 1
        else:
            orientation = -1

        e = rubik_cube.edge(id=position, orientation=orientation)

        edge_list.append(e)

    # 0
    for i in range(24):
        edge_distance[i, i] = 0

    # 1
    edge_list_0 = edge_list[:12]
    edge_list_1 = edge_list[12:]

    c_0 = rubik_cube(0)
    c_1 = rubik_cube(1)

    for opt in opt_list:
        for stride in [1, 2, 3]:
            c_0.copy_edge(edge_list_0)
            c_1.copy_edge(edge_list_1)

            c_0.remote(opt=opt, stride=stride)
            for edge in c_0.edges:
                init = edge.id
                if edge.orientation == 1:
                    dest = edge.position
                else:
                    dest = edge.position + 12
                if edge_distance[init, dest] > 1:
                    edge_distance[init, dest] = 1

            c_1.remote(opt=opt, stride=stride)
            for edge in c_1.edges:
                init = edge.id + 12
                if edge.orientation == 1:
                    dest = edge.position
                else:
                    dest = edge.position + 12
                if edge_distance[init, dest] > 1:
                    edge_distance[init, dest] = 1

    while 10 in edge_distance:
        for i in range(24):
            for j in range(24):
                for k in range(24):
                    new_distance = edge_distance[i, j] + edge_distance[j, k]
                    if new_distance < edge_distance[i, k]:
                        edge_distance[i, k] = new_distance
'''


def compute_corner_distance(corner_i, corner_j):
    if corner_i.orientation == 0:
        i = corner_i.position
    elif corner_i.orientation == 1:
        i = corner_i.position + 8
    elif corner_i.orientation == -1:
        i = corner_i.position + 16

    if corner_j.orientation == 0:
        j = corner_j.position
    elif corner_j.orientation == 1:
        j = corner_j.position + 8
    elif corner_j.orientation == -1:
        j = corner_j.position + 16

    return corner_distance[i, j]


def compute_edge_distance(edge_i, edge_j):
    if edge_i.orientation == 1:
        i = edge_i.position
    elif edge_i.orientation == -1:
        i = edge_i.position + 12

    if edge_j.orientation == 1:
        j = edge_j.position
    elif edge_j.orientation == -1:
        j = edge_j.position + 12

    return edge_distance[i, j]


def compute_corner_reward(corner_i):
    '''
    通过cube计算块的reward，每个块随着距离增加奖励减半
    :param corner_i:
    :return:
    '''
    origin = corner(id=corner_i.id)
    d = compute_corner_distance(origin, corner_i)
    reward = 128.0 * (0.5 ** d)

    # if d > 0:
    #     print("corner{0} {1}".format(corner_i.id, d))
    return reward


def compute_edge_reward(edge_j):
    origin = edge(id=edge_j.id)
    d = compute_edge_distance(origin, edge_j)
    reward = 128.0 * (0.5 ** d)
    # if d > 0:
    #     print("edge{0} {1}".format(edge_j.id, d))
    return reward


def dist_init():
    edge_distance = make_edge_distance()
    corner_distance = make_corner_distance()


def naive_reward(x):
    reward = 0
    # dist_init() #  每次都重新计算太浪费时间了
    for c in x.corners:
        reward += compute_corner_reward(c)
    for e in x.edges:
        reward += compute_edge_reward(e)

    return reward
