'''
定义一个魔方的数学模型
魔方的状态
魔方的操作
'''
# 颜色编号：绿：0 红：1 白：2 橙：3 黄：4 蓝：5
# 魔方方向设定： U：绿 F：红

import numpy as np


class edge:

    def __init__(self, id):
        '''
            一个棱块有：
                两个色块
                方向
                位置
        '''
        self.id = id
        self.color = self.paint()
        self.position = self.id
        self.orientation = 1

    def paint(self):
        color_list = [[0, 2], [0, 1], [0, 4], [0, 3], [5, 2], [5, 1], [5, 4], [5, 3],
                      [1, 2], [1, 4], [3, 4], [3, 2]]
        return color_list[self.id]

    def change_orien(self):
        self.orientation = -self.orientation
        return self.orientation


class corner:
    def __init__(self, id):
        self.id = id
        self.color = self.paint()
        self.position = self.id
        self.orientation = 0

    def paint(self):
        color_list = [[0, 1, 2], [0, 3, 2], [0, 3, 4], [0, 1, 4],
                       [5, 1, 2], [5, 3, 2], [5, 3, 4], [5, 1, 4]]
        return color_list[self.id]

    def change_orien(self, opt=0):
        if opt == 0:
            return self.orientation
        if self.id in [0, 2, 5, 7]:
            if opt == 1:
                if self.orientation == 0:
                    self.orientation = 1
                elif self.orientation == 1:
                    self.orientation = -1
                else:
                    self.orientation = 0
            elif opt == 2:  # 从y轴到z轴
                if self.orientation == 0:
                    self.orientation = -1
                elif self.orientation == 1:
                    self.orientation = 0
                else:
                    self.orientation = 1
        else:
            if opt == 2:
                if self.orientation == 0:
                    self.orientation = 1
                elif self.orientation == 1:
                    self.orientation = -1
                else:
                    self.orientation = 0
            elif opt == 1:
                if self.orientation == 0:
                    self.orientation = -1
                elif self.orientation == 1:
                    self.orientation = 0
                else:
                    self.orientation = 1

        return self.orientation


class face:
    def __init__(self, id):
        self.id = id
        self.corners_id = list()
        self.edges_id = list()


class rubik_cube:

    def __init__(self, id):

        self.id = id  # 魔方编号，姑且弄一个虽然不知道有什么用
        self.corners = list()
        self.edges = list()
        for i in range(8):
            corner_cube = corner(i)
            self.corners.append(corner_cube)

        for j in range(12):
            edge_cube = edge(j)
            self.edges.append(edge_cube)

        self.corner_condition = np.array([0, 1, 2, 3, 4, 5, 6, 7], dtype=int)
        self.edge_condition = np.array([0, 1, 2, 3, 4, 5,
                               6, 7, 8, 9, 10, 11], dtype=int)


    def opt_U_1(self):

        face_corner = [0, 1, 2, 3]
        face_edge = [0, 1, 2, 3]

        corner_id = self.corner_condition[face_corner]
        edge_id = self.edge_condition[face_edge]

        # update the corner and edge condition
        self.corner_condition[face_corner] = corner_id[[1, 2, 3, 0]]
        self.edge_condition[face_edge] = edge_id[[1, 2, 3, 0]]

        # update the cubes' orientation and position
        # no need to change the orientation of corners for U and D
        # no need to change the orientation of edges for U and D
        self.corners[corner_id[0]].position = 3
        self.corners[corner_id[1]].position = 0
        self.corners[corner_id[2]].position = 1
        self.corners[corner_id[3]].position = 2

        self.edges[edge_id[0]].position = 3
        self.edges[edge_id[1]].position = 0
        self.edges[edge_id[2]].position = 1
        self.edges[edge_id[3]].position = 2

    def opt_U_2(self):

        face_corner = [0, 1, 2, 3]
        face_edge = [0, 1, 2, 3]

        corner_id = self.corner_condition[face_corner]
        edge_id = self.edge_condition[face_edge]

        # update the corner and edge condition
        self.corner_condition[face_corner] = corner_id[[2, 3, 0, 1]]
        self.edge_condition[face_edge] = edge_id[[2, 3, 0, 1]]

        # update the cubes' orientation and position
        # no need to change the orientation of corners for U and D
        # no need to change the orientation of edges for U and D
        self.corners[corner_id[0]].position = 2
        self.corners[corner_id[1]].position = 3
        self.corners[corner_id[2]].position = 0
        self.corners[corner_id[3]].position = 1

        self.edges[edge_id[0]].position = 2
        self.edges[edge_id[1]].position = 3
        self.edges[edge_id[2]].position = 0
        self.edges[edge_id[3]].position = 1

    def opt_U_3(self):

        face_corner = [0, 1, 2, 3]
        face_edge = [0, 1, 2, 3]

        corner_id = self.corner_condition[face_corner]
        edge_id = self.edge_condition[face_edge]

        # update the corner and edge condition
        self.corner_condition[face_corner] = corner_id[[3, 0, 1, 2]]
        self.edge_condition[face_edge] = edge_id[[3, 0, 1, 2]]

        # update the cubes' orientation and position
        # no need to change the orientation of corners for U and D
        # no need to change the orientation of edges for U and D
        self.corners[corner_id[0]].position = 1
        self.corners[corner_id[1]].position = 2
        self.corners[corner_id[2]].position = 3
        self.corners[corner_id[3]].position = 0

        self.edges[edge_id[0]].position = 1
        self.edges[edge_id[1]].position = 2
        self.edges[edge_id[2]].position = 3
        self.edges[edge_id[3]].position = 0

    def opt_D_3(self):

        face_corner = [4, 5, 6, 7]
        face_edge = [4, 5, 6, 7]

        corner_id = self.corner_condition[face_corner]
        edge_id = self.edge_condition[face_edge]

        # update the corner and edge condition
        self.corner_condition[face_corner] = corner_id[[1, 2, 3, 0]]
        self.edge_condition[face_edge] = edge_id[[1, 2, 3, 0]]

        # update the cubes' orientation and position
        # no need to change the orientation of corners for U and D
        # no need to change the orientation of edges for U and D
        self.corners[corner_id[0]].position = 7
        self.corners[corner_id[1]].position = 4
        self.corners[corner_id[2]].position = 5
        self.corners[corner_id[3]].position = 6

        self.edges[edge_id[0]].position = 7
        self.edges[edge_id[1]].position = 4
        self.edges[edge_id[2]].position = 5
        self.edges[edge_id[3]].position = 6

    def opt_D_2(self):

        face_corner = [4, 5, 6, 7]
        face_edge = [4, 5, 6, 7]

        corner_id = self.corner_condition[face_corner]
        edge_id = self.edge_condition[face_edge]

        # update the corner and edge condition
        self.corner_condition[face_corner] = corner_id[[2, 3, 0, 1]]
        self.edge_condition[face_edge] = edge_id[[2, 3, 0, 1]]

        # update the cubes' orientation and position
        # no need to change the orientation of corners for U and D
        # no need to change the orientation of edges for U and D
        self.corners[corner_id[0]].position = 6
        self.corners[corner_id[1]].position = 7
        self.corners[corner_id[2]].position = 4
        self.corners[corner_id[3]].position = 5

        self.edges[edge_id[0]].position = 6
        self.edges[edge_id[1]].position = 7
        self.edges[edge_id[2]].position = 4
        self.edges[edge_id[3]].position = 5

    def opt_D_1(self):

        face_corner = [4, 5, 6, 7]
        face_edge = [4, 5, 6, 7]

        corner_id = self.corner_condition[face_corner]
        edge_id = self.edge_condition[face_edge]

        # update the corner and edge condition
        self.corner_condition[face_corner] = corner_id[[3, 0, 1, 2]]
        self.edge_condition[face_edge] = edge_id[[3, 0, 1, 2]]

        # update the cubes' orientation and position
        # no need to change the orientation of corners for U and D
        # no need to change the orientation of edges for U and D
        self.corners[corner_id[0]].position = 5
        self.corners[corner_id[1]].position = 6
        self.corners[corner_id[2]].position = 7
        self.corners[corner_id[3]].position = 4

        self.edges[edge_id[0]].position = 5
        self.edges[edge_id[1]].position = 6
        self.edges[edge_id[2]].position = 7
        self.edges[edge_id[3]].position = 4

    def opt_F_1(self):

        face_corner = [0, 4, 7, 3]
        face_edge = [8, 7, 11, 3]

        corner_id = self.corner_condition[face_corner]
        edge_id = self.edge_condition[face_edge]

        # update the corner and edge condition
        self.corner_condition[face_corner] = corner_id[[3, 0, 1, 2]]
        self.edge_condition[face_edge] = edge_id[[3, 0, 1, 2]]

        # update the corner and edge cubes' position and orientation
        self.corners[corner_id[0]].position = 4
        self.corners[corner_id[0]].change_orien(opt=2)
        self.corners[corner_id[1]].position = 7
        self.corners[corner_id[1]].change_orien(opt=1)
        self.corners[corner_id[2]].position = 3
        self.corners[corner_id[2]].change_orien(opt=2)
        self.corners[corner_id[3]].position = 0
        self.corners[corner_id[3]].change_orien(opt=1)

        self.edges[edge_id[0]].position = 7
        self.edges[edge_id[0]].change_orien()
        self.edges[edge_id[1]].position = 11
        self.edges[edge_id[1]].change_orien()
        self.edges[edge_id[2]].position = 3
        self.edges[edge_id[2]].change_orien()
        self.edges[edge_id[3]].position = 8
        self.edges[edge_id[3]].change_orien()

    def opt_F_2(self):

        face_corner = [0, 4, 7, 3]
        face_edge = [8, 7, 11, 3]

        corner_id = self.corner_condition[face_corner]
        edge_id = self.edge_condition[face_edge]

        # update the corner and edge condition
        self.corner_condition[face_corner] = corner_id[[2, 3, 0, 1]]
        self.edge_condition[face_edge] = edge_id[[2, 3, 0, 1]]

        # update the corner and edge cubes' position and orientation
        self.corners[corner_id[0]].position = 7
        self.corners[corner_id[1]].position = 3
        self.corners[corner_id[2]].position = 0
        self.corners[corner_id[3]].position = 4

        self.edges[edge_id[0]].position = 11
        self.edges[edge_id[1]].position = 3
        self.edges[edge_id[2]].position = 8
        self.edges[edge_id[3]].position = 7


    def opt_F_3(self):

        face_corner = [0, 4, 7, 3]
        face_edge = [8, 7, 11, 3]

        corner_id = self.corner_condition[face_corner]
        edge_id = self.edge_condition[face_edge]

        # update the corner and edge condition
        self.corner_condition[face_corner] = corner_id[[1, 2, 3, 0]]
        self.edge_condition[face_edge] = edge_id[[1, 2, 3, 0]]

        # update the corner and edge cubes' position and orientation
        self.corners[corner_id[0]].position = 3
        self.corners[corner_id[0]].change_orien(opt=2)
        self.corners[corner_id[1]].position = 0
        self.corners[corner_id[1]].change_orien(opt=1)
        self.corners[corner_id[2]].position = 4
        self.corners[corner_id[2]].change_orien(opt=2)
        self.corners[corner_id[3]].position = 7
        self.corners[corner_id[3]].change_orien(opt=1)

        self.edges[edge_id[0]].position = 3
        self.edges[edge_id[0]].change_orien()
        self.edges[edge_id[1]].position = 8
        self.edges[edge_id[1]].change_orien()
        self.edges[edge_id[2]].position = 7
        self.edges[edge_id[2]].change_orien()
        self.edges[edge_id[3]].position = 11
        self.edges[edge_id[3]].change_orien()

    def opt_B_1(self):

        face_corner = [1, 2, 6, 5]
        face_edge = [1, 10, 5, 9]

        corner_id = self.corner_condition[face_corner]
        edge_id = self.edge_condition[face_edge]

        # update the corner and edge condition
        self.corner_condition[face_corner] = corner_id[[3, 0, 1, 2]]
        self.edge_condition[face_edge] = edge_id[[3, 0, 1, 2]]

        # update the corner and edge cubes' position and orientation
        self.corners[corner_id[0]].position = 2
        self.corners[corner_id[0]].change_orien(opt=1)
        self.corners[corner_id[1]].position = 6
        self.corners[corner_id[1]].change_orien(opt=2)
        self.corners[corner_id[2]].position = 5
        self.corners[corner_id[2]].change_orien(opt=1)
        self.corners[corner_id[3]].position = 1
        self.corners[corner_id[3]].change_orien(opt=2)

        self.edges[edge_id[0]].position = 10
        self.edges[edge_id[0]].change_orien()
        self.edges[edge_id[1]].position = 5
        self.edges[edge_id[1]].change_orien()
        self.edges[edge_id[2]].position = 9
        self.edges[edge_id[2]].change_orien()
        self.edges[edge_id[3]].position = 1
        self.edges[edge_id[3]].change_orien()

    def opt_B_2(self):

        face_corner = [1, 2, 6, 5]
        face_edge = [1, 10, 5, 9]

        corner_id = self.corner_condition[face_corner]
        edge_id = self.edge_condition[face_edge]

        # update the corner and edge condition
        self.corner_condition[face_corner] = corner_id[[2, 3, 0, 1]]
        self.edge_condition[face_edge] = edge_id[[2, 3, 0, 1]]

        # update the corner and edge cubes' position and orientation
        self.corners[corner_id[0]].position = 6
        self.corners[corner_id[1]].position = 5
        self.corners[corner_id[2]].position = 1
        self.corners[corner_id[3]].position = 2

        self.edges[edge_id[0]].position = 5
        self.edges[edge_id[1]].position = 9
        self.edges[edge_id[2]].position = 1
        self.edges[edge_id[3]].position = 10

    def opt_B_3(self):

        face_corner = [1, 2, 6, 5]
        face_edge = [1, 10, 5, 9]

        corner_id = self.corner_condition[face_corner]
        edge_id = self.edge_condition[face_edge]

        # update the corner and edge condition
        self.corner_condition[face_corner] = corner_id[[1, 2, 3, 0]]
        self.edge_condition[face_edge] = edge_id[[1, 2, 3, 0]]

        # update the corner and edge cubes' position and orientation
        self.corners[corner_id[0]].position = 5
        self.corners[corner_id[0]].change_orien(opt=1)
        self.corners[corner_id[1]].position = 1
        self.corners[corner_id[1]].change_orien(opt=2)
        self.corners[corner_id[2]].position = 2
        self.corners[corner_id[2]].change_orien(opt=1)
        self.corners[corner_id[3]].position = 6
        self.corners[corner_id[3]].change_orien(opt=2)

        self.edges[edge_id[0]].position = 9
        self.edges[edge_id[0]].change_orien()
        self.edges[edge_id[1]].position = 1
        self.edges[edge_id[1]].change_orien()
        self.edges[edge_id[2]].position = 10
        self.edges[edge_id[2]].change_orien()
        self.edges[edge_id[3]].position = 5
        self.edges[edge_id[3]].change_orien()

    def opt_R_1(self):

        face_corner = [0, 1, 5, 4]
        face_edge = [0, 9, 4, 8]

        corner_id = self.corner_condition[face_corner]
        edge_id = self.edge_condition[face_edge]

        # update the corner and edge condition
        self.corner_condition[face_corner] = corner_id[[3, 0, 1, 2]]
        self.edge_condition[face_edge] = edge_id[[3, 0, 1, 2]]

        # update the corner and edge cubes' position and orientation
        self.corners[corner_id[0]].position = 1
        self.corners[corner_id[0]].change_orien(opt=1)
        self.corners[corner_id[1]].position = 5
        self.corners[corner_id[1]].change_orien(opt=2)
        self.corners[corner_id[2]].position = 4
        self.corners[corner_id[2]].change_orien(opt=1)
        self.corners[corner_id[3]].position = 0
        self.corners[corner_id[3]].change_orien(opt=2)

        self.edges[edge_id[0]].position = 9
        self.edges[edge_id[1]].position = 4
        self.edges[edge_id[2]].position = 8
        self.edges[edge_id[3]].position = 0

    def opt_R_2(self):

        face_corner = [0, 1, 5, 4]
        face_edge = [0, 9, 4, 8]

        corner_id = self.corner_condition[face_corner]
        edge_id = self.edge_condition[face_edge]

        # update the corner and edge condition
        self.corner_condition[face_corner] = corner_id[[2, 3, 0, 1]]
        self.edge_condition[face_edge] = edge_id[[2, 3, 0, 1]]

        # update the corner and edge cubes' position and orientation
        self.corners[corner_id[0]].position = 5
        self.corners[corner_id[1]].position = 4
        self.corners[corner_id[2]].position = 0
        self.corners[corner_id[3]].position = 1

        self.edges[edge_id[0]].position = 4
        self.edges[edge_id[1]].position = 8
        self.edges[edge_id[2]].position = 0
        self.edges[edge_id[3]].position = 9

    def opt_R_3(self):

        face_corner = [0, 1, 5, 4]
        face_edge = [0, 9, 4, 8]

        corner_id = self.corner_condition[face_corner]
        edge_id = self.edge_condition[face_edge]

        # update the corner and edge condition
        self.corner_condition[face_corner] = corner_id[[1, 2, 3, 0]]
        self.edge_condition[face_edge] = edge_id[[1, 2, 3, 0]]

        # update the corner and edge cubes' position and orientation
        self.corners[corner_id[0]].position = 4
        self.corners[corner_id[0]].change_orien(opt=1)
        self.corners[corner_id[1]].position = 0
        self.corners[corner_id[1]].change_orien(opt=2)
        self.corners[corner_id[2]].position = 1
        self.corners[corner_id[2]].change_orien(opt=1)
        self.corners[corner_id[3]].position = 5
        self.corners[corner_id[3]].change_orien(opt=2)

        self.edges[edge_id[0]].position = 8
        self.edges[edge_id[1]].position = 0
        self.edges[edge_id[2]].position = 9
        self.edges[edge_id[3]].position = 4

    def opt_L_1(self):

        face_corner = [2, 3, 7, 6]
        face_edge = [2, 11, 6, 10]

        corner_id = self.corner_condition[face_corner]
        edge_id = self.edge_condition[face_edge]

        # update the corner and edge condition
        self.corner_condition[face_corner] = corner_id[[3, 0, 1, 2]]
        self.edge_condition[face_edge] = edge_id[[3, 0, 1, 2]]

        # update the corner and edge cubes' position and orientation
        self.corners[corner_id[0]].position = 3
        self.corners[corner_id[0]].change_orien(opt=1)
        self.corners[corner_id[1]].position = 7
        self.corners[corner_id[1]].change_orien(opt=2)
        self.corners[corner_id[2]].position = 6
        self.corners[corner_id[2]].change_orien(opt=1)
        self.corners[corner_id[3]].position = 2
        self.corners[corner_id[3]].change_orien(opt=2)

        self.edges[edge_id[0]].position = 11
        self.edges[edge_id[1]].position = 6
        self.edges[edge_id[2]].position = 10
        self.edges[edge_id[3]].position = 2

    def opt_L_2(self):

        face_corner = [2, 3, 7, 6]
        face_edge = [2, 11, 6, 10]

        corner_id = self.corner_condition[face_corner]
        edge_id = self.edge_condition[face_edge]

        # update the corner and edge condition
        self.corner_condition[face_corner] = corner_id[[2, 3, 0, 1]]
        self.edge_condition[face_edge] = edge_id[[2, 3, 0, 1]]

        # update the corner and edge cubes' position and orientation
        self.corners[corner_id[0]].position = 7
        self.corners[corner_id[1]].position = 6
        self.corners[corner_id[2]].position = 2
        self.corners[corner_id[3]].position = 3

        self.edges[edge_id[0]].position = 6
        self.edges[edge_id[1]].position = 10
        self.edges[edge_id[2]].position = 2
        self.edges[edge_id[3]].position = 11

    def opt_L_3(self):

        face_corner = [2, 3, 7, 6]
        face_edge = [2, 11, 6, 10]

        corner_id = self.corner_condition[face_corner]
        edge_id = self.edge_condition[face_edge]

        # update the corner and edge condition
        self.corner_condition[face_corner] = corner_id[[1, 2, 3, 0]]
        self.edge_condition[face_edge] = edge_id[[1, 2, 3, 0]]

        # update the corner and edge cubes' position and orientation
        self.corners[corner_id[0]].position = 6
        self.corners[corner_id[0]].change_orien(opt=1)
        self.corners[corner_id[1]].position = 2
        self.corners[corner_id[1]].change_orien(opt=2)
        self.corners[corner_id[2]].position = 3
        self.corners[corner_id[2]].change_orien(opt=1)
        self.corners[corner_id[3]].position = 7
        self.corners[corner_id[3]].change_orien(opt=2)

        self.edges[edge_id[0]].position = 10
        self.edges[edge_id[1]].position = 2
        self.edges[edge_id[2]].position = 11
        self.edges[edge_id[3]].position = 6


def U1(r):
    r.opt_U_1()


def U2(r):
    r.opt_U_2()


def U3(r):
    r.opt_U_3()


def D1(r):
    r.opt_D_1()


def D2(r):
    r.opt_D_2()


def D3(r):
    r.opt_D_3()


def F1(r):
    r.opt_F_1()


def F2(r):
    r.opt_F_2()


def F3(r):
    r.opt_F_3()


def B1(r):
    r.opt_B_1()


def B2(r):
    r.opt_B_2()


def B3(r):
    r.opt_B_3()


def L1(r):
    r.opt_L_1()


def L2(r):
    r.opt_L_2()


def L3(r):
    r.opt_L_3()


def R1(r):
    r.opt_R_1()


def R2(r):
    r.opt_R_2()


def R3(r):
    r.opt_R_3()
