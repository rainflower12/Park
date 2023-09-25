class Car:
    def __init__(self, x, y, pre_x=0, pre_y=0, direction=0, pre_direction=0):
        """
        Initialize the car object
        Args:
            param x: x coordinate
            param y: y coordinate
            param pre_x: previous x coordinate
            param pre_y: previous y coordinate
            param direction: direction of the car
            param pre_direction: previous direction of the car
        """
        self.x = x
        self.y = y
        self.pre_x = pre_x  # 初始化上一步坐标为当前坐标
        self.pre_y = pre_y
        self.direction = direction
        self.pre_direction = pre_direction

    def move(self):
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
