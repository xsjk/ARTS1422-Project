import datetime as dt
import numba as nb
import pandas as pd
import numpy as np
import json

months  = [5,6,7,8,9,10]
days = [31,30,31,31,30,31]
index = 0
index_to_districts_names = ['海秀镇','西秀镇','海秀街道','长流镇','东山镇','永兴镇','石山镇','秀英街道','龙桥镇','金宇街道','大同街道','龙泉镇','城西镇','新坡镇','遵谭镇','海垦街道','滨海街道','金贸街道','中山街道','龙塘镇','府城街道','旧州镇','云龙镇','大坡镇','红旗镇','甲子镇','三门坡镇','滨江街道','凤翔街道','国兴街道','白沙街道','三江镇','白龙街道','博爱街道','新埠街道','海府街道','蓝天街道','人民路街道','和平南街道','灵山镇','演丰镇','大致坡镇','海甸街道']

#loading data
total_data = pd.read_pickle('./data/data.pkl')
time_map_departure = np.load('./data/时间地图_departure.npy')
time_map_arrive = np.load('./data/时间地图_arrive.npy')
district_town_id_to_index = json.load(open('./data/时间地图_npy_keys_to_index.json'))
arrive_days_to_index = [np.load(f'./data/arrive_day_to_index/arrive_{i}day_to_index.npy') for i in range(184)]
departure_days_to_index = [np.load(f'./data/departure_day_to_index/departure_{i}day_to_index.npy') for i in range(184)]
arrive_hours_to_index = [np.load(f'./data/arrive_hour_to_index/arrive_{i}hour_to_index.npy') for i in range(24)]
departure_hours_to_index = [np.load(f'./data/departure_hour_to_index/departure_{i}hour_to_index.npy') for i in range(24)]
topological_graph_data_by_departure_time = np.load('./data/topological_graph_by_departure_time.npy')
topological_graph_data_by_arrive_time = np.load('./data/topological_graph_by_arrive_time.npy')

@nb.njit
def find_index(index, indices):
    for i in index:
        indices[i] = True

@nb.jit(forceobj=True)
def find_departure_day_index(days:list[int]):
    result = np.zeros(len(total_data), dtype=bool)
    for day in days:
        find_index(departure_days_to_index[day], result)
    return result

@nb.jit(forceobj=True)
def find_arrive_day_index(days:list[int]):
    result = np.zeros(len(total_data), dtype = bool)
    for day in days:
        find_index(arrive_days_to_index[day], result)
    return result

@nb.jit(forceobj=True)
def find_departure_hour_index(hours:list[int]):
    result = np.zeros(len(total_data), dtype = bool)
    for hour in hours:
        find_index(departure_hours_to_index[hour], result)
    return result

@nb.jit(forceobj=True)
def find_arrive_hour_index(hours:list[int]):
    result = np.zeros(len(total_data), dtype = bool)
    for hour in hours:
        find_index(arrive_hours_to_index[hour], result)
    return result

def get_df(days:list[int], hours:list[int], which:str):
    if(which == 'departure_time'):
        return total_data[find_departure_day_index(days) & find_departure_hour_index(hours)]
    elif(which == 'arrive_time'):
        return total_data[find_arrive_day_index(days) & find_arrive_hour_index(hours)]



class date:

    __days:list[int] = []
    __hours:list[int] = []
    __days_bool_index:np.ndarray = np.array([])
    __hours_bool_index:np.ndarray = np.array([])
    __data:pd.DataFrame = pd.DataFrame()
    __type:str = ''

    def get_data(self, days:list[int], hours:list[int], type:str):
        if days == []:
            days = list(range(184))
        if hours == []:
            hours = list(range(24))
        assert 0 <= min(days) <= max(days) <= 183 and 0 <= min(hours) <= max(hours) <= 23
        if type == self.__type:
            if days != self.__days or hours != self.__hours:
                if days != self.__days:
                    self.__days = days
                    self.__days_bool_index = find_departure_day_index(days) if type == 'departure_time' else find_arrive_day_index(days)
                if hours != self.__hours:
                    self.__hours = hours
                    self.__hours_bool_index = find_departure_hour_index(hours) if type == 'departure_time' else find_arrive_hour_index(hours)
                self.__data = total_data[self.__days_bool_index & self.__hours_bool_index]
        else:
            self.__type = type
            self.__days = days
            self.__hours = hours
            self.__days_bool_index = find_departure_day_index(days) if type == 'departure_time' else find_arrive_day_index(days)
            self.__hours_bool_index = find_departure_hour_index(hours) if type == 'departure_time' else find_arrive_hour_index(hours)
            self.__data = total_data[self.__days_bool_index & self.__hours_bool_index]
        return self.__data


d = date()

#约定先lng 后lat


class isochrone_graph:

    #约定车辆速度约为每小时45km(每分钟0.75km)
    #约定0.01个经纬度表示1km
    #对于k分钟时间线,圆圈最大半径不应大于k*0.0075*0.1
    #半径默认设为500m(0.5)
    __默认最小半径:float = 0.003 #单位经纬度
    __最小半径增量:float = 0.001 #单位经纬度
    __一个等时线最少点数:int = 10


    def k_min_isochrone_by_departure_time(self, k:list[int], middle_point_coordinate:list[float, float], date:list[int], hour:list[int])->list[list[list[float],list[float]]]:
        if date==[]:
            date = list(range(184))
        if hour==[]:
            hour = list(range(24))
        df = d.get_data(date,hour,'departure_time')
        result = []
        delta_lng = df['starting_lng'].values - middle_point_coordinate[0]
        delta_lat = df['starting_lat'].values - middle_point_coordinate[1]
        normal_times = df['normal_time'].values
        bases = np.array([np.array([np.cos(np.radians(i)), np.sin(np.radians(i))]) for i in range(0,360,20)])
        #画k[i]分钟图
        for i in range(len(k)):
            r = self.__默认最小半径
            max_r = k[i] * 0.0075 * 0.2
            while r <= max_r:
                #初步筛选起df点位置与时长合乎选择条件的字段
                df_index = ((delta_lng * delta_lng + delta_lat * delta_lat) < r*r) & (normal_times <= k[i])
                if np.sum(df_index) > self.__一个等时线最少点数:
                    data = df[df_index]
                    vectors = (data[['dest_lng','dest_lat']].values - data[['starting_lng','starting_lat']].values) / data['normal_time'].values.reshape(data.shape[0],1) * k[i]
                    bases_index = (np.floor((np.arctan2(vectors[:,1],vectors[:,0]) / np.pi * 180 + 10) % 360) / 20).astype(np.int8)
                    bases_product = np.sum(bases[bases_index]*vectors,axis=1)
                    result_range = np.zeros(18)
                    result_persentage = np.zeros(18)
                    for j in range(18):
                        result_range[j] = np.max(bases_product[np.equal(bases_index,j)])
                        result_persentage[j] = np.sum(np.equal(bases_index,j))
                    result_range[np.isnan(result_range)] = 0
                    result_persentage /= np.sum(result_persentage)
                    result.append([result_range.tolist(), result_persentage.tolist()])
                    break
                else:
                    r += self.__最小半径增量
            if r > max_r:
                raise(f"Don't have enough points to draw k[{i}] in isochrone_graph::k_min_isochrone")
        return result

    def k_min_isochrone_by_arrival_time(self, k:list[int], middle_point_coordinate:list[float, float], date:list[int], hour:list[int])->list[list[list[float],list[float]]]:
        if date==[]:
            date = list(range(184))
        if hour==[]:
            hour = list(range(24))
        df = d.get_data(date,hour,'arrive_time')
        result = []
        delta_lng = df['dest_lng'].values - middle_point_coordinate[0]
        delta_lat = df['dest_lat'].values - middle_point_coordinate[1]
        normal_times = df['normal_time'].values
        bases = np.array([np.array([np.cos(np.radians(i)), np.sin(np.radians(i))]) for i in range(0,360,20)])
        #画k[i]分钟图
        for i in range(len(k)):
            r = self.__默认最小半径
            max_r = k[i] * 0.0075 * 0.2
            while r <= max_r:
                #初步筛选起df点位置与时长合乎选择条件的字段
                df_index = ((delta_lng * delta_lng + delta_lat * delta_lat) < r*r) & (normal_times <= k[i])
                if np.sum(df_index) > self.__一个等时线最少点数:
                    data = df[df_index]
                    vectors = (data[['starting_lng','starting_lat']].values - data[['dest_lng','dest_lat']].values) / data['normal_time'].values.reshape(data.shape[0],1) * k[i]
                    bases_index = (np.floor((np.arctan2(vectors[:,1],vectors[:,0]) / np.pi * 180 + 10) % 360) / 20).astype(np.int8)
                    bases_product = np.sum(bases[bases_index]*vectors,axis=1)
                    result_range = np.zeros(18)
                    result_persentage = np.zeros(18)
                    for j in range(18):
                        result_range[j] = np.max(bases_product[np.equal(bases_index,j)])
                        result_persentage[j] = np.sum(np.equal(bases_index,j))
                    result_range[np.isnan(result_range)] = 0
                    result_persentage /= np.sum(result_persentage)
                    print(result_persentage)
                    result.append([result_range.tolist(), result_persentage.tolist()])
                    break
                else:
                    r += self.__最小半径增量
            if r > max_r:
                raise(f"Don't have enough points to draw k[{i}] in isochrone_graph::k_min_isochrone")
        return result

class order_scatter_diagram:
    __半径:float = 0.05 #单位经纬度

    #已调试
    def origin(self, date:list[int], hour:list[int], middle_point_coordinate:list[float, float])->list[list[float, float]]:
        if date==[]:
            date = list(range(184))
        if hour==[]:
            hour = list(range(24))
        df = d.get_data(date, hour, 'departure_time')
        lngs = df['starting_lng'].values - middle_point_coordinate[0]
        lats = df['starting_lat'].values - middle_point_coordinate[1]
        satisfied_indexs = lngs * lngs + lats * lats < self.__半径 * self.__半径
        return df[satisfied_indexs][['starting_lng','starting_lat']].values.tolist()

    #已调试
    def dest(self, date:list[int], hour:list[int], middle_point_coordinate:list[float, float]):
        if date==[]:
            date = list(range(184))
        if hour==[]:
            hour = list(range(24))
        df = d.get_data(date, hour, 'arrive_time')
        lngs = df['dest_lng'].values - middle_point_coordinate[0]
        lats = df['dest_lat'].values - middle_point_coordinate[1]
        satisfied_index = lngs * lngs + lats * lats < self.__半径 * self.__半径
        return df[satisfied_index][['dest_lng','dest_lat']].values.tolist()

#热力图
class thermodynamic_diagram:

    @staticmethod
    def subdivided(middle_point_coordinate:list[float, float], l:float, k:int, array, result:list[dict['lat':float, 'lng':float, 'count':float]])->None:
        if array.shape[0] == 0:
            return
        elif k == 0:
            result.append({'lng':middle_point_coordinate[0],'lat':middle_point_coordinate[1],'count':array.shape[0]})
        else:
            grater_lng = array[:,0] >= middle_point_coordinate[0]
            grater_lat = array[:,1] > middle_point_coordinate[1]
            smaller_l = l / 2.0
            thermodynamic_diagram.subdivided([middle_point_coordinate[0] + smaller_l, middle_point_coordinate[1] + smaller_l], smaller_l, k-1, array[grater_lng & grater_lat], result)
            thermodynamic_diagram.subdivided([middle_point_coordinate[0] + smaller_l, middle_point_coordinate[1] - smaller_l], smaller_l, k-1, array[grater_lng & ~grater_lat], result)
            thermodynamic_diagram.subdivided([middle_point_coordinate[0] - smaller_l, middle_point_coordinate[1] + smaller_l], smaller_l, k-1, array[~grater_lng & grater_lat], result)
            thermodynamic_diagram.subdivided([middle_point_coordinate[0] - smaller_l, middle_point_coordinate[1] - smaller_l], smaller_l, k-1, array[~grater_lng & ~grater_lat], result)

    #boundary : lat : [19.520 , 20.120] : delta = 0.6
    #boundary : lng : [110.100, 110.710] : delta = 0.61
    #当放大倍率为k时total_lng = 0.61 / k, total_lat = 0.6 / k
    __边细分次数:int = 6 #代表2**6

    def out_degree(self, date:list[int], hour:list[int], middle_point_coordinate:list[float, float], enlarge_factor:int)->list[dict['lat':float, 'lng':float, 'count':int]]:
        if date == []:
            date = list(range(184))
        if hour == []:
            hour = list(range(24))
        result = []
        df = d.get_data(date, hour, 'departure_time')
        l = 0.31 / enlarge_factor
        array = df[['starting_lng','starting_lat']].values
        array_index = (array[:,0] <= middle_point_coordinate[0] + l) & (array[:,0] > middle_point_coordinate[0] - l) & (array[:,1] <= middle_point_coordinate[1] + l) & (array[:,1] > middle_point_coordinate[1] - l)
        thermodynamic_diagram.subdivided(middle_point_coordinate, l, self.__边细分次数, array[array_index],result)
        return result

    def in_degree(self, date:list[int], hour:list[int], middle_point_coordinate:list[float, float], enlarge_factor:int)->list[dict['lat':float, 'lng':float, 'count':int]]:
        if date == []:
            date = list(range(184))
        if hour == []:
            hour = list(range(24))
        result = []
        df = d.get_data(date, hour, 'arrive_time')
        l = 0.31 / enlarge_factor
        array = df[['starting_lng','starting_lat']].values
        array_index = (array[:,0] <= middle_point_coordinate[0] + l) & (array[:,0] > middle_point_coordinate[0] - l) & (array[:,1] <= middle_point_coordinate[1] + l) & (array[:,1] > middle_point_coordinate[1] - l)
        thermodynamic_diagram.subdivided(middle_point_coordinate, l, self.__边细分次数, array[array_index],result)
        return result

class time_map:

    def traffic_flow_in_degree_graph(self, towns:list[int]) -> list[list[float]]:
        data = np.zeros(184 * 24).reshape(184,24)
        for town in towns:
            data = np.add(data, time_map_departure[district_town_id_to_index[str(town)]])
        total_max = np.max(np.max(data))
        total_min = np.min(np.min(data))
        total_k = 1.0 / (total_max - total_min)
        data = (data - total_min) * total_k
        return data.tolist()

    def traffic_flow_out_degree_graph(self, towns:list[int])->list[list[float]]:
        data = np.zeros(184 * 24).reshape(184,24)
        for town in towns:
            data = np.add(data, time_map_arrive[district_town_id_to_index[str(town)]])
        total_max = np.max(np.max(data))
        total_min = np.min(np.min(data))
        total_k = 1.0 / (total_max - total_min)
        data = (data - total_min) * total_k
        return data.tolist()

class topological_graph:
    def draw_topological_graph_by_departure_time(self, days:list[int], hours:list[int])->list[list[int]]:
        if days == []:
            days = list(range(184))
        if hours == []:
            hours = list(range(24))
        ans = []
        result = np.zeros((43,43))
        for day in days:
            for hour in hours:
                result += topological_graph_data_by_departure_time[day][hour]
        total_data = np.sum(result)
        for start in range(43):
            for end in range(43):
                if result[start][end] >= total_data*0.0035:
                    ans.append({'source':index_to_districts_names[start], 'target':index_to_districts_names[end], 'value':result[start][end]})
        return ans
    def draw_topological_graph_by_arrival_time(self, days:list[int], hours:list[int])->list[list[int]]:
        if days == []:
            days = list(range(184))
        if hours == []:
            hours = list(range(24))
        ans = []
        result = np.zeros((43,43))
        for day in days:
            for hour in hours:
                result += topological_graph_data_by_arrive_time[day][hour]
        total_data = np.sum(result)
        for start in range(43):
            for end in range(43):
                if result[start][end] >= total_data*0.0035:
                    ans.append({'source':index_to_districts_names[start], 'target':index_to_districts_names[end], 'value':result[start][end]})
        return ans
