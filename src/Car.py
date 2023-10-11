from map import Map
import threading
import time
import sys


class Car(threading.Thread):
    def __init__(self, x, y, map: Map, pre_x, pre_y, stage=1, direction=0, pre_direction=0):
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
        self.flag = 0
        self.pass_road = []
        self.index = 0  # 车辆编号
        self.stage = stage  # 车辆运行阶段
        Car.lock = threading.Lock()

    def get_dest(self, dest_x, dest_y) -> tuple:
        """
        Assign the dest
        Args:
            dest_x : destination x coordinate
            dest_y : destination y coordinate
        Returns:
            tuple: destination x and y coordinate
        """
        self.dest_x = dest_x
        self.dest_y = dest_y
        return (self.dest_x, self.dest_y)

    def get_temp_dest(self, dest_x, dest_y) -> tuple:
        """
        Assign the temporary dest
        Args:
            dest_x : destination x coordinate
            dest_y : destination y coordinate
        Returns:
                tuple: destination x and y coordinate
        """
        if (self.map.layout.iloc[self.dest_x, self.dest_y] == 1):
            self.temp_dest_x, self.temp_dest_y = self.map.get_closest_road(self.dest_x, self.dest_y)
        else:
            self.temp_dest_x, self.temp_dest_y = self.dest_x, self.dest_y
        return (self.temp_dest_x, self.temp_dest_y)

    def drive(self):
        """
        Move the car and change the position
        """
        if self.direction == 1:  # Move up
            self.x -= 1
        elif self.direction == 2:  # Move down
            self.x += 1
        elif self.direction == 3:  # Move left
            self.y -= 1
        elif self.direction == 4:  # Move right
            self.y += 1
        else:
            print(self.direction)
            print("Invalid direction value. The car will stay in its current position.")

    def add_position(self):
        """
        Add the position of the car to the postion list
        """
        self.pass_road.append((self.x, self.y))

    def stop_the_car(self):
        """
        Stop the car and print the pass road
        """
        with self.lock:
            print(str(threading.get_ident()) + " Destination reached!")
            print("The car pass the road is:", end=" ")
            print(self.pass_road)
            # while True:
            time.sleep(5)

    def start_the_car(self):
        """
        Before the car start to do some work
        Move out the parking
        Move in the road
        """
        if self.map.layout.iloc[self.x, self.y] == -1:
            x, y = self.map.get_closest_road(self.x, self.y)
            if x < self.x:
                self.direction = 1
            elif x > self.x:
                self.direction = 2
            elif y < self.y:
                self.direction = 3
            elif y > self.y:
                self.direction = 4
            while self.x != x or self.y != y:
                result = self.check_conflict()
                if result[0] is False:
                    self.pre_x = self.x
                    self.pre_y = self.y
                    self.drive()
                    if (self.map.layout.iloc[self.pre_x - 1, self.pre_y] == -1):
                        self.map.layout.iloc[self.pre_x - 1, self.pre_y] = 1
                    if (self.map.layout.iloc[self.pre_x + 1, self.pre_y] == -1):
                        self.map.layout.iloc[self.pre_x + 1, self.pre_y] = 1
                    if (self.map.layout.iloc[self.pre_x, self.pre_y] == -1):
                        self.map.layout.iloc[self.pre_x, self.pre_y] == 1
                    self.add_position()
                else:
                    self.solve_conflict(result[1])   # 如果解决 下次检测就不会冲突
            self.flag = 1
        else:
            self.flag = 1

    def check_dest_position(self):
        """
        Check if the car has reached the destination
        Return:
            bool: if the car has reached the destination
        """
        return (self.x, self.y) == (self.dest_x, self.dest_y)

    def set_parking(self):
        """
        Set the car parking position
        """
        self.map.layout.iloc[self.x, self.y] = -1
        if (self.map.layout.iloc[self.x + 1, self.y] == 1):
            self.map.layout.iloc[self.x + 1, self.y] = -1
        if (self.map.layout.iloc[self.x - 1, self.y] == 1):
            self.map.layout.iloc[self.x - 1, self.y] = -1

    def drive_to_parking(self):
        """
        When car is next to 1 to the parking_dest, then drive to the parking_dest
        """
        while self.x != self.dest_x or self.y != self.dest_y:
            if self.dest_x < self.x:
                self.direction = 1
            elif self.dest_x > self.x:
                self.direction = 2
            elif self.dest_y < self.y:
                self.direction = 3
            elif self.dest_y > self.y:
                self.direction = 4
            result = self.check_conflict()
            if result[0] is False:
                self.pre_x = self.x
                self.pre_y = self.y
                self.drive()
                self.add_position()
                self.set_parking()
            else:
                self.solve_conflict(result[1])   # 如果解决 下次检测就不会冲突
                self.drive_to_temp_dest()

    def drive_to_temp_dest(self):
        """
        The car drive to the temp dest
        """
        while self.x != self.temp_dest_x or self.y != self.temp_dest_y:
            if self.check_special_case() is False:
                # print(self.x, self.y)
                # print(self.direction)
                # time.sleep(10)
                # 如果满足驶入条件
                self.pre_x = self.x
                self.pre_y = self.y
                self.drive()
                self.add_position()
            else:
                self.map.assign_car_direction(self, self.temp_dest_x, self.temp_dest_y)
                result = self.check_conflict()
                if result[0] is False:
                    self.pre_x = self.x
                    self.pre_y = self.y
                    self.drive()
                    self.add_position()
                else:
                    self.solve_conflict(result[1])   # 如果解决 下次检测就不会冲突

    def manage_move(self, dest_x, dest_y):
        """
        Manage the car move to the position
        Args:
            dest_x : destination x coordinate
            dest_y : destination y coordinate
        """
        self.start_the_car()  # 车辆启动
        self.get_dest(dest_x, dest_y)
        self.get_temp_dest(dest_x, dest_y)
        self.drive_to_temp_dest()
        self.drive_to_parking()
        self.stop_the_car()

    def check_special_case(self) -> bool:
        """
        Check whether satisfy entering the parking space in the opposite lane
        If satisfy direction will change
        Returns:
            bool: has_conflict -> True, no_conflict -> False
        """
        # Entering the parking space in the opposite lane conflict
        has_conflict = True
        if self.direction == 3 and self.x + 1 == self.temp_dest_x and self.y == self.dest_y and \
                self.map.layout.iloc[self.dest_x, self.dest_y] == 1:  # 车辆左行时，停车位在temp下方1格时，触发检测函数
            if self.map.check_car(self.x + 1, self.y - 1):
                has_conflict = True
            else:
                has_conflict = False
                self.direction = 2
        if self.direction == 4 and self.x - 1 == self.temp_dest_x and self.y == self.dest_y and \
                self.map.layout.iloc[self.dest_x, self.dest_y] == 1:
            # 车辆右行时，停车位在temp上方1格时，触发检测函数
            if self.map.check_car(self.x - 1, self.y + 1):
                # 是否有车辆再上一格临时停车
                has_conflict = True
            else:
                has_conflict = False
                self.direction = 1
        return has_conflict

    def check_conflict(self) -> tuple:
        """
        Check if there is a conflict
        Returns:
            tuple: conflict(bool) and conflicting vehicles(car)
        """
        # if ahead self direction have a car , then solve the conflict
        have_conflict = False
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
        for car in self.map.cars:
            if (car.x, car.y) == (self.ahead_x, self.ahead_y) and car != self:
                have_conflict = True
                if (self.map.layout.iloc[self.x, self.y] == -1):
                    return (have_conflict, None)  # 逻辑有漏洞 其实应该是自己在停车场然后也返回检测到车辆,然后根据自身在停车场然后判断解决
                else:
                    return (have_conflict, car)  # just here return the car
        # intersection detection
        if self.direction == 3:  # 左行过路口时，第一次检测下方是否有来车，如果还要左行，则检测上方是否有来车。
            if self.map.layout.iloc[self.x][self.y - 1] in self.map.upcolumn:
                if (self.map.check_car(self.x + 1, self.y - 1)):
                    have_conflict = True
                else:
                    have_conflict = False
            if self.map.layout.iloc[self.x][self.y - 1] in self.map.downcolumn:
                if (self.map.check_car(self.x - 1, self.y - 1)):
                    have_conflict = True
                else:
                    have_conflict = False
        if self.direction == 4:  # 右行过路口时，第一次检测上方是否有来车，如果还要右行，则检测下方是否有来车。
            if self.map.layout.iloc[self.x][self.y + 1] in self.map.upcolumn:
                if self.map.chech_car(self.x + 1, self.y + 1):
                    have_conflict = True
                else:
                    have_conflict = False
            if self.map.layout.iloc[self.x][self.y + 1] in self.map.downcolumn:
                if self.map.check_car(self.x - 1, self.y + 1):
                    have_conflict = True
                else:
                    have_conflict = False
        # Exit parking space detection
        if self.map.layout.iloc[self.x, self.y] == -1 and self.map.layout.iloc[self.x - 1, self.y] == -1:
            if self.map.check_car(self.x + 1, self.y) or self.map.check_car(self.x + 1, self.y + 1):
                have_conflict = True
            else:
                have_conflict = False
                self.direction = 2
        if self.map.layout.iloc[self.x, self.y] == -1 and self.map.layout.iloc[self.x + 1, self.y] == -1:
            if self.map.check_car(self.x - 1, self.y) or self.map.check_car(self.x - 1, self.y - 1):
                have_conflict = True
            else:
                have_conflict = False
                self.direction = 1
        return (have_conflict, None)

    def solve_conflict(self, car) -> bool:
        """
        Try to solve the conflict
        Args:
            car : the car to overtake
        Returns:
            bool: solve successful or not
        """
        if car is None:
            with self.lock:
                time.sleep(2)
                print(self.pass_road)
                print("no way to drive")
            return False
        else:
            car_x = car.x
            car_y = car.y
            car_flag = car.flag
            # print(car_x, car_y, car_flag)
            if car_flag == 0 and self.map.layout.iloc[car_x, car_y] == 0:
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
                    self.x = across_x
                    self.y = across_y
                    temp = (self.x, self.y)
                    self.pass_road.append(temp)
                    self.x = target_x
                    self.y = target_y
                    temp = (self.x, self.y)
                    self.pass_road.append(temp)
                    return True
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
                    self.x = across_x
                    self.y = across_y
                    temp = (self.x, self.y)
                    self.pass_road.append(temp)
                    self.x = target_x
                    self.y = target_y
                    temp = (self.x, self.y)
                    self.pass_road.append(temp)
                    return True
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
                    self.x = across_x
                    self.y = across_y
                    temp = (self.x, self.y)
                    self.pass_road.append(temp)
                    self.x = target_x
                    self.y = target_y
                    temp = (self.x, self.y)
                    self.pass_road.append(temp)
                    return True
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
                    self.x = across_x
                    self.y = across_y
                    temp = (self.x, self.y)
                    self.pass_road.append(temp)
                    self.x = target_x
                    self.y = target_y
                    temp = (self.x, self.y)
                    self.pass_road.append(temp)
                    return True
            elif car_flag == 1 and self.map.layout.iloc[car_x, car_y] == 0:
                return False
            else:
                find_direction = self.map.get_road_direction(self.x, self.y)
                result = self.map.get_closest_parking(car_x, car_y, find_direction)
                if (result[0] == -9):
                    print("no parking")
                    return False
                self.get_dest(result[0], result[1])
                self.get_temp_dest(self.dest_x, self.dest_y)
                return True

    def set_temp_parking(self, parking_x, parking_y, pre_parking_x, pre_parking_y):
        """
        Set the temporary parking position
        Args:
            parking_x : parking x coordinate
            parking_y : parking y coordinate
        """
        self.x = parking_x
        self.y = parking_y
        self.pre_x = pre_parking_x
        self.pre_y = pre_parking_y
        self.flag = 0
        # print("set ok!")
        # while True:
        #     time.sleep(100)
        print(str(threading.get_ident()) + " Temporary parking ok!")
        while True:
            time.sleep(100)

    def run(self):
        
        # (dest_x, dest_y) = (5, 18)
        
        # stage = 2 just from one parking to another parking
        # self.manage_move(self.dest_x, self.dest_y)
        # self.manage_move(11, 18)

        # stage = 2 and has a temp parking 
        # if self.index == 0:
        #     self.manage_move(self.dest_x, self.dest_y)
        #     self.manage_move(11, 18)
        # elif self.index == 1:
        #     self.set_temp_parking(6, 19, 6, 20)
        
        # if self.index == 0:
            self.manage_move(self.dest_x, self.dest_y)
            # self.manage_move(11, 18)
        # elif self.index == 1:
        #     self.set_temp_parking(7, 13, 7, 12)
        # else:
        #     self.manage_move(5, 18)