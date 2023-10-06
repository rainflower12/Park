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
        self.flag = 1
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
        if (self.map.layout.iloc[self.dest_x, self.dest_x] == 1):
            self.temp_dest_x, self.temp_dest_y = self.map.get_closest_road(self.dest_x, self.dest_y)
        else:
            self.temp_dest_x, self.temp_dest_y = self.dest_x, self.dest_y
        return (self.temp_dest_x, self.temp_dest_y)

    def drive(self):
        """
        Move the car
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
        Show the position of the car
        """
        # print(f"({self.x}, {self.y})", end=" ", flush=True)
        self.pass_road.append((self.x, self.y))

    def stop_the_car(self):
        with self.lock:
            print(str(threading.get_ident()) + " Destination reached!")
            print("The car pass the road is:", end=" ")
            print(self.pass_road)
            while True:
                time.sleep(100)

    def start_the_car(self):
        self.flag = 1

    def check_dest_position(self):
        """
        Check if the car has reached the destination
        Return:
            bool: if the car has reached the destination
        """
        return (self.x, self.y) == (self.dest_x, self.dest_y)

    def placeHolder_parking(self, parking_x, parking_y):
        """
        Check if the car has reached the destination
        Return:
            bool: if the car has reached the destination
        """
        if (self.map.layout.iloc[parking_x + 1, parking_y] == 1):
            pass

    def drive_to_parking(self):
        while self.x != self.dest_x or self.y != self.dest_y:
            if self.dest_x < self.x:
                self.direction = 1
            elif self.dest_x > self.x:
                self.direction = 2
            elif self.dest_y < self.y:
                self.direction = 3
            elif self.dest_y > self.y:
                self.direction = 4
            result = self.check_collision()
            if result[0] is False:
                self.pre_x = self.x
                self.pre_y = self.y
                self.drive()
                self.add_position()
                break
            else:
                self.solve_collision(result[1])   # 如果解决 下次检测就不会冲突
                self.drive_to_temp_dest()

    def drive_to_temp_dest(self):
        while self.x != self.temp_dest_x or self.y != self.temp_dest_y:
            # print(self.x, self.y)
            # print(self.temp_dest_x, self.temp_dest_y)
            self.map.assign_car_direction(self, self.temp_dest_x, self.temp_dest_y)
            result = self.check_collision()
            # if (self.index == 2):
            #     print(result)
            if result[0] is False:
                self.pre_x = self.x
                self.pre_y = self.y
                self.drive()
                self.add_position()
            else:
                self.solve_collision(result[1])   # 如果解决 下次检测就不会冲突

    def drive_out_parking(self):
        pass

    def manage_move(self, dest_x, dest_y):
        """
        Manage the car move to the position
        """
        self.start_the_car()  # 车辆启动
        self.get_dest(dest_x, dest_y)
        self.get_temp_dest(dest_x, dest_y)
        self.drive_to_temp_dest()
        self.drive_to_parking()
        self.stop_the_car()

    def check_collision(self) -> tuple:
        """
        Check if there is a collision
        Returns:
            tuple: conflict(bool) and conflicting vehicles(car)
        """
        # if ahead self direction have a car , then solve the collision
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
                return (True, car)
        return (False, None)

    def solve_collision(self, car):
        """
        Try to solve the collision
        Args:
            car : the car to overtake
        Returns:
            bool: solve successful or not
        """
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
            # print(self.pass_road)
            result = self.map.get_closest_parking(car_x, car_y)
            self.get_dest(result[0], result[1])
            self.get_temp_dest(self.dest_x, self.dest_y)
            # print(self.dest_x, self.dest_y)
            return True

    def set_temp_parking(self, parking_x, parking_y):
        """
        Set the temporary parking position
        """
        self.x = parking_x
        self.y = parking_y
        self.flag = 0
        print(str(threading.get_ident()) + " Temporary parking ok!")
        # print(self.x, self.y)
        while True:
            time.sleep(100)

    def run(self):
        if (self.index == 1):
            self.set_temp_parking(4, 15)
        else:
            self.manage_move(self.dest_x, self.dest_y)
            sys.exit()
