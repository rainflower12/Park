# def identify_directions(map, x, y):
#     directions = []

#     # 左
#     if x - 1 >= 0 and map[x - 1][y] == 1:
#         directions.append("左")
    
#     # 右
#     if x + 1 < len(map) and map[x + 1][y] == 1:
#         directions.append("右")
    
#     # 上
#     if y - 1 >= 0 and map[x][y - 1] == 1:
#         directions.append("上")
    
#     # 下
#     if y + 1 < len(map[0]) and map[x][y + 1] == 1:
#         directions.append("下")
    
#     # 左上
#     if x - 1 >= 0 and y - 1 >= 0 and map[x - 1][y - 1] == 1:
#         directions.append("左上")
    
#     # 左下
#     if x - 1 >= 0 and y + 1 < len(map[0]) and map[x - 1][y + 1] == 1:
#         directions.append("左下")
    
#     # 右上
#     if x + 1 < len(map) and y - 1 >= 0 and map[x + 1][y - 1] == 1:
#         directions.append("右上")
    
#     # 右下
#     if x + 1 < len(map) and y + 1 < len(map[0]) and map[x + 1][y + 1] == 1:
#         directions.append("右下")
    
#     return directions

# # 示例地图
# map = [
#     [1, 0, 1, 0, 0],
#     [0, 1, 0, 1, 0],
#     [1, 0, 1, 0, 1],
#     [0, 0, 1, 1, 0],
# ]

# # 识别坐标 (2, 2) 的可行驶方向
# print(identify_directions(map, 2, 2))



# # x = car.x
#         # y = car.y
#         # pre_x = car.pre_x
#         # pre_y = car.pre_y
#         # if pre_y in self.upcolumn:
#         #     if dest_x < x - self.height:
#         #         if x - 2 >= 0:
#         #             car.direction = 1  # 如果已经在上行列，直接向上
#         #             car.pre_direction = 1
#         #     # 检查 y 方向
#         #     elif dest_y > y:
#         #         if y + 2 < len(self.layout.columns):
#         #             if x in self.rightrow:
#         #                 car.direction = 4  # 如果已经在右行行，直接向右移动
#         #                 car.pre_direction = 4
#         #                 return
#         #             elif x - 1 in self.rightrow:
#         #                 car.direction = 1
#         #                 car.pre_direction = 4
#         #             elif x + 1 in self.rightrow:
#         #                 car.direction = 2
#         #                 car.pre_direction = 4
#         #     elif dest_y < y:
#         #         if y - 2 >= 0:
#         #             if x in self.leftrow:
#         #                 car.direction = 3  # 如果已经在左行行，直接向左移动
#         #                 car.pre_direction = 3
#         #                 return
#         #             if x - 1 in self.leftrow:
#         #                 car.direction = 1
#         #                 car.pre_direction = 3
#         #             elif x + 1 in self.leftrow:
#         #                 car.direction = 2
#         #                 car.pre_direction = 3
#         # elif pre_y in self.downcolumn:
#         #     if dest_x > x + self.height:
#         #         if x + 2 < len(self.layout):
#         #             car.direction = 2  # 如果已经在下行列，直接向下移动
#         #             car.pre_direction = 2
#         #     # 检查 y 方向
#         #     elif dest_y > y:
#         #         if y + 2 < len(self.layout.columns):
#         #             if x in self.rightrow:
#         #                 car.direction = 4  # 如果已经在右行行，直接向右移动
#         #                 car.pre_direction = 4
#         #                 return
#         #             if x - 1 in self.rightrow:
#         #                 car.direction = 1
#         #                 car.pre_direction = 4
#         #             elif x + 1 in self.rightrow:
#         #                 car.direction = 2
#         #                 car.pre_direction = 4
#         #     elif dest_y < y:
#         #         if y - 2 >= 0:
#         #             if x in self.leftrow:
#         #                 car.direction = 3  # 如果已经在左行行，直接向左移动
#         #                 car.pre_direction = 3
#         #                 return
#         #             if x - 1 in self.leftrow:
#         #                 car.direction = 1
#         #                 car.pre_direction = 3
#         #             elif x + 1 in self.leftrow:
#         #                 car.direction = 2
#         #                 car.pre_direction = 3
#         # elif pre_x in self.rightrow:
#         #     if dest_y > y + self.weight:
#         #         if y + 2 < len(self.layout.columns):
#         #             car.direction = 4  # 如果已经在下行列，直接向下移动
#         #             car.pre_direction = 4
#         #     elif dest_x > x:
#         #         if x + 2 < len(self.layout):
#         #             if y in self.downcolumn:
#         #                 car.direction = 2  # 如果已经在下行列，直接向下移动
#         #                 car.pre_direction = 2
#         #                 return
#         #             elif y - 1 in self.downcolumn:
#         #                 car.direction = 3
#         #                 car.pre_direction = 2
#         #             elif y + 1 in self.downcolumn:
#         #                 car.direction = 4
#         #                 car.pre_direction = 2
#         #     elif dest_x <= x - 1:
#         #         if x - 2 >= 0:
#         #             if y in self.upcolumn:
#         #                 car.direction = 1  # 如果已经在上行列，直接向上移动
#         #                 car.pre_direction = 1
#         #                 return
#         #             elif y - 1 in self.upcolumn:
#         #                 car.direction = 3
#         #                 car.pre_direction = 1
#         #             elif y + 1 in self.upcolumn:
#         #                 car.direction = 4
#         #                 car.pre_direction = 1
#         # elif pre_x in self.leftrow:
#         #     if dest_y < y - self.weight:
#         #         if y - 2 > -1:
#         #             car.direction = 3  # 如果已经在下行列，直接向下移动
#         #             car.pre_direction = 3

#         #     elif dest_x > x:
#         #         if x + 2 < len(self.layout):
#         #             if y in self.downcolumn:
#         #                 car.direction = 2  # 如果已经在下行列，直接向下移动
#         #                 car.pre_direction = 2
#         #                 return
#         #             if y - 1 in self.downcolumn:
#         #                 car.direction = 3
#         #                 car.pre_direction = 2
#         #             elif y + 1 in self.downcolumn:
#         #                 car.direction = 4
#         #                 car.pre_direction = 2
#         #     elif dest_x < x:  # 改过1改2
#         #         if x - 2 >= 0:
#         #             if y in self.upcolumn:
#         #                 car.direction = 1  # 如果已经在上行列，直接向上移动
#         #                 car.pre_direction = 1
#         #                 return
#         #             if y - 1 in self.upcolumn:
#         #                 car.direction = 3
#         #                 car.pre_direction = 1
#         #             elif y + 1 in self.upcolumn:
#         #                 car.direction = 4
#         #                 car.pre_direction = 1
#         # # print(car.direction)
#         # if car.direction == 0:
#         #     print("还未有direction1")
#         #     if pre_y in self.upcolumn:
#         #         if dest_x < x:
#         #             if x - 2 >= 0:
#         #                 car.direction = 1  # 如果已经在上行列，直接向上
#         #                 car.pre_direction = 1
#         #     elif pre_y in self.downcolumn:
#         #         if dest_x > x:
#         #             if x + 2 < len(self.layout):
#         #                 car.direction = 2  # 如果已经在下行列，直接向下移动
#         #                 car.pre_direction = 2
#         #     elif pre_x in self.rightrow:
#         #         if dest_y > y:
#         #             if y + 2 < len(self.layout.columns):
#         #                 car.direction = 4  # 如果已经在下行列，直接向下移动
#         #                 car.pre_direction = 4
#         #     if dest_y < y:
#         #         if y - 2 > -1:
#         #             car.direction = 3  # 如果已经在下行列，直接向下移动
#         #             car.pre_direction = 3

#         # if car.direction == 0:
#         #     print("还未有direction2")
#         #     if x in self.leftrow or x in self.rightrow:
#         #         if (x + 2) < len(self.layout):
#         #             if pre_x <= x:
#         #                 if y in self.downcolumn:
#         #                     car.direction = 2  # 如果已经在下行列，直接向下移动
#         #                     return
#         #                 elif (y - 1) in self.downcolumn:
#         #                     car.direction = 3
#         #                 elif (y + 1) in self.downcolumn:
#         #                     car.direction = 4
#         #         elif (x - 2) >= 0:
#         #             if pre_x >= x:
#         #                 if y in self.upcolumn:
#         #                     car.direction = 1  # 如果已经在上行列，直接向上移动
#         #                     return
#         #                 elif (y - 1) in self.upcolumn:
#         #                     car.direction = 3
#         #                 elif (y + 1) in self.upcolumn:
#         #                     car.direction = 4
#         #     if y in self.upcolumn or y in self.downcolumn:
#         #         if (y + 2) < len(self.layout.columns):
#         #             if pre_y <= y:
#         #                 if x in self.rightrow:
#         #                     car.direction = 4  # 如果已经在下行列，直接向下移动
#         #                     return
#         #                 elif (x - 1) in self.rightrow:
#         #                     car.direction = 1
#         #                 elif (x + 1) in self.rightrow:
#         #                     car.direction = 2
#         #         elif (y - 2) >= 0:
#         #             if pre_y >= y:
#         #                 if x in self.leftrow:
#         #                     car.direction = 3  # 如果已经在上行列，直接向上移动
#         #                     return
#         #                 elif (x - 1) in self.leftrow:
#         #                     car.direction = 1
#         #                 elif (x + 1) in self.leftrow:
#         #                     car.direction = 2


# from collections import deque

# def nearest_zeros(matrix):
#     if not matrix:
#         return []

#     rows, cols = len(matrix), len(matrix[0])
#     directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
#     result = [[-1 for _ in range(cols)] for _ in range(rows)]

#     for i in range(rows):
#         for j in range(cols):
#             if matrix[i][j] == 1:
#                 visited = [[False for _ in range(cols)] for _ in range(rows)]
#                 queue = deque([(i, j, 0)])  # (row, col, distance)
#                 visited[i][j] = True

#                 while queue:
#                     row, col, distance = queue.popleft()

#                     if matrix[row][col] == 0:
#                         result[i][j] = distance
#                         break

#                     for dr, dc in directions:
#                         new_row, new_col = row + dr, col + dc
#                         if 0 <= new_row < rows and 0 <= new_col < cols and not visited[new_row][new_col]:
#                             queue.append((new_row, new_col, distance + 1))
#                             visited[new_row][new_col] = True

#     return result

# # 示例用法
# matrix = [
#     [0, 1, 0, 0, 1],
#     [0, 0, 1, 1, 0],
#     [1, 0, 0, 1, 0],
# ]
# result = nearest_zeros(matrix)
# for row in result:
#     print(row)

# import requests, threading

# urls = [
#     f"https://www.cnblogs.com/#p{page}"
#     for page in range(1, 50 + 1)
# ]


# def craw(url):
#     r = requests.get(url)
#     print(url, len(r.text))


# def sigle_thread():
#     print("single thread begin")
#     for url in urls:
#         craw(url)
#     print("single thread end")


# def multi_thread():
#     print("multi thread begin")
#     threads = []
#     for url in urls:
#         threads.append(threading.Thread(target=craw, args=(url,)))
#     for thread in threads:
#         thread.start()
#     for thread in threads:
#         thread.join()
#     print("multi thread end")


# sigle_thread()
# multi_thread()


# Pipeline 架构

# for i in range(10):
#     print(i)