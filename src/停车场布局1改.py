import pandas as pd
import os

# 获取当前模块所在的目录
module_dir = os.path.dirname(__file__)

# 构建相对路径到资源文件
relative_path_to_layout = os.path.join('..', 'resources', 'layout.csv')

# 获取资源文件的绝对路径
layout_path = os.path.abspath(os.path.join(module_dir, relative_path_to_layout))

# 读取CSV文件
df = pd.read_csv(layout_path)
for i in range(len(df)):
    for j in range(len(df.iloc[i])):
        if df.iloc[i, j] == 1:
            start_row, start_col = i, j
            break
    if "start_row" in locals():
        break

# 接下来，找到方块的长和宽
w, h = 0, 0
for i in range(start_row, len(df)):
    if all(df.iloc[i, start_col:start_col + w + 1] == 1):
        h += 1
    else:
        break

for j in range(start_col, len(df.iloc[start_row])):
    if df.iloc[start_row, j] == 1:
        w += 1
    else:
        break
# 打印长和宽
print("一块停车位的长:", w)
print("一块停车位的宽:", h)


class Car:
    def __init__(self, x, y, pre_x, pre_y, flag, pre_flag):
        self.x = x
        self.y = y
        self.pre_x = pre_x  # 初始化上一步坐标为当前坐标
        self.pre_y = pre_y
        self.flag = flag
        self.pre_flag = pre_flag

    def move(self):
        if self.flag == 1:  # Move up
            self.pre_x = self.x
            self.pre_y = self.y
            self.x -= 1
        elif self.flag == 2:  # Move down
            self.pre_x = self.x
            self.pre_y = self.y
            self.x += 1
        elif self.flag == 3:  # Move left
            self.pre_x = self.x
            self.pre_y = self.y
            self.y -= 1
        elif self.flag == 4:  # Move right
            self.pre_x = self.x
            self.pre_y = self.y
            self.y += 1
        else:
            print(car.flag)
            print("Invalid flag value. The car will stay in its current position.")


def identify_road_and_cross(file_path):
    # 读取csv文件
    df = pd.read_csv(file_path, header=None)

    # 初始化存储“道路行”和“道路列”的数组
    roadrow = []
    roadcolumn = []

    # 找到“道路行”
    for index, row in df.iterrows():
        if 1 not in row.tolist():
            roadrow.append(index)

    # 找到“道路列”
    for col in df.columns:
        if 1 not in df[col].tolist():
            roadcolumn.append(col)

    # 初始化存储“交叉路口”的数组
    cross = []

    # 设置交叉路口
    for row in roadrow:
        for col in roadcolumn:
            cross.append((row, col))

    # 初始化存储“左行行”和“右行行”的数组
    leftrow = []
    rightrow = []

    # 找到“左行行”和“右行行”
    for row in roadrow:
        if row - 1 in roadrow:
            leftrow.append(row - 1)
        if row + 1 in roadrow:
            rightrow.append(row + 1)

    # 初始化存储“下行列”和“上行列”的数组
    downcolumn = []
    upcolumn = []

    # 找到“下行列”和“上行列”
    for col in roadcolumn:
        if col - 1 in roadcolumn:
            downcolumn.append(col - 1)
        if col + 1 in roadcolumn:
            upcolumn.append(col + 1)

    return roadrow, roadcolumn, cross, leftrow, rightrow, downcolumn, upcolumn


def assign_car_flag(car, dest_x, dest_y, file_path, cross, leftrow, rightrow, downcolumn, upcolumn):
    df = pd.read_csv(file_path, header=None)
    x = car.x
    y = car.y
    pre_x = car.pre_x
    pre_y = car.pre_y

    if df.iloc[x, y] != 0:
        print("车辆在停车位内")
    else:
        if (x, y) in cross:
            # if (pre_x,pre_y) in cross:
            # car.flag=car.pre_flag
            # print("cuo10")
            # else:
            crossflag(car, file_path, dest_x, dest_y, leftrow, rightrow, upcolumn, downcolumn)  # Set flag for cross
        elif x in leftrow:
            car.flag = 3  # Move left
            car.pre_flag = 0
        elif x in rightrow:
            car.flag = 4  # Move right
            car.pre_flag = 0
        elif y in downcolumn:
            car.flag = 2  # Move down
            car.pre_flag = 0
        elif y in upcolumn:
            car.flag = 1  # Move up
            car.pre_flag = 0
        else:
            print("无法为车辆分配有效标志")


def crossflag(car, file_path, dest_x, dest_y, leftrow, rightrow, upcolumn, downcolumn):
    df = pd.read_csv(file_path, header=None)
    x = car.x
    y = car.y
    pre_x = car.pre_x
    pre_y = car.pre_y
    if pre_y in upcolumn:
        if dest_x < x - h:
            if x - 2 >= 0:
                car.flag = 1  # 如果已经在上行列，直接向上
                car.pre_flag = 1
        # 检查 y 方向
        elif dest_y > y:
            if y + 2 < len(df.columns):
                if x in rightrow:
                    car.flag = 4  # 如果已经在右行行，直接向右移动
                    car.pre_flag = 4
                    return
                elif x - 1 in rightrow:
                    car.flag = 1
                    car.pre_flag = 4
                elif x + 1 in rightrow:
                    car.flag = 2
                    car.pre_flag = 4
        elif dest_y < y:
            if y - 2 >= 0:
                if x in leftrow:
                    car.flag = 3  # 如果已经在左行行，直接向左移动
                    car.pre_flag = 3
                    return
                if x - 1 in leftrow:
                    car.flag = 1
                    car.pre_flag = 3
                elif x + 1 in leftrow:
                    car.flag = 2
                    car.pre_flag = 3
    elif pre_y in downcolumn:
        if dest_x > x + h:
            if x + 2 < len(df):
                car.flag = 2  # 如果已经在下行列，直接向下移动
                car.pre_flag = 2
        # 检查 y 方向
        elif dest_y > y:
            if y + 2 < len(df.columns):
                if x in rightrow:
                    car.flag = 4  # 如果已经在右行行，直接向右移动
                    car.pre_flag = 4
                    return
                if x - 1 in rightrow:
                    car.flag = 1
                    car.pre_flag = 4
                elif x + 1 in rightrow:
                    car.flag = 2
                    car.pre_flag = 4
        elif dest_y < y:
            if y - 2 >= 0:
                if x in leftrow:
                    car.flag = 3  # 如果已经在左行行，直接向左移动
                    car.pre_flag = 3
                    return
                if x - 1 in leftrow:
                    car.flag = 1
                    car.pre_flag = 3
                elif x + 1 in leftrow:
                    car.flag = 2
                    car.pre_flag = 3
    elif pre_x in rightrow:
        if dest_y > y + w:
            if y + 2 < len(df.columns):
                car.flag = 4  # 如果已经在下行列，直接向下移动
                car.pre_flag = 4
        elif dest_x > x:
            if x + 2 < len(df):
                if y in downcolumn:
                    car.flag = 2  # 如果已经在下行列，直接向下移动
                    car.pre_flag = 2
                    return
                elif y - 1 in downcolumn:
                    car.flag = 3
                    car.pre_flag = 2
                elif y + 1 in downcolumn:
                    car.flag = 4
                    car.pre_flag = 2
        elif dest_x <= x - 1:
            if x - 2 >= 0:
                if y in upcolumn:
                    car.flag = 1  # 如果已经在上行列，直接向上移动
                    car.pre_flag = 1
                    return
                elif y - 1 in upcolumn:
                    car.flag = 3
                    car.pre_flag = 1
                elif y + 1 in upcolumn:
                    car.flag = 4
                    car.pre_flag = 1
    elif pre_x in leftrow:
        if dest_y < y - w:
            if y - 2 > -1:
                car.flag = 3  # 如果已经在下行列，直接向下移动
                car.pre_flag = 3

        elif dest_x > x:
            if x + 2 < len(df):
                if y in downcolumn:
                    car.flag = 2  # 如果已经在下行列，直接向下移动
                    car.pre_flag = 2
                    return
                if y - 1 in downcolumn:
                    car.flag = 3
                    car.pre_flag = 2
                elif y + 1 in downcolumn:
                    car.flag = 4
                    car.pre_flag = 2
        elif dest_x < x:  # 改过1改2
            if x - 2 >= 0:
                if y in upcolumn:
                    car.flag = 1  # 如果已经在上行列，直接向上移动
                    car.pre_flag = 1
                    return
                if y - 1 in upcolumn:
                    car.flag = 3
                    car.pre_flag = 1
                elif y + 1 in upcolumn:
                    car.flag = 4
                    car.pre_flag = 1
    print(car.flag)
    if car.flag == 0:
        print("还未有flag1")
        if pre_y in upcolumn:
            if dest_x < x:
                if x - 2 >= 0:
                    car.flag = 1  # 如果已经在上行列，直接向上
                    car.pre_flag = 1
        elif pre_y in downcolumn:
            if dest_x > x:
                if x + 2 < len(df):
                    car.flag = 2  # 如果已经在下行列，直接向下移动
                    car.pre_flag = 2
        elif pre_x in rightrow:
            if dest_y > y:
                if y + 2 < len(df.columns):
                    car.flag = 4  # 如果已经在下行列，直接向下移动
                    car.pre_flag = 4
        if dest_y < y:
            if y - 2 > -1:
                car.flag = 3  # 如果已经在下行列，直接向下移动
                car.pre_flag = 3

    if car.flag == 0:
        print("还未有flag2")
        if x in leftrow or x in rightrow:
            if (x + 2) < len(df):
                if pre_x <= x:
                    if y in downcolumn:
                        car.flag = 2  # 如果已经在下行列，直接向下移动
                        return
                    elif (y - 1) in downcolumn:
                        car.flag = 3
                    elif (y + 1) in downcolumn:
                        car.flag = 4
            elif (x - 2) >= 0:
                if pre_x >= x:
                    if y in upcolumn:
                        car.flag = 1  # 如果已经在上行列，直接向上移动
                        return
                    elif (y - 1) in upcolumn:
                        car.flag = 3
                    elif (y + 1) in upcolumn:
                        car.flag = 4
        if y in upcolumn or y in downcolumn:
            if (y + 2) < len(df.columns):
                if pre_y <= y:
                    if x in rightrow:
                        car.flag = 4  # 如果已经在下行列，直接向下移动
                        return
                    elif (x - 1) in rightrow:
                        car.flag = 1
                    elif (x + 1) in rightrow:
                        car.flag = 2
            elif (y - 2) >= 0:
                if pre_y >= y:
                    if x in leftrow:
                        car.flag = 3  # 如果已经在上行列，直接向上移动
                        return
                    elif (x - 1) in leftrow:
                        car.flag = 1
                    elif (x + 1) in leftrow:
                        car.flag = 2


def move_car(car, dest_x, dest_y, file_path):
    df = pd.read_csv(file_path, header=None)
    counter = 0  # 用于计数已打印的坐标数量
    while car.x != dest_x or car.y != dest_y:
        assign_car_flag(car, dest_x, dest_y, file_path, cross, leftrow, rightrow, downcolumn, upcolumn)
        car.move()
        print(f"({car.x}, {car.y})\t", end="", flush=True)
        # print(f"之前坐标({car.pre_x}, {car.pre_y})\t", end="", flush=True)

        counter += 1
        if counter == 10:
            print()  # 换行
            counter = 0

        if car.x == dest_x and car.y == dest_y:
            print((car.x, car.y))
            print("Destination reached!")
            break
        else:
            if (car.x + 1 == dest_x and car.y == dest_y) or (car.x - 1 == dest_x and car.y == dest_y) or (car.x == dest_x and car.y + 1 == dest_y) or (car.x == dest_x and car.y - 1 == dest_y):
                if (car.y + 1 == dest_y):
                    if (df.iloc[dest_x + 1, dest_y] == 1 or df.iloc[car.x + 1, car.y] == 1):
                        car.flag = 4
                        car.move()
                        print((car.x, car.y))
                        print("Destination reached!")
                        break
                    else:
                        print("Destination is 1next to you!")
                        break
                if (car.y - 1 == dest_y):
                    if (df.iloc[dest_x - 1, dest_y] == 1 or df.iloc[car.x - 1, car.y] == 1):
                        car.flag = 3
                        car.move()
                        print((car.x, car.y))
                        print("Destination reached!")
                        break
                    else:
                        print("Destination is 2next to you!")
                        break
                if (car.x + 1 == dest_x):
                    if (df.iloc[dest_x, dest_y] == 1):
                        car.x = dest_x
                        car.y = dest_y
                        print((car.x, car.y))
                        print("Parking reached!")
                        break
                    elif (car.y in downcolumn):
                        car.flag = 2
                        car.move()
                        print((car.x, car.y))
                        print("Destination reached!")
                        break
                    else:
                        print("Destination is 3next to you!")
                        break
                if (car.x - 1 == dest_x):
                    if (df.iloc[dest_x, dest_y] == 1):
                        car.x = dest_x
                        car.y = dest_y
                        print((car.x, car.y))
                        print("Parking reached!")
                        break
                    elif (car.y in upcolumn):
                        car.flag = 1
                        car.move()
                        print((car.x, car.y))
                        print("Destination reached!")
                        break
                    else:
                        print("Destination is 4next to you!")
                        break
# 调用函数并传入文件路径


roadrow, roadcolumn, cross, leftrow, rightrow, downcolumn, upcolumn = identify_road_and_cross(layout_path)

# 你需要先调用 identify_road_and_cross() 函数获取 roadrow, roadcolumn, cross, leftrow, rightrow, downcolumn, upcolumn 等参数
# 然后创建一个 Car 对象，并根据用户输入的坐标调用 assign_car_flag() 函数来分配标志

car_x = int(input("请输入车辆的行坐标："))
car_y = int(input("请输入车辆的列坐标："))
car_pre_x = int(input("请输入车辆的上一秒所在行坐标："))
car_pre_y = int(input("请输入车辆的上一秒所在列坐标："))
car = Car(car_x, car_y, car_pre_x, car_pre_y, 0, 2)  # 创建车辆对象，初始标志为 0
dest_x = int(input("请输入目的地的行坐标："))
dest_y = int(input("请输入目的地的列坐标："))


# assign_car_flag(car,dest_x, dest_y, layout_path, cross, leftrow, rightrow, downcolumn, upcolumn)
# print("车辆的标志已分配为:", car.flag)
move_car(car, dest_x, dest_y, layout_path)
# 打印结果
print("道路行:", roadrow)
print("道路列:", roadcolumn)
print("交叉路口:", cross)
print("左行行:", leftrow)
print("右行行:", rightrow)
print("下行列:", downcolumn)
print("上行列:", upcolumn)
