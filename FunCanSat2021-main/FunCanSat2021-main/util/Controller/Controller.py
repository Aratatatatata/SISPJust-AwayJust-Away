import math

from . import servo 

class Controller():
    def __init__(self):
        self.l_servo = servo.MG996R(12)
        self.r_servo = servo.MG996R(18)

        self.l_servo.write(0)
        self.r_servo.write(0)

    def gps_LR(self, gps_x, gps_y, dir_x, dir_y):
        dis_x = gps_x - dir_x
        dis_y = gps_y - dir_y
        if(dis_y >= 0 and dis_x >= 0) or (dis_y < 0 and dis_x < 0):
            return 0
        else:
            return 1
            
    def direction(self, gps_x, gps_y):
        position = [
                [41.833705, 140.770666],
                [41.833705, 140.770666],
                [41.833705, 140.770666],
                [41.833705, 140.770666]
        ]

        n_dir = abs(position[0][0] - gps_x) + abs(position[0][1] - gps_y)
        e_dir = abs(position[1][0] - gps_x) + abs(position[1][1] - gps_y)
        s_dir = abs(position[2][0] - gps_x) + abs(position[2][1] - gps_y)
        w_dir = abs(position[3][0] - gps_x) + abs(position[3][1] - gps_y)
            
        go_dir = min(self, n_dir, e_dir, s_dir, w_dir)
        if go_dir == n_dir:
            return position[0][0], position[0][1]
        elif go_dir == e_dir:
            return position[1][0], position[1][1]
        elif go_dir == s_dir:
            return position[2][0], position[2][1]
        else:
            return position[3][0], position[3][1]
            
    def uturn(self, gps_x, gps_y, dir_x, dir_y):
        LR = self.gps_LR(gps_x, gps_y, dir_x, dir_y)
        dis_x = abs(gps_x - dir_x)
        dis_y = abs(gps_y - dir_y)
        if abs(dis_x - dis_y) < 1:
            self.l_servo.write(120)
        elif dis_x > dis_y and LR == 0:
            self.l_servo.write(90)
        elif dis_y > dis_x and LR == 0:
            self.r_servo.write(90)
        elif dis_x > dis_y and LR == 1:
            self.r_servo.write(90)
        elif dis_y > dis_x and LR == 1:
            self.l_servo.write(90)


    def dis_gps(self, old_x, old_y, gps_x, gps_y, dir_x, dir_y):
        dis_now_x = abs(old_x - gps_x)
        dis_now_y = abs(old_y - gps_y)
        dis_goal_x = abs(dir_x - gps_x)
        dis_goal_y = abs(dir_y - gps_y)
        asin_now = math.degrees(math.atan2(dis_now_y, dis_now_x))
        asin_goal = math.degrees(math.atan2(dis_goal_y, dis_goal_x))
        let = asin_goal - asin_now
        abs_let = abs(let)
        LR = self.gps_LR(gps_x, gps_y, dir_x, dir_y)
        if dis_goal_x + dis_goal_y <= 0.002:
            self.l_servo.write(180)
            fin = True
        elif LR == 0 and let > 0:
            self.l_servo.write(abs_let)
            #print('hidari')
        elif LR == 0 and abs_let < 0.1:
            pass
            #print('iji')
        elif LR == 0 and let < 0:
            self.r_servo.write(180)
            #print('migi')
        elif LR == 1 and abs_let < 0.1:
            pass
            #print('iji')
        elif LR ==1 and let > 0:
            self.r_servo.write(180)
        elif LR == 1 and let < 0:
            self.l_servo.write(abs_let)
            #print('hidari')

        return LR, let
