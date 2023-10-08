import pandas as pd


class Map:
    def __init__(self, layout_path):
        self.layout_path = layout_path
        self.layout = pd.read_csv(self.layout_path, header=None)
        self.wide = None
        self.height = None
        self.roadrow = None
        self.roadcolumn = None
        self.cross = None
        self.leftrow = None
        self.rightrow = None
        self.downcolumn = None
        self.upcolumn = None
        self.cars = []
        if (self.wide is None) or (self.height is None):
            self.get_parking_space_wide_height()
        if (self.cross is None) or \
            (self.roadrow is None) or \
            (self.roadcolumn is None) or \
            (self.leftrow is None) or \
            (self.rightrow is None) or \
            (self.downcolumn is None) or \
                (self.upcolumn is None):
            self.identify_road_and_cross()

    def check_car(self, x, y):
        """
        Check if there is a car at (x,y)
        Args:
            x : x coordinate
            y : y coordinate
        Returns:
            bool: True if there is a car at (x,y)
        """
        for car in self.cars:
            if (car.x == x) and (car.y == y):
                return True
        return False

    def get_road_direction(self, x, y) -> int:
        """
        Get the road (x,y) direction
        Args:
            x : x coordinate
            y : y coordinate
        Returns:
            int: road direction
        """
        if y in self.upcolumn:
            return 1
        elif y in self.downcolumn:
            return 2
        elif x in self.leftrow:
            return 3
        elif x in self.rightrow:
            return 4

    def get_parking_space_wide_height(self) -> tuple:
        """
        Get the wide and height of a parking space
        Returns:
            tuple: the wide and height of a parking space
        """
        for i in range(len(self.layout)):
            for j in range(len(self.layout.iloc[i])):
                if self.layout.iloc[i, j] == 1:
                    start_row, start_col = i, j
                    break
            if "start_row" in locals():
                break
        self.wide, self.height = 0, 0
        for i in range(start_row, len(self.layout)):
            if all(self.layout.iloc[i, start_col:start_col + self.wide + 1] == 1):
                self.height += 1
            else:
                break
        for j in range(start_col, len(self.layout.iloc[start_row])):
            if self.layout.iloc[start_row, j] == 1:
                self.wide += 1
            else:
                break
        return (self.wide, self.height)

    def identify_road_and_cross(self) -> tuple:
        """
        Extract the layout of the road network
        Returns:
            tuple: the message of the layout of the road network
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

    def get_closest_road(self, dest_x, dest_y) -> tuple:
        """
        Get the closest road to the parking lot
        Args:
            dest_x : destination x coordinate
            dest_y : destination y coordinate
        Returns:
            tuple: the road (x,y) to the parking lot (dest_x,dest_y)
        """
        i = 1
        while True:
            if self.layout.iloc[dest_x, dest_y] == 0:
                return (dest_x, dest_y)
            elif self.layout.iloc[dest_x - i, dest_y] == 0:
                return (dest_x - i, dest_y)
            elif self.layout.iloc[dest_x + i, dest_y] == 0:
                return (dest_x + i, dest_y)
            i += 1
        # just up or down

    def get_closest_parking(self, target_x, target_y, find_direction) -> tuple:
        """
        Get the closest parking to the target
            x : target x coordinate
            y : target y coordinate
            find_direction: find closest parking direction
        Returns:
            tuple: the parking (x,y) to the target (target_x,target_y)
            when no parking return (-9,-9)
        """
        i = 1
        while True:
            if (target_y - i < 0 or target_y + i >= len(self.layout.columns)):
                return (-9,-9)
            if (i > 10):
                return (-9,-9)
            if (find_direction == 3):
                if self.layout.iloc[target_x, target_y - i] == 1:
                    return (target_x, target_y - i)
            if (find_direction == 4):
                if self.layout.iloc[target_x, target_y + i] == 1:
                    return (target_x, target_y + i)
            i += 1
        # 3: left, 4: right
        # according to the find_direction to find a parking
        # find limit is 10 only y±i 
        # eixt when find a parking or limit or out of range
        # when parking has a car and position == -1
        # when road position == 0
        # when parking position == 1
        # when no parking return (-9,-9)

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
        x = car.x
        y = car.y
        pre_x = car.pre_x
        pre_y = car.pre_y
        car.direction = 0  # 之前没有置0
        # 这里h是每一个停车区域块的高度，w是其宽度，为防止绕一圈（绕路）的情况
        if pre_y in self.upcolumn:  # 是否在上行列，这边在上行列，就没有给他分配往下行列走的可能，所以不会掉头
            if dest_x < x-self.height:  # 保证上行的时候可以一直上行一个停车场区域高度以上
                if x - 2 >= 0:  # 防止这是停车场最上面那个路口，向上会走出停车场
                    car.direction = 1  # 如果已经在上行列，直接向上
                    car.pre_direction = 1
            # 检查 y 方向
            elif dest_y > y:  # 判断出来往右走，然后就在周围寻找x在右行道里面的格子，即x-1,x+1
                if y + 2 < len(self.layout.columns):  # 防止这是停车场最右面那个路口，向右会走出停车场
                    if x in self.rightrow:
                        car.direction = 4  # 如果已经在右行行，直接向右移动
                        car.pre_direction = 4
                        return
                    elif x - 1 in self.rightrow:
                        car.direction = 1
                        car.pre_direction = 4
                        print("2")
                    elif x + 1 in self.rightrow:
                        car.direction = 2
                        car.pre_direction = 4
            elif dest_y < y:  # 同理
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
        elif pre_y in self.downcolumn:  # 同理
            if dest_x > x + self.height:
                if x + 2 < len(self.layout):
                    car.direction = 2  # 如果已经在下行列，直接向下移动
                    car.pre_direction = 2
            # 检查 y 方向
            elif dest_y > y:
                if y + 2 < len(self.layout):
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
            if dest_y > y+self.wide:  # 如果已经在右行行，则判断往右行能不能向右一直走一个区域，和上面一样，是防止绕路的
                if y + 2 < len(self.layout):
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
            if dest_y < y - self.wide:
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
        if car.direction == 0:  # （以车辆在上行道为例）因为上面判断已经在上行道，想要往上走就必须要走一个区域那么长，
            # 如果车的y右恰巧等于目的地的y，经过上面的函数，车辆仍有可能没有direction,此刻不需要左右转，那我们此时可以直接让车辆上行
            if y in self.upcolumn:
                if dest_x < x:
                    if x - 2 >= 0:
                        car.direction = 1  # 如果已经在上行列，直接向上
                        car.pre_direction = 1
            elif y in self.downcolumn:
                if dest_x > x:
                    if x + 2 < len(self.layout):
                        car.direction = 2  # 如果已经在下行列，直接向下移动
                        car.pre_direction = 2
            elif x in self.rightrow:
                if dest_y > y:
                    if y + 2 < len(self.layout.columns):
                        car.direction = 4  # 如果已经在下行列，直接向下移动
                        car.pre_direction = 4
            elif x in self.leftrow:
                if dest_y < y:
                    if y - 2 > -1:
                        car.direction = 3  # 如果已经在下行列，直接向下移动
                        car.pre_direction = 3
        if car.direction == 0:  # 经过上述操作，仍然没有direction，那就只要保证不出停车场范围，随便走
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
