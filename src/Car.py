from Map import Map
import threading
import time


class Car(threading.Thread):
    def __init__(self, x, y, map: Map, pre_x=0, pre_y=0, direction=0, pre_direction=0):
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

    def show_position(self):
        """
        Show the position of the car
        """
        # Print position and wrap every 10 times when printing
        print(f"({self.x}, {self.y})", end=" ", flush=True)

    def move(self, dest_x, dest_y):
        """
        Move the car and show the position
        """
        if self.flag == 1:
            # 目的地是停车场
            if (self.map.layout.iloc[dest_x, dest_y] == 1):
                temp_dest_x, temp_dest_y = self.map.get_closest_road(dest_x, dest_y)
            else:
                temp_dest_x, temp_dest_y = dest_x, dest_y
            while self.x != temp_dest_x or self.y != temp_dest_y:
                self.map.navigate_car_to_dest(self, temp_dest_x, temp_dest_y)
                while True:
                    if self.check_collision() is False:
                        self.drive()
                        self.show_position()
                        break
                    time.sleep(10)
            if (temp_dest_x, temp_dest_y) == (dest_x, dest_y):
                print()
                print("Destination reached!")
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
                        print(dest)
                        print()
                        print("Parking reached!")
                        break
                    time.sleep(10)
        else:
            print("car stop")
            return

    def check_collision(self) -> bool:
        """
        Check if there is a collision
        Returns:
            bool: whether to stop
        """
        # if ahead self direction have a car , then stop
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
            if car != self:
                if (car.x, car.y) == (self.ahead_x, self.ahead_y) and car.flag == 1:
                    print("stop")
                    return True
                if ((car.x, car.y) == (self.ahead_x, self.ahead_y) and car.flag == 0):
                    self.try_overtake(car.x, car.y)
                    return False
        return False

    def try_overtake(self, car_x, car_y):
        """
        Try to overtake
        """
        if self.direction == 1:
            i = 1
            while (i < 5):
                has_car = 0
                target_x = car_x - i
                target_y = car_y
                across_x = self.x
                across_y = self.y
                for car in self.map.cars:
                    if (car.x, car.y) == (target_x, target_y):
                        i += 1
                        has_car = 1
                        break
                if (has_car):
                    continue
                across_y -= 1
                for car in self.map.cars:
                    for j in range(i + 2):
                        if (car.x, car.y) == (across_x - j, across_y):
                            has_car = 1
                            break
                if (has_car):
                    continue
                for j in range(i + 2):
                    print(across_x - j, across_y)
                print(across_x - i - 1, across_y + 1)
                self.x = across_x - i - 1
                self.y = across_y + 1
                print("overtake")
        elif self.direction == 2:
            i = 1
            while (i < 5):
                has_car = 0
                target_x = car_x + i
                target_y = car_y
                across_x = self.x
                across_y = self.y
                for car in self.map.cars:
                    if (car.x, car.y) == (target_x, target_y):
                        i += 1
                        has_car = 1
                        break
                if (has_car):
                    continue
                across_y += 1
                for car in self.map.cars:
                    for j in range(i + 2):
                        if (car.x, car.y) == (across_x + j, across_y):
                            has_car = 1
                            break
                if (has_car):
                    continue
                for j in range(i + 2):
                    print(across_x + j, across_y)
                print(across_x + i + 1, across_y - 1)
                self.x = across_x + i + 1
                self.y = across_y - 1
                print("overtake")
        elif self.direction == 3:
            i = 1
            while (i < 5):
                has_car = 0
                target_x = car_x
                target_y = car_y - i
                across_x = self.x
                across_y = self.y
                for car in self.map.cars:
                    if (car.x, car.y) == (target_x, target_y):
                        i += 1
                        has_car = 1
                        break
                if (has_car):
                    continue
                across_x += 1
                for car in self.map.cars:
                    for j in range(i + 2):
                        if (car.x, car.y) == (across_x, across_y - j):
                            has_car = 1
                            break
                if (has_car):
                    continue
                for j in range(i + 2):
                    print(across_x, across_y - j)
                print(across_x - 1, across_y - i - 1)
                self.x = across_x - 1
                self.y = across_y - i - 1
                print("overtake")
        elif self.direction == 4:
            i = 1
            while (i < 5):
                has_car = 0
                target_x = car_x
                target_y = car_y + i
                across_x = self.x
                across_y = self.y
                for car in self.map.cars:
                    if (car.x, car.y) == (target_x, target_y):
                        i += 1
                        has_car = 1
                        break
                if (has_car):
                    continue
                across_x -= 1
                for car in self.map.cars:
                    for j in range(i + 2):
                        if (car.x, car.y) == (across_x, across_y + j):
                            has_car = 1
                            break
                if (has_car):
                    continue
                for j in range(i + 2):
                    print(across_x, across_y + j)
                print(across_x + 1, across_y + i + 1)
                self.x = across_x + 1
                self.y = across_y + i + 1
                print("overtake")

    def stop(self):
        self.flag = 0

    def start(self):
        self.flag = 1

    def run(self):
        self.move(self.dest_x, self.dest_y)
