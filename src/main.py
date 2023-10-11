from car import Car
from map import Map
import os
import time


def create_map() -> Map:
    module_dir = os.path.dirname(__file__)
    relative_path_to_layout = os.path.join('..', 'resources', 'layout.csv')
    layout_path = os.path.abspath(os.path.join(module_dir, relative_path_to_layout))
    map = Map(layout_path)
    return map


def create_temp_parking(map: Map):
    pre_x = 12
    pre_y = 18
    car_x = 12
    car_y = 17
    car = Car(car_x, car_y, map, pre_x, pre_y)
    # 或许不需要,一上来没启动就是临时停车
    car.set_temp_parking(car_x, car_y, pre_x, pre_y)
    map.cars.append(car)


def single_car_test(map: Map):
    Entrance_x = 0
    Entrance_y = 0
    car_x = 1
    car_y = 0
    car = Car(car_x, car_y, map, Entrance_x, Entrance_y)
    map.cars.append(car)
    dest_x = 11
    dest_y = 16
    car.manage_move(dest_x, dest_y)
    create_temp_parking(map)
    car.manage_move(5, 16)


def mul_car_test(map: Map):
    Entrance_x = 0
    Entrance_y = 0
    car_x = 1
    car_y = 0
    dest_x = 5
    dest_y = 18
    car_threads = []
    for i in range(2):
        car_thread = Car(car_x, car_y, map, Entrance_x, Entrance_y)
        car_thread.index = i
        car_thread.get_dest(dest_x, dest_y)
        car_thread.start()
        car_threads.append(car_thread)
        map.cars.append(car_thread)
        time.sleep(3)
    # wait all thread to finish the task
    for car_thread in car_threads:
        car_thread.join()
    print("All cars have arrived at the destination.")


if __name__ == "__main__":
    map = create_map()
    mul_car_test(map)
