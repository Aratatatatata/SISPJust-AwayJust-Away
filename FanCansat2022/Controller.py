import math

#欲しいものとして左右どちらを引けばいいか
#

class Controller():
    def __init__(self):
          
    
    
    #最も近いゴール座標を返す。
    def set_goal(self, gps_x, gps_y):
        position = [
                [41.842300, 140.767590],
                [41.842220, 140.767666],
                [41.842220, 140.767700],
                [41.842100, 140.767590]
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
            

    #ひとつ前のgpsと今のgps、今のgpsとgoal、それぞれの傾きから右左を出す
    def dis_gps(self, old_x, old_y, now_x, now_y, dir_x, dir_y):
        dis_now_x = now_x - old_x 
        dis_now_y = now_y -old_y
        dis_goal_x = dir_x - now_x
        dis_goal_y = dir_y - now_y
        asin_now = math.degrees(math.atan2(dis_now_y, dis_now_x))#傾きを角度にする
        asin_goal = math.degrees(math.atan2(dis_goal_y, dis_goal_x))#傾きを角度にする
        let = asin_goal - asin_now    #ゴールが左右どちらにあるかを出す。この値が正の値であればgoalは左にある。
        
　　　　return let
