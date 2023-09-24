from Car import Car
from Map import Map
import os

module_dir = os.path.dirname(__file__)
relative_path_to_layout = os.path.join('..', 'resources', 'layout.csv')
layout_path = os.path.abspath(os.path.join(module_dir, relative_path_to_layout))

map = Map(layout_path)

car_x = int(input("请输入车辆的行坐标："))
car_y = int(input("请输入车辆的列坐标："))
car_pre_x = int(input("请输入车辆的上一秒所在行坐标："))
car_pre_y = int(input("请输入车辆的上一秒所在列坐标："))
car = Car(car_x, car_y, car_pre_x, car_pre_y, 0, 2)  # 创建车辆对象，初始标志为 0
dest_x = int(input("请输入目的地的行坐标："))
dest_y = int(input("请输入目的地的列坐标："))

map.navigate_car_to_dest(car, dest_x, dest_y)
