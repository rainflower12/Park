from Car import Car
from Map import Map
import os


def create_map() -> Map:
    module_dir = os.path.dirname(__file__)
    relative_path_to_layout = os.path.join('..', 'resources', 'layout.csv')
    layout_path = os.path.abspath(os.path.join(module_dir, relative_path_to_layout))
    map = Map(layout_path)
    return map


def sigle_car_test(map: Map):
    car_x = 2
    car_y = 16
    car = Car(car_x, car_y, map)
    dest_x = 11
    dest_y = 16
    car.move(dest_x, dest_y)


def mul_car_test(map: Map):
    car_x = 0
    car_y = 0
    dest_x = 5
    dest_y = 16
    car_threads = []
    for i in range(10):
        car_thread = Car(car_x, car_y, map)
        car_thread.get_dest(dest_x, dest_y)
        car_thread.start()
        car_threads.append(car_thread)
        map.cars.append(car_thread)
    for car_thread in car_threads:
        car_thread.join()
    print("All cars have arrived at the destination.")


if __name__ == "__main__":
    map = create_map()
    sigle_car_test(map)
