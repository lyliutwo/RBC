'''
定义一个魔方的数学模型
魔方的状态
魔方的操作
'''
# 颜色编号：绿：0 红：1 白：2 橙：3 黄：4 蓝：5
# 魔方方向设定： U：绿 F：红
color_list = ["G", "R", "W", "O", "Y", "B"]
opt_list = ["R", "L", "U", "D", "F", "B"]

import numpy as np


class edge:

    def __init__(self, id, position=-1, orientation=1):
        '''
            一个棱块有：
                两个色块
                方向
                位置
        '''
        self.id = id
        self.color = self.paint()
        if position == -1:
            self.position = self.id
        else:
            self.position = position
        self.orientation = orientation

    def paint(self):
        color_list = [[0, 2], [0, 3], [0, 4], [0, 1], [5, 2], [5, 3], [5, 4], [5, 1],
                      [1, 2], [3, 2], [3, 4], [1, 4]]
        return color_list[self.id]

    def change_orien(self):
        self.orientation = -self.orientation
        return self.orientation

    def show_color_face(self, face):
        if self.position in [1, 3, 5, 7]:
            if self.orientation == 1:
                color_order = [0, 1, -1]
            else:
                color_order = [1, 0, -1]
        elif self.position in [0, 2, 4, 6]:
            if self.orientation == 1:
                color_order = [0, -1, 1]
            else:
                color_order = [1, -1, 0]
        elif self.position in [8, 9, 10, 11]:
            if self.orientation == 1:
                color_order = [-1, 0, 1]
            else:
                color_order = [-1, 1, 0]

        if color_order[face] == -1:
            raise Exception("The edge don't in this face!", face)
        else:
            return color_list[self.color[color_order[face]]]


class corner:

    def __init__(self, id, position=-1, orientation=0):
        self.id = id
        self.color = self.paint()
        if position == -1:
            self.position = self.id
        else:
            self.position = position
        self.orientation = orientation

    def paint(self):
        corner_color_list = [[0, 1, 2], [0, 3, 2], [0, 3, 4], [0, 1, 4],
                       [5, 1, 2], [5, 3, 2], [5, 3, 4], [5, 1, 4]]
        return corner_color_list[self.id]

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

    def show_color_face(self, face):   # face: 0-U,D 1-F,B 2-R,L
        a_group = [0, 2, 5, 7]
        b_group = [1, 3, 4, 6]
        if (self.id in a_group and self.position in a_group) or \
                (self.id in b_group and self.position in b_group):
            if self.orientation == 0:
                color_order = [0, 1, 2]
            elif self.orientation == 1:
                color_order = [1, 2, 0]
            elif self.orientation == -1:
                color_order = [2, 0, 1]
        else:
            if self.orientation == 0:
                color_order = [0, 2, 1]
            elif self.orientation == 1:
                color_order = [1, 0, 2]
            elif self.orientation == -1:
                color_order = [2, 1, 0]

        return color_list[self.color[color_order[face]]]


class face:
    def __init__(self, id):
        self.id = id
        self.corners_id = list()
        self.edges_id = list()


class rubik_cube:

    def __init__(self, id, random=False, random_step=0):

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
        self.opt_log = list()  # ["R3", "L2",...]
        self.random_step = random_step
        if random:
            self.upset(self.random_step, print_root=False)

    def is_solved(self):
        for c in self.corners:
            if not (c.id == c.position and c.orientation == 0):
                return False
        for e in self.edges:
            if not(e.id == e.position and e.orientation == 1):
                return False
        return True

    def copy_corner(self, corner_list):
        self.corners = corner_list

    def copy_edge(self, edge_list):
        self.edges = edge_list

    def digit_remote(self, opt_id):
        '''
        R: 0, 6, 12
        L: 1, 7, 13
        U: 2, 8, 14
        D: 3, 9, 15
        F: 4, 10, 16
        B: 5, 11, 17
        :param opt_id:
        :return:
        '''
        if opt_id not in range(18):
            raise Exception("Wrong operation with id of {}".format(opt_id))
        self.remote(opt=opt_list[opt_id % 6], stride=opt_id // 6+1, write_log=True)

    def remote(self, opt, stride=1, write_log=True):
        if opt == "R":
            if stride % 4 == 0:
                pass
            elif stride % 4 == 1:
                self.opt_R_1()
            elif stride % 4 == 2:
                self.opt_R_2()
            else:
                self.opt_R_3()

        if opt == "L":
            if stride % 4 == 0:
                pass
            elif stride % 4 == 1:
                self.opt_L_1()
            elif stride % 4 == 2:
                self.opt_L_2()
            else:
                self.opt_L_3()

        if opt == "U":
            if stride % 4 == 0:
                pass
            elif stride % 4 == 1:
                self.opt_U_1()
            elif stride % 4 == 2:
                self.opt_U_2()
            else:
                self.opt_U_3()

        if opt == "D":
            if stride % 4 == 0:
                pass
            elif stride % 4 == 1:
                self.opt_D_1()
            elif stride % 4 == 2:
                self.opt_D_2()
            else:
                self.opt_D_3()

        if opt == "F":
            if stride % 4 == 0:
                pass
            elif stride % 4 == 1:
                self.opt_F_1()
            elif stride % 4 == 2:
                self.opt_F_2()
            else:
                self.opt_F_3()

        if opt == "B":
            if stride % 4 == 0:
                pass
            elif stride % 4 == 1:
                self.opt_B_1()
            elif stride % 4 == 2:
                self.opt_B_2()
            else:
                self.opt_B_3()

        if write_log:
            self.opt_log.append([opt, stride])

    def vectorize(self):
        # 将魔方状态转化为20维向量，用于计算Q
        v = np.zeros(20)
        for i in range(8):
            c = self.corners[i]
            p = c.position
            o = c.orientation
            v[i] = p + o * 8

        for j in range(12):
            e = self.edges[j]
            p = e.position
            o = e.orientation
            v[i + 8] = p + o * 12

        return v

    def visualize(self):
        face_U = [[2, 1, 3, 0], [1, 2, 0, 3], 0]  # [ids of corners, ids of edges, id of center]
        face_F = [[3, 0, 7, 4], [3, 11, 8, 7], 1]
        face_R = [[0, 1, 4, 5], [0, 8, 9, 4], 2]
        face_B = [[1, 2, 5, 6], [1, 9, 10, 5], 3]
        face_L = [[2, 3, 6, 7], [2, 10, 11, 6], 4]
        face_D = [[7, 4, 6, 5], [7, 6, 4, 5], 5]

        face_color_U = ["G", "G", "G", "G", "G", "G", "G", "G", "G"]
        face_color_U[0] = self.corners[self.corner_condition[2]].show_color_face(0)
        face_color_U[1] = self.edges[self.edge_condition[1]].show_color_face(0)
        face_color_U[2] = self.corners[self.corner_condition[1]].show_color_face(0)
        face_color_U[3] = self.edges[self.edge_condition[2]].show_color_face(0)
        face_color_U[5] = self.edges[self.edge_condition[0]].show_color_face(0)
        face_color_U[6] = self.corners[self.corner_condition[3]].show_color_face(0)
        face_color_U[7] = self.edges[self.edge_condition[3]].show_color_face(0)
        face_color_U[8] = self.corners[self.corner_condition[0]].show_color_face(0)

        face_color_F = ["R", "R", "R", "R", "R", "R", "R", "R", "R"]
        face_color_F[0] = self.corners[self.corner_condition[3]].show_color_face(1)
        face_color_F[1] = self.edges[self.edge_condition[3]].show_color_face(1)
        face_color_F[2] = self.corners[self.corner_condition[0]].show_color_face(1)
        face_color_F[3] = self.edges[self.edge_condition[11]].show_color_face(1)
        face_color_F[5] = self.edges[self.edge_condition[8]].show_color_face(1)
        face_color_F[6] = self.corners[self.corner_condition[7]].show_color_face(1)
        face_color_F[7] = self.edges[self.edge_condition[7]].show_color_face(1)
        face_color_F[8] = self.corners[self.corner_condition[4]].show_color_face(1)

        face_color_R = ["W", "W", "W", "W", "W", "W", "W", "W", "W"]
        face_color_R[0] = self.corners[self.corner_condition[0]].show_color_face(2)
        face_color_R[1] = self.edges[self.edge_condition[0]].show_color_face(2)
        face_color_R[2] = self.corners[self.corner_condition[1]].show_color_face(2)
        face_color_R[3] = self.edges[self.edge_condition[8]].show_color_face(2)
        face_color_R[5] = self.edges[self.edge_condition[9]].show_color_face(2)
        face_color_R[6] = self.corners[self.corner_condition[4]].show_color_face(2)
        face_color_R[7] = self.edges[self.edge_condition[4]].show_color_face(2)
        face_color_R[8] = self.corners[self.corner_condition[5]].show_color_face(2)

        face_color_B = ["O", "O", "O", "O", "O", "O", "O", "O", "O"]
        face_color_B[0] = self.corners[self.corner_condition[1]].show_color_face(1)
        face_color_B[1] = self.edges[self.edge_condition[1]].show_color_face(1)
        face_color_B[2] = self.corners[self.corner_condition[2]].show_color_face(1)
        face_color_B[3] = self.edges[self.edge_condition[9]].show_color_face(1)
        face_color_B[5] = self.edges[self.edge_condition[10]].show_color_face(1)
        face_color_B[6] = self.corners[self.corner_condition[5]].show_color_face(1)
        face_color_B[7] = self.edges[self.edge_condition[5]].show_color_face(1)
        face_color_B[8] = self.corners[self.corner_condition[6]].show_color_face(1)

        face_color_L = ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"]
        face_color_L[0] = self.corners[self.corner_condition[2]].show_color_face(2)
        face_color_L[1] = self.edges[self.edge_condition[2]].show_color_face(2)
        face_color_L[2] = self.corners[self.corner_condition[3]].show_color_face(2)
        face_color_L[3] = self.edges[self.edge_condition[10]].show_color_face(2)
        face_color_L[5] = self.edges[self.edge_condition[11]].show_color_face(2)
        face_color_L[6] = self.corners[self.corner_condition[6]].show_color_face(2)
        face_color_L[7] = self.edges[self.edge_condition[6]].show_color_face(2)
        face_color_L[8] = self.corners[self.corner_condition[7]].show_color_face(2)

        face_color_D = ["B", "B", "B", "B", "B", "B", "B", "B", "B"]
        face_color_D[0] = self.corners[self.corner_condition[7]].show_color_face(0)
        face_color_D[1] = self.edges[self.edge_condition[7]].show_color_face(0)
        face_color_D[2] = self.corners[self.corner_condition[4]].show_color_face(0)
        face_color_D[3] = self.edges[self.edge_condition[6]].show_color_face(0)
        face_color_D[5] = self.edges[self.edge_condition[4]].show_color_face(0)
        face_color_D[6] = self.corners[self.corner_condition[6]].show_color_face(0)
        face_color_D[7] = self.edges[self.edge_condition[5]].show_color_face(0)
        face_color_D[8] = self.corners[self.corner_condition[5]].show_color_face(0)

        scan1 = "        {0}{1}{2}".format(face_color_U[0], face_color_U[1], face_color_U[2])
        scan2 = "        {0}{1}{2}".format(face_color_U[3], face_color_U[4], face_color_U[5])
        scan3 = "        {0}{1}{2}".format(face_color_U[6], face_color_U[7], face_color_U[8])
        scan4 = "{0}{1}{2} {3}{4}{5} {6}{7}{8} {9}{10}{11}"\
                .format(face_color_L[0], face_color_L[1], face_color_L[2], \
                        face_color_F[0], face_color_F[1], face_color_F[2], \
                        face_color_R[0], face_color_R[1], face_color_R[2], \
                        face_color_B[0], face_color_B[1], face_color_B[2])
        scan5 = "{0}{1}{2} {3}{4}{5} {6}{7}{8} {9}{10}{11}" \
            .format(face_color_L[3], face_color_L[4], face_color_L[5], \
                    face_color_F[3], face_color_F[4], face_color_F[5], \
                    face_color_R[3], face_color_R[4], face_color_R[5], \
                    face_color_B[3], face_color_B[4], face_color_B[5])
        scan6 = "{0}{1}{2} {3}{4}{5} {6}{7}{8} {9}{10}{11}" \
            .format(face_color_L[6], face_color_L[7], face_color_L[8], \
                    face_color_F[6], face_color_F[7], face_color_F[8], \
                    face_color_R[6], face_color_R[7], face_color_R[8], \
                    face_color_B[6], face_color_B[7], face_color_B[8])
        scan7 = "        {0}{1}{2}".format(face_color_D[0], face_color_D[1], face_color_D[2])
        scan8 = "        {0}{1}{2}".format(face_color_D[3], face_color_D[4], face_color_D[5])
        scan9 = "        {0}{1}{2}".format(face_color_D[6], face_color_D[7], face_color_D[8])

        print(scan1)
        print(scan2)
        print(scan3)
        print(scan4)
        print(scan5)
        print(scan6)
        print(scan7)
        print(scan8)
        print(scan9)

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

    def upset(self, step, print_root=True):
        for _ in range(step):
            opt_id = np.random.randint(18)
            opt = opt_list[opt_id % 6]
            stride = opt_id // 6 + 1
            self.remote(opt, stride, write_log=True)

        if print_root:
            print("The cube is upset as follow:")
            self.show_log(part="upset")

    def show_log(self, part="all"):
        if part == "all":
            for opt, stride in self.opt_log:
                print("{0}{1}".format(opt, stride), end="  ")
            print(" ")
        elif part == "upset" or "random":
            for opt, stride in self.opt_log[:self.random_step]:
                print("{0}{1}".format(opt, stride), end="  ")
            print(" ")
        elif part == "solve":
            for opt, stride in self.opt_log[self.random_step:]:
                print("{0}{1}".format(opt, stride), end="  ")
            print(" ")
        else:
            raise Exception("part = 'all' or 'upset' or 'solve'.")




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
