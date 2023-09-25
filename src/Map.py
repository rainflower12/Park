import pandas as pd


class Map:
    def __init__(self, layout_path):
        self.layout_path = layout_path
        self.layout = pd.read_csv(self.layout_path, header=None)
        self.weight = None
        self.height = None
        self.roadrow = None
        self.roadcolumn = None
        self.cross = None
        self.leftrow = None
        self.rightrow = None
        self.downcolumn = None
        self.upcolumn = None
        self.cars = []

    def get_parking_space_weight_height(self) -> tuple:
        """
        Get the weight and height of a parking space
        """
        for i in range(len(self.layout)):
            for j in range(len(self.layout.iloc[i])):
                if self.layout.iloc[i, j] == 1:
                    start_row, start_col = i, j
                    break
            if "start_row" in locals():
                break
        self.weight, self.height = 0, 0
        for i in range(start_row, len(self.layout)):
            if all(self.layout.iloc[i, start_col:start_col + self.weight + 1] == 1):
                self.height += 1
            else:
                break
        for j in range(start_col, len(self.layout.iloc[start_row])):
            if self.layout.iloc[start_row, j] == 1:
                self.weight += 1
            else:
                break
        return (self.weight, self.height)

    def identify_road_and_cross(self) -> tuple:
        """
        Extract the layout of the road network
        """
        self.roadrow = []
        self.roadcolumn = []
        self.leftrow = []
        self.rightrow = []
        self.downcolumn = []
        self.upcolumn = []
        self.cross = []
        for index, row in self.layout.iterrows():
            if 1 not in row.tolist():
                self.roadrow.append(index)
        for col in self.layout.columns:
            if 1 not in self.layout[col].tolist():
                self.roadcolumn.append(col)
        for row in self.roadrow:
            for col in self.roadcolumn:
                self.cross.append((row, col))
        for row in self.roadrow:
            if row - 1 in self.roadrow:
                self.leftrow.append(row - 1)
            if row + 1 in self.roadrow:
                self.rightrow.append(row + 1)
        for col in self.roadcolumn:
            if col - 1 in self.roadcolumn:
                self.downcolumn.append(col - 1)
            if col + 1 in self.roadcolumn:
                self.upcolumn.append(col + 1)
        return (self.roadrow, self.roadcolumn, self.cross, self.leftrow, self.rightrow, self.downcolumn, self.upcolumn)

    def navigate_car_to_dest(self, car, dest_x, dest_y):
        """
        Navigate to the destination
        Args:
            param car: Car object
            param dest_x: destination x coordinate
            param dest_y: destination y coordinate
        """

        if (self.weight is None) or (self.height is None):
            self.get_parking_space_weight_height()
        if (self.cross is None) or \
            (self.roadrow is None) or \
            (self.roadcolumn is None) or \
            (self.leftrow is None) or \
            (self.rightrow is None) or \
            (self.downcolumn is None) or \
                (self.upcolumn is None):
            self.identify_road_and_cross()

        self.assign_car_direction(car, dest_x, dest_y)

    def assign_car_direction(self, car, dest_x, dest_y):
        """
        Get vehicle driving direction
        Args:
            car : Car object
            dest_x : destination x coordinate
            dest_y : destination y coordinate
        """
        x = car.x
        y = car.y
        # pre_x = car.pre_x
        # pre_y = car.pre_y

        # 不会触发 已经重写停车场内逻辑
        if self.layout.iloc[x, y] != 0:
            print("车辆在停车位内")
            x, y = self.get_closest_road(x, y)
            if x < car.x:
                car.direction = 1
            elif x > car.x:
                car.direction = 2
            elif y < car.y:
                car.direction = 3
            elif y > car.y:
                car.direction = 4
        else:
            if (x, y) in self.cross:
                # if (pre_x,pre_y) in cross:
                # car.direction=car.pre_direction
                # print("cuo10")
                # else:
                self.cross_direction(car, dest_x, dest_y)
            elif x in self.leftrow:
                car.direction = 3  # Move left
                car.pre_direction = 0
            elif x in self.rightrow:
                car.direction = 4  # Move right
                car.pre_direction = 0
            elif y in self.downcolumn:
                car.direction = 2  # Move down
                car.pre_direction = 0
            elif y in self.upcolumn:
                car.direction = 1  # Move up
                car.pre_direction = 0
            else:
                print("无法为车辆分配有效标志")

    def get_distance(self, x, y, dest_x, dest_y) -> int:
        """
        Get the distance between two points
        Args:
            x : x coordinate
            y : y coordinate
            dest_x : destination x coordinate
            dest_y : destination y coordinate
        Returns:
            int: the distance of (x,y) between (dest_x,dest_y)
        """
        return abs(x - dest_x) + abs(y - dest_y)

    def cross_direction(self, car, dest_x, dest_y):
        """
        Get vehicle driving direction at cross
        Args:
            car : Car object
            dest_x : destination x coordinate
            dest_y : destination y coordinate
        """
        # Decide whether to go left or down based on the shortest path between the current location and the target location.
        if car.x in self.leftrow and car.y in self.downcolumn:
            if self.get_distance(car.x, car.y - 1, dest_x, dest_y) <= self.get_distance(car.x + 1, car.y, dest_x, dest_y):
                car.direction = 3  # Move left
            else:
                car.direction = 2  # Move down
        # Decide whether to go left or up based on the shortest path between the current location and the target location.
        if car.x in self.leftrow and car.y in self.upcolumn:
            if self.get_distance(car.x, car.y - 1, dest_x, dest_y) <= self.get_distance(car.x - 1, car.y, dest_x, dest_y):
                car.direction = 3  # Move left
            else:
                car.direction = 1  # Move up
        # Decide whether to go right or down based on the shortest path between the current location and the target location.
        if car.x in self.rightrow and car.y in self.downcolumn:
            if self.get_distance(car.x, car.y + 1, dest_x, dest_y) <= self.get_distance(car.x + 1, car.y, dest_x, dest_y):
                car.direction = 4  # Move right
            else:
                car.direction = 2  # Move down
        # Decide whether to go right or up based on the shortest path between the current location and the target location.
        if car.x in self.rightrow and car.y in self.upcolumn:
            if self.get_distance(car.x, car.y + 1, dest_x, dest_y) <= self.get_distance(car.x - 1, car.y, dest_x, dest_y):
                car.direction = 4  # Move right
            else:
                car.direction = 1  # Move up
        # 优化 最短路算法

    def get_closest_road(self, dest_x, dest_y) -> tuple:
        """
        Get the closest road to the parking lot
        Args:
            dest_x : destination x coordinate
            dest_y : destination y coordinate
        Returns:
            tuple: the closest road (x,y) to the parking lot (dest_x,dest_y)
        """
        i = 1
        while True:
            if self.layout.iloc[dest_x, dest_y] == 0:
                return (dest_x, dest_y)
            elif self.layout.iloc[dest_x - i, dest_y] == 0:
                return (dest_x - i, dest_y)
            elif self.layout.iloc[dest_x + i, dest_y] == 0:
                return (dest_x + i, dest_y)
            elif self.layout.iloc[dest_x, dest_y - i] == 0:
                return (dest_x, dest_y - i)
            elif self.layout.iloc[dest_x, dest_y + i] == 0:
                return (dest_x, dest_y + i)
            i += 1
