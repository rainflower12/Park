from Map import Map
import threading


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
        # 我在停车场,我需要驶出
        if (self.map.layout.iloc[self.x, self.y] == 1):
            self.x, self.y = self.map.get_closest_road(self.x, self.y)
            print("out of parking space")
            print()
            print(self.x, self.y)
        # 目的地是停车场
        if (self.map.layout.iloc[dest_x, dest_y] == 1):
            temp_dest_x, temp_dest_y = self.map.get_closest_road(dest_x, dest_y)
        else:
            temp_dest_x, temp_dest_y = dest_x, dest_y
        while self.x != temp_dest_x or self.y != temp_dest_y:
            self.map.navigate_car_to_dest(self, temp_dest_x, temp_dest_y)
            self.drive()
            self.show_position()
        if (temp_dest_x, temp_dest_y) == (dest_x, dest_y):
            print()
            print("Destination reached!")
        else:
            dest = (dest_x, dest_y)
            print(dest)
            print()
            print("Parking reached!")

    def run(self):
        self.move(self.dest_x, self.dest_y)