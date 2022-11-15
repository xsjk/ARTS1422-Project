# change absolute paths to relative paths @ 2022-11-15 14:12:00

import pandas as pd
import numpy as np

total_data = pd.read_pickle(r"data\data.pkl")

#已调试
def update_data(data: np.ndarray[np.ndarray[np.datetime64, np.datetime64]], type: str):
    if data.size == 0:
        raise("NULL Data are given in function update_data!!!")
    if type != "departure_time" and type != "arrive_time":
        raise("Invalid type is given in function update_data!!!")
    bool_index = np.zeros(total_data.shape[0], dtype=bool)
    for i in data:
        bool_index |= (total_data[type]>=i[0]).values & (total_data[type]<= i[1]).values
    return total_data[bool_index]

#已调试
def merge_hour(hours: list[int]) -> list[list[int, int]]: #list[开始时间, 持续时长]
    h = [[i-1, 1] for i in sorted(hours)]
    i = 0
    while i < len(h) - 1:
        if h[i][0] + h[i][1] == h[i + 1][0]:
            h[i][1] += h[i + 1][1]
            h.pop(i + 1)
        else:
            i += 1
    return h

#已调试
def merge_date(date: list[list[int, int]], hours: list[int]) -> np.ndarray[np.ndarray[np.datetime64, np.datetime64]]:
    h = merge_hour(hours)
    periods = np.array([np.array([np.datetime64(f"2017-{i[0]:02d}-{i[1]:02d} {j[0]:02d}:00:00"), np.datetime64(f"2017-{i[0]:02d}-{i[1]:02d} {j[0]:02d}:00:00") + np.timedelta64(j[1], "h")]) for i in date for j in h])
    return periods


class date:

    __date = np.empty((0, 2),dtype=np.datetime64)
    __data:pd.DataFrame = pd.DataFrame()
    __type:str = ""

    def get_data(self, date: list[int, int], hours: list[int], type: str):
        date = merge_date(date, hours)
        if (date.shape == self.__date.shape) and (date == self.__date) and (type == self.__type):
            return self.__data
        else:
            self.__date = date
            self.__type = type
            self.__data = update_data(self.__date, self.__type)
            return self.__data


d = date()

#约定先lng 后lat


class 等时线图:

    #约定车辆速度约为每小时45km(每分钟0.75km)
    #约定0.01个经纬度表示1km
    #对于k分钟时间线,圆圈最大半径不应大于k*0.0075*0.1
    #半径默认设为500m(0.5)
    __默认最小半径: float = 0.003 #单位经纬度
    __最小半径增量: float = 0.001 #单位经纬度
    __一个等时线最少点数: int = 10


    def 某小时k分钟线(self, k: list[int, int, int], 中心坐标: list[float, float], 日期: list[list[int, int]], 小时: list[int]) -> list[list[float], list[float], list[float]]:
        if k[1] - k[0] < 10 or k[2] - k[1] < 10:
            raise("Invalid K is given in function 等时线图::某小时k分钟线!!!")
        df = d.get_data(日期,小时,"departure_time")
        result = []
        #筛选起点符合要求的字段
        delta_lng = df["starting_lng"].values - 中心坐标[0]
        delta_lat = df["starting_lat"].values - 中心坐标[1]
        normal_times = df["normal_time"].values
        bases = np.array([np.array([np.cos(np.radians(i)), np.sin(np.radians(i))]) for i in range(0, 360, 20)])
        #画k[i]分钟图
        for i in range(3):
            r = self.__默认最小半径
            max_r = k[i] * 0.0075 * 0.2
            while r <= max_r:
                #初步筛选起df点位置与时长合乎选择条件的字段
                df_index = ((delta_lng * delta_lng + delta_lat * delta_lat) < r * r) & (normal_times >= (k[i] - 5)) & (normal_times < (k[i] + 5))
                if np.sum(df_index) > self.__一个等时线最少点数:
                    data = df[df_index]
                    vectors = (data[["dest_lng", "dest_lat"]].values - data[["starting_lng", "starting_lat"]].values) / data["normal_time"].values.reshape(data.shape[0], 1) * k[i]
                    bases_index = (np.floor((np.arctan2(vectors[:, 1], vectors[:, 0]) / np.pi * 180 + 10) % 360) / 20).astype(np.int8)
                    bases_product = np.sum(bases[bases_index] * vectors, axis=1)
                    result_i = np.zeros(18)
                    for j in range(18):
                        result_i[j] = np.mean(bases_product[np.equal(bases_index, j)])
                    result_i[np.isnan(result_i)] = 0
                    result.append(result_i.tolist())
                    break
                else:
                    r += self.__最小半径增量
            if r > max_r:
                raise(f"Don't have enough points to draw k[{i}] in 等时线图::某小时k分钟线")
        return result

class 订单散点图:
    __半径:float = 0.05 #单位经纬度

    #已调试
    def 起点(self, 日期: list[list[int, int]], 小时: list[int], 中心坐标: list[float, float]) -> list[list[float, float]]:
        df = d.get_data(日期, 小时, "departure_time")
        lngs = df["starting_lng"].values - 中心坐标[0]
        lats = df["starting_lat"].values - 中心坐标[1]
        satisfied_indexs = lngs * lngs + lats * lats < self.__半径 * self.__半径
        return df[satisfied_indexs][["starting_lng","starting_lat"]].values.tolist()

    #已调试
    def 终点(self, 日期: list[list[int, int]], 小时: list[int], 中心坐标: list[float, float]):
        df = d.get_data(日期, 小时, "arrive_time")
        lngs = df["dest_lng"].values - 中心坐标[0]
        lats = df["dest_lat"].values - 中心坐标[1]
        satisfied_index = lngs * lngs + lats * lats < self.__半径 * self.__半径
        return df[satisfied_index][["dest_lng", "dest_lat"]].values.tolist()

class 热力图:

    @staticmethod
    def subdivided(中心坐标: list[float, float], l: float, k: int, array: np.ndarray[np.ndarray[float, float]], result: list[dict["lat": float, "lng": float, "count": float]]) -> None:
        if array.shape[0] == 0:
            return
        elif k == 0:
            result.append({"lng": 中心坐标[0], "lat": 中心坐标[1], "count": array.shape[0]})
        else:
            grater_lng = array[:, 0] >= 中心坐标[0]
            grater_lat = array[:, 1] > 中心坐标[1]
            smaller_l = l / 2.0
            热力图.subdivided([中心坐标[0] + smaller_l, 中心坐标[1] + smaller_l], smaller_l, k-1, array[grater_lng & grater_lat], result)
            热力图.subdivided([中心坐标[0] + smaller_l, 中心坐标[1] - smaller_l], smaller_l, k-1, array[grater_lng & ~grater_lat], result)
            热力图.subdivided([中心坐标[0] - smaller_l, 中心坐标[1] + smaller_l], smaller_l, k-1, array[~grater_lng & grater_lat], result)
            热力图.subdivided([中心坐标[0] - smaller_l, 中心坐标[1] - smaller_l], smaller_l, k-1, array[~grater_lng & ~grater_lat], result)

    #boundary : lat : [19.520 , 20.120] : delta = 0.6
    #boundary : lng : [110.100, 110.710] : delta = 0.61
    #当放大倍率为k时total_lng = 0.61 / k, total_lat = 0.6 / k
    __边细分次数: int = 6 #代表2**4

    def 出度(self, 日期: list[list[int, int]], 小时: list[int], 中心坐标: list[float, float], 放大倍率: int) -> list[dict["lat": float, "lng": float, "count": int]]:
        result = []
        df = d.get_data(日期, 小时, "departure_time")
        l = 0.31 / 放大倍率
        array = df[["starting_lng", "starting_lat"]].values
        array_index = (array[:, 0] <= 中心坐标[0] + l) & (array[:, 0] > 中心坐标[0] - l) & (array[:, 1] <= 中心坐标[1] + l) & (array[:, 1] > 中心坐标[1] - l)
        print(df[array_index])
        热力图.subdivided(中心坐标, l, self.__边细分次数, array[array_index], result)
        with open(r"tmp.txt", "w", encoding="utf-8") as f:
            f.write(str(result))
        return result

    def 入度(self, 日期: list[list[int, int]], 小时: list[int], 中心坐标: list[float, float], 放大倍率: int)->list[dict["lat": float, "lng": float, "count": int]]:
        result = []
        df = d.get_data(日期, 小时, "arrive_time")
        l = 0.31 / 放大倍率
        array = df[["starting_lng", "starting_lat"]].values
        array_index = (array[:, 0] <= 中心坐标[0] + l) & (array[:, 0] > 中心坐标[0] - l) & (array[:, 1] <= 中心坐标[1] + l) & (array[:, 1] > 中心坐标[1] - l)
        print(df[array_index])
        热力图.subdivided(中心坐标, l, self.__边细分次数, array[array_index], result)
        with open(r"tmp.txt", "w", encoding="utf-8") as f:
            f.write(str(result))
        return result

class 时间地图:

    def 车流图出度(self, 街道: list[int]) -> list[list[float]]:
        pass

# a = 等时线图()
# a.某小时k分钟线(
#     [5,15,25],
#     [110.3550, 20.00],
#     [[5,7]],
#     [7,8,9]
# )

c = 热力图()