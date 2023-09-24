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
            param file_path: path to the layout file
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
        while car.x != dest_x or car.y != dest_y:
            self.assign_car_direction(car, dest_x, dest_y)
            car.move()
            car.show_position()
            if (car.x + 1 == dest_x and car.y == dest_y) or (car.x - 1 == dest_x and car.y == dest_y) or (car.x == dest_x and car.y + 1 == dest_y) or (car.x == dest_x and car.y - 1 == dest_y):
                if (car.y + 1 == dest_y):
                    if (self.layout.iloc[dest_x + 1, dest_y] == 1 or self.layout.iloc[car.x + 1, car.y] == 1):
                        car.direction = 4
                        car.move()
                        print((car.x, car.y))
                        print("Destination reached!")
                        break
                    else:
                        print("Destination is 1next to you!")
                        break
                if (car.y - 1 == dest_y):
                    if (self.layout.iloc[dest_x - 1, dest_y] == 1 or self.layout.iloc[car.x - 1, car.y] == 1):
                        car.direction = 3
                        car.move()
                        print((car.x, car.y))
                        print("Destination reached!")
                        break
                    else:
                        print("Destination is 2next to you!")
                        break
                if (car.x + 1 == dest_x):
                    if (self.layout.iloc[dest_x, dest_y] == 1):
                        car.x = dest_x
                        car.y = dest_y
                        print((car.x, car.y))
                        print("Parking reached!")
                        break
                    elif (car.y in self.downcolumn):
                        car.direction = 2
                        car.move()
                        print((car.x, car.y))
                        print("Destination reached!")
                        break
                    else:
                        print("Destination is 3next to you!")
                        break
                if (car.x - 1 == dest_x):
                    if (self.layout.iloc[dest_x, dest_y] == 1):
                        car.x = dest_x
                        car.y = dest_y
                        print((car.x, car.y))
                        print("Parking reached!")
                        break
                    elif (car.y in self.upcolumn):
                        car.direction = 1
                        car.move()
                        print((car.x, car.y))
                        print("Destination reached!")
                        break
                    else:
                        print("Destination is 4next to you!")
                        break

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

        if self.layout.iloc[x, y] != 0:
            print("车辆在停车位内")
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

    def cross_direction(self, car, dest_x, dest_y):
        """
        Get vehicle driving direction at cross
        Args:
            car : Car object
            file_path : path to the layout file
            dest_x : destination x coordinate
            dest_y : destination y coordinate
        """
        x = car.x
        y = car.y
        pre_x = car.pre_x
        pre_y = car.pre_y
        if pre_y in self.upcolumn:
            if dest_x < x - self.height:
                if x - 2 >= 0:
                    car.direction = 1  # 如果已经在上行列，直接向上
                    car.pre_direction = 1
            # 检查 y 方向
            elif dest_y > y:
                if y + 2 < len(self.layout.columns):
                    if x in self.rightrow:
                        car.direction = 4  # 如果已经在右行行，直接向右移动
                        car.pre_direction = 4
                        return
                    elif x - 1 in self.rightrow:
                        car.direction = 1
                        car.pre_direction = 4
                    elif x + 1 in self.rightrow:
                        car.direction = 2
                        car.pre_direction = 4
            elif dest_y < y:
                if y - 2 >= 0:
                    if x in self.leftrow:
                        car.direction = 3  # 如果已经在左行行，直接向左移动
                        car.pre_direction = 3
                        return
                    if x - 1 in self.leftrow:
                        car.direction = 1
                        car.pre_direction = 3
                    elif x + 1 in self.leftrow:
                        car.direction = 2
                        car.pre_direction = 3
        elif pre_y in self.downcolumn:
            if dest_x > x + self.height:
                if x + 2 < len(self.layout):
                    car.direction = 2  # 如果已经在下行列，直接向下移动
                    car.pre_direction = 2
            # 检查 y 方向
            elif dest_y > y:
                if y + 2 < len(self.layout.columns):
                    if x in self.rightrow:
                        car.direction = 4  # 如果已经在右行行，直接向右移动
                        car.pre_direction = 4
                        return
                    if x - 1 in self.rightrow:
                        car.direction = 1
                        car.pre_direction = 4
                    elif x + 1 in self.rightrow:
                        car.direction = 2
                        car.pre_direction = 4
            elif dest_y < y:
                if y - 2 >= 0:
                    if x in self.leftrow:
                        car.direction = 3  # 如果已经在左行行，直接向左移动
                        car.pre_direction = 3
                        return
                    if x - 1 in self.leftrow:
                        car.direction = 1
                        car.pre_direction = 3
                    elif x + 1 in self.leftrow:
                        car.direction = 2
                        car.pre_direction = 3
        elif pre_x in self.rightrow:
            if dest_y > y + self.weight:
                if y + 2 < len(self.layout.columns):
                    car.direction = 4  # 如果已经在下行列，直接向下移动
                    car.pre_direction = 4
            elif dest_x > x:
                if x + 2 < len(self.layout):
                    if y in self.downcolumn:
                        car.direction = 2  # 如果已经在下行列，直接向下移动
                        car.pre_direction = 2
                        return
                    elif y - 1 in self.downcolumn:
                        car.direction = 3
                        car.pre_direction = 2
                    elif y + 1 in self.downcolumn:
                        car.direction = 4
                        car.pre_direction = 2
            elif dest_x <= x - 1:
                if x - 2 >= 0:
                    if y in self.upcolumn:
                        car.direction = 1  # 如果已经在上行列，直接向上移动
                        car.pre_direction = 1
                        return
                    elif y - 1 in self.upcolumn:
                        car.direction = 3
                        car.pre_direction = 1
                    elif y + 1 in self.upcolumn:
                        car.direction = 4
                        car.pre_direction = 1
        elif pre_x in self.leftrow:
            if dest_y < y - self.weight:
                if y - 2 > -1:
                    car.direction = 3  # 如果已经在下行列，直接向下移动
                    car.pre_direction = 3

            elif dest_x > x:
                if x + 2 < len(self.layout):
                    if y in self.downcolumn:
                        car.direction = 2  # 如果已经在下行列，直接向下移动
                        car.pre_direction = 2
                        return
                    if y - 1 in self.downcolumn:
                        car.direction = 3
                        car.pre_direction = 2
                    elif y + 1 in self.downcolumn:
                        car.direction = 4
                        car.pre_direction = 2
            elif dest_x < x:  # 改过1改2
                if x - 2 >= 0:
                    if y in self.upcolumn:
                        car.direction = 1  # 如果已经在上行列，直接向上移动
                        car.pre_direction = 1
                        return
                    if y - 1 in self.upcolumn:
                        car.direction = 3
                        car.pre_direction = 1
                    elif y + 1 in self.upcolumn:
                        car.direction = 4
                        car.pre_direction = 1
        # print(car.direction)
        if car.direction == 0:
            print("还未有direction1")
            if pre_y in self.upcolumn:
                if dest_x < x:
                    if x - 2 >= 0:
                        car.direction = 1  # 如果已经在上行列，直接向上
                        car.pre_direction = 1
            elif pre_y in self.downcolumn:
                if dest_x > x:
                    if x + 2 < len(self.layout):
                        car.direction = 2  # 如果已经在下行列，直接向下移动
                        car.pre_direction = 2
            elif pre_x in self.rightrow:
                if dest_y > y:
                    if y + 2 < len(self.layout.columns):
                        car.direction = 4  # 如果已经在下行列，直接向下移动
                        car.pre_direction = 4
            if dest_y < y:
                if y - 2 > -1:
                    car.direction = 3  # 如果已经在下行列，直接向下移动
                    car.pre_direction = 3

        if car.direction == 0:
            print("还未有direction2")
            if x in self.leftrow or x in self.rightrow:
                if (x + 2) < len(self.layout):
                    if pre_x <= x:
                        if y in self.downcolumn:
                            car.direction = 2  # 如果已经在下行列，直接向下移动
                            return
                        elif (y - 1) in self.downcolumn:
                            car.direction = 3
                        elif (y + 1) in self.downcolumn:
                            car.direction = 4
                elif (x - 2) >= 0:
                    if pre_x >= x:
                        if y in self.upcolumn:
                            car.direction = 1  # 如果已经在上行列，直接向上移动
                            return
                        elif (y - 1) in self.upcolumn:
                            car.direction = 3
                        elif (y + 1) in self.upcolumn:
                            car.direction = 4
            if y in self.upcolumn or y in self.downcolumn:
                if (y + 2) < len(self.layout.columns):
                    if pre_y <= y:
                        if x in self.rightrow:
                            car.direction = 4  # 如果已经在下行列，直接向下移动
                            return
                        elif (x - 1) in self.rightrow:
                            car.direction = 1
                        elif (x + 1) in self.rightrow:
                            car.direction = 2
                elif (y - 2) >= 0:
                    if pre_y >= y:
                        if x in self.leftrow:
                            car.direction = 3  # 如果已经在上行列，直接向上移动
                            return
                        elif (x - 1) in self.leftrow:
                            car.direction = 1
                        elif (x + 1) in self.leftrow:
                            car.direction = 2
