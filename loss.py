import numpy as np

from rubic_cube import rubik_cube, corner, edge

corner_distance = np.ones([24, 24]) * 10
edge_distance = np.ones([24, 24]) * 10
opt_list = ["R", "L", "U", "D", "F", "B"]


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
        corner = corner(id=position, orientation=orientation)
        corner_list.append(corner)

    # 0
    for i in range(24):
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

                corner_distance[init, dest] = 1

    # 2
    while 10 in corner_distance:
        for i in range(24):
            for j in range(24):
                for k in range(24):
                    new_distance = corner_distance[i, j] + corner_distance[j, k]
                    if new_distance < corner_distance[i, k]:
                        corner_distance[i, k] = new_distance


def make_edge_distance():
    edge_list = list()
    for id in range(24):
        position = id % 12
        if id < 12:
            orientation = 1
        else:
            orientation = -1

        e = edge(id=position, orientation=orientation)

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
                edge_distance[init, dest] = 1

            c_1.remote(opt=opt, stride=stride)
            for edge in c_1.edges:
                init = edge.id + 12
                if edge.orientation == 1:
                    dest = edge.position
                else:
                    dest = edge.position + 12
                edge_distance[init, dest] = 1

    while 10 in edge_distance:
        for i in range(24):
            for j in range(24):
                for k in range(24):
                    new_distance = edge_distance[i, j] + edge_distance[j, k]
                    if new_distance < edge_distance[i, k]:
                        edge_distance[i, k] = new_distance


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


def compute_corner_loss(corner_i):
    origin = corner(id=corner_i.id)
    return compute_corner_distance(corner_i, origin)


def compute_edge_loss(edge_j):
    origin = edge(id=edge_j)
    return compute_edge_distance(edge_j, origin)


def naive_loss(x):
    loss = 0
    for c in x.corners:
        loss += compute_corner_loss(c)
    for e in x.edges:
        loss += compute_edge_loss(e)

    return loss