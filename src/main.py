from Car import Car
from Map import Map
import os
import threading


def car_thread(car_id, all_map: Map, initial_x, initial_y, destination_x, destination_y, pre_x=0, pre_y=0):
    # 创建车辆对象
    car = Car(initial_x, initial_y, pre_x, pre_y)

    # 在地图上放置车辆
    all_map.place_vehicle(car, initial_x, initial_y)

    # 导航车辆到目的地
    all_map.navigate_car_to_dest(car, destination_x, destination_y)


module_dir = os.path.dirname(__file__)
relative_path_to_layout = os.path.join('..', 'resources', 'layout.csv')
layout_path = os.path.abspath(os.path.join(module_dir, relative_path_to_layout))

map = Map(layout_path)

car_x = 0  # int(input("请输入车辆的行坐标："))
car_y = 0  # int(input("请输入车辆的列坐标："))
car_pre_x = 0  # int(input("请输入车辆的上一秒所在行坐标："))
car_pre_y = 0  # int(input("请输入车辆的上一秒所在列坐标："))
car = Car(car_x, car_y)  # 创建车辆对象，初始标志为 0
dest_x = 6  # int(input("请输入目的地的行坐标："))
dest_y = 16  # int(input("请输入目的地的列坐标："))

map.navigate_car_to_dest(car, dest_x, dest_y)
