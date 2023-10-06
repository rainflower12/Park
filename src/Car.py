from map import Map
import threading
import time
import sys


class Car(threading.Thread):
    def __init__(self, x, y, map: Map, stage=1, pre_x=0, pre_y=0, direction=0, pre_direction=0):
        """
        Initialize the car object
        Args:
            param x: x coordinate
            param y: y coordinate
            param map: Map object
            param pre_x: previous x coordinate
            param pre_y: previous y coordinate
            param direction: direction of the car
            param pre_direction: previous direction of the car
        """
        super().__init__()
        self.x = x
        self.y = y
        self.map = map
        self.pre_x = pre_x  # 初始化上一步坐标为当前坐标
        self.pre_y = pre_y
        self.direction = direction
        self.pre_direction = pre_direction
        self.flag = 1
        self.pass_road = []
        self.index = 0
        self.stage = stage
        Car.lock = threading.Lock()

    def get_dest(self, dest_x, dest_y):
        self.dest_x = dest_x
        self.dest_y = dest_y

    def drive(self):
        """
        Move the car
        """
        if self.direction == 1:  # Move up
            # self.pre_x = self.x
            # self.pre_y = self.y
            self.x -= 1
        elif self.direction == 2:  # Move down
            # self.pre_x = self.x
            # self.pre_y = self.y
            self.x += 1
        elif self.direction == 3:  # Move left
            # self.pre_x = self.x
            # self.pre_y = self.y
            self.y -= 1
        elif self.direction == 4:  # Move right
            # self.pre_x = self.x
            # self.pre_y = self.y
            self.y += 1
        else:
            print(self.direction)
            print("Invalid direction value. The car will stay in its current position.")

    def add_position(self):
        """
        Show the position of the car
        """
        # print(f"({self.x}, {self.y})", end=" ", flush=True)
        self.pass_road.append((self.x, self.y))

    def move(self, dest_x, dest_y):
        """
        Move the car and show the position
        """
        # 如果车辆已启动
        if self.flag == 1:
            # 目的地是停车场
            if (self.map.layout.iloc[dest_x, dest_y] == 1):
                self.temp_dest_x, self.temp_dest_y = self.map.get_closest_road(dest_x, dest_y)
            else:
                self.temp_dest_x, self.temp_dest_y = dest_x, dest_y
            while self.x != self.temp_dest_x or self.y != self.temp_dest_y:
                while True:
                    self.map.navigate_car_to_dest(self, self.temp_dest_x, self.temp_dest_y)
                    if self.check_collision() is False:
                        print(self.x, self.y, self.direction)
                        self.drive()
                        self.add_position()
                        break
                    time.sleep(1)
            # 到达目的地退出
            if (self.temp_dest_x, self.temp_dest_y) == (dest_x, dest_y):
                with self.lock:
                    print(str(threading.get_ident()) + " Destination reached!")
                    self.flag = 0
                    print("The car pass the road is:", end=" ")
                    print(self.pass_road)
                    self.stage -= 1
                    if self.stage == 0:
                        sys.exit()
            else:
                if dest_x < self.x:
                    self.direction = 1
                elif dest_x > self.x:
                    self.direction = 2
                elif dest_y < self.y:
                    self.direction = 3
                elif dest_y > self.y:
                    self.direction = 4
                while True:
                    if self.check_collision() is False:
                        dest = (dest_x, dest_y)
                        self.pass_road.append(dest)
                        self.x = dest_x
                        self.y = dest_y
                        with self.lock:
                            print(str(threading.get_ident()) + " Parking reached!")
                            self.flag = 0
                            print("The car pass the road is:", end=" ")
                            print(self.pass_road)
                            self.stage -= 1
                            if self.stage == 0:
                                sys.exit()
        else:
            print("car stop")

    def check_collision(self) -> bool:
        """
        Check if there is a collision
        Returns:
            bool: whether to stop
        """
        # if ahead self direction have a car , then try to overtake
        self.ahead_x = 0
        self.ahead_y = 0
        if self.direction == 1:  # Move up
            self.ahead_x = self.x - 1
            self.ahead_y = self.y
        elif self.direction == 2:  # Move down
            self.ahead_x = self.x + 1
            self.ahead_y = self.y
        elif self.direction == 3:  # Move left
            self.ahead_x = self.x
            self.ahead_y = self.y - 1
        elif self.direction == 4:  # Move right
            self.ahead_x = self.x
            self.ahead_y = self.y + 1
        # 无法到达目的地,并且无法超车 退出
        for car in self.map.cars:
            if car != self:
                if (car.x, car.y) == (self.ahead_x, self.ahead_y) and car.flag == 1:
                    # 前车在行使 返回停车等待
                    return True
                if ((car.x, car.y) == (self.ahead_x, self.ahead_y) and car.flag == 0):
                    # 前车到达目的地,并且在我必经之路上,尝试超车
                    # 位置是否支持超车
                    # if (self.map.layout.iloc[car.x, car.y] == 1):
                    #     # 必经之路有停车场 不支持超车 直接抛锚在当前位置, 路线错误
                    #     self.flag = 0
                    #     with self.lock:
                    #         print("Parking has the car")
                    #         print(str(threading.get_ident()) + " Unable to overtake and forced to stop!")
                    #         self.flag = 0
                    #         print("The car pass the road is:", end=" ")
                    #         print(self.pass_road)
                    #         sys.exit()
                    # else:
                    #     if (self.try_overtake(car.x, car.y) is True):
                    #         return False
                    #     elif (self.try_overtake(car.x, car.y) is False):
                    #         # 无可走路径 报错
                    #         with self.lock:
                    #             print("No way to drive")
                    #             print(str(threading.get_ident()) + " Unable to overtake and forced to stop!")
                    #             self.flag = 0
                    #             print("The car pass the road is:", end=" ")
                    #             print(self.pass_road)
                    #             sys.exit()
                    if (self.map.layout.iloc[car.x, car.y] == 1):
                        self.dest_x, self.dest_y = self.map.get_closest_parking(car.x, car.y)
                        self.temp_dest_x, self.temp_dest_y = self.map.get_closest_road(self.dest_x, self.dest_y)
                        # print(self.temp_dest_x, self.temp_dest_y)
                        return True
                    elif (self.map.layout.iloc[car.x, car.y] == 0):
                        if (car.flag == 0):
                            # 唯一超车位置
                            self.try_overtake(car.x, car.y)
                            return True
                        else:
                            return True
        return False

    def try_overtake(self, car_x, car_y):
        """
        Try to overtake
        Returns:
            bool: overtake successful or not
        """
        if self.direction == 1:
            # 寻找可超越路径
            has_car = 0
            target_x = car_x - 1
            target_y = car_y
            across_x = self.x - 1
            across_y = self.y - 1
            for car in self.map.cars:
                if (car.x, car.y) == (target_x, target_y):
                    has_car = 1
            if (has_car):
                return False
            for car in self.map.cars:
                if (car.x, car.y) == (across_x, across_y):
                    has_car = 1
                    break
            if (has_car):
                return False
            # 可以超车
            if (self.map.get_distance(target_x, target_y, self.dest_x, self.dest_y)
                    < self.map.get_distance(self.x, self.y, self.dest_x, self.dest_y)):
                self.x = across_x
                self.y = across_y
                temp = (self.x, self.y)
                self.pass_road.append(temp)
                self.x = target_x
                self.y = target_y
                temp = (self.x, self.y)
                self.pass_road.append(temp)
                return True
            else:
                return False
        elif self.direction == 2:
            has_car = 0
            target_x = car_x + 1
            target_y = car_y
            across_x = self.x + 1
            across_y = self.y + 1
            for car in self.map.cars:
                if (car.x, car.y) == (target_x, target_y):
                    has_car = 1
                    break
            if (has_car):
                return False
            for car in self.map.cars:
                if (car.x, car.y) == (across_x, across_y):
                    has_car = 1
                    break
            if (has_car):
                return False
            # 可以超车
            if (self.map.get_distance(target_x, target_y, self.dest_x, self.dest_y)
                    < self.map.get_distance(self.x, self.y, self.dest_x, self.dest_y)):
                self.x = across_x
                self.y = across_y
                temp = (self.x, self.y)
                self.pass_road.append(temp)
                self.x = target_x
                self.y = target_y
                temp = (self.x, self.y)
                self.pass_road.append(temp)
                return True
            else:
                return False
        elif self.direction == 3:
            has_car = 0
            target_x = car_x
            target_y = car_y - 1
            across_x = self.x + 1
            across_y = self.y - 1
            for car in self.map.cars:
                if (car.x, car.y) == (target_x, target_y):
                    has_car = 1
                    break
            if (has_car):
                return False
            for car in self.map.cars:
                if (car.x, car.y) == (across_x, across_y):
                    has_car = 1
                    break
            if (has_car):
                return False
            # 可以超车
            if (self.map.get_distance(target_x, target_y, self.dest_x, self.dest_y)
                    < self.map.get_distance(self.x, self.y, self.dest_x, self.dest_y)):
                self.x = across_x
                self.y = across_y
                temp = (self.x, self.y)
                self.pass_road.append(temp)
                self.x = target_x
                self.y = target_y
                temp = (self.x, self.y)
                self.pass_road.append(temp)
                return True
            else:
                return False
        elif self.direction == 4:
            has_car = 0
            target_x = car_x
            target_y = car_y + 1
            across_x = self.x - 1
            across_y = self.y + 1
            for car in self.map.cars:
                if (car.x, car.y) == (target_x, target_y):
                    has_car = 1
                    break
            if (has_car):
                return False
            for car in self.map.cars:
                if (car.x, car.y) == (across_x, across_y):
                    has_car = 1
                    break
            if (has_car):
                return False
            # 可以超车
            if (self.map.get_distance(target_x, target_y, self.dest_x, self.dest_y)
                    < self.map.get_distance(self.x, self.y, self.dest_x, self.dest_y)):
                self.x = across_x
                self.y = across_y
                temp = (self.x, self.y)
                self.pass_road.append(temp)
                self.x = target_x
                self.y = target_y
                temp = (self.x, self.y)
                self.pass_road.append(temp)
                return True
            else:
                return False
        return False

    def stop_the_car(self):
        self.flag = 0

    def start_the_car(self):
        self.get_dest(1, 3)
        self.move(self.dest_x, self.dest_y)
        time.sleep(20)
        self.pass_road = []
        self.get_dest(5, 20)
        self.flag = 1
        self.move(self.dest_x, self.dest_y)
        sys.exit()

    def run(self):
        if self.index == 1:
            self.start_the_car()
            self.index = 0
        else:
            self.move(self.dest_x, self.dest_y)
            sys.exit()
