import pandas as pd
import numpy as np
import json

months  = [5,6,7,8,9,10]
days = [31,30,31,31,30,31]
index = 0
index_to_month_day = dict()

for i in range(len(months)):
    for j in range(1,days[i]+1):
        index_to_month_day[index] = [months[i], j]
        index+=1


total_data = pd.read_pickle(r'./data/data.pkl')
time_map_departure = np.load(r'./data\时间地图_departure.npy')
time_map_arrive = np.load(r'./data\时间地图_arrive.npy')
district_town_id_to_index = json.load(open(r'./data\时间地图_npy_keys_to_index.json','r',encoding='utf-8'))

#已调试
def update_data(data, type:str):
    if data.size==0:
        raise('NULL Data are given in function update_data!!!')
    if type != 'departure_time' and type != 'arrive_time':
        raise('Invalid type is given in function update_data!!!')
    bool_index = np.zeros(total_data.shape[0],dtype=bool)
    for i in data:
        bool_index |= (total_data[type]>=i[0]).values & (total_data[type]<= i[1]).values
    return total_data[bool_index]

#已调试
def merge_hour(hours:list[int])->list[list[int,int]]:#list[开始时间, 持续时长]
    h = [[i-1,1] for i in sorted(hours)]
    i = 0
    while i < len(h) - 1:
        if h[i][0]+h[i][1] == h[i+1][0]:
            h[i][1] += h[i+1][1]
            h.pop(i+1)
        else:
            i += 1
    return h

#已调试
def merge_date(date:list[list[int, int]], hours:list[int]):
    h = merge_hour(hours)
    periods = np.array([np.array([np.datetime64(f'2017-{i[0]:02d}-{i[1]:02d} {j[0]:02d}:00:00'), np.datetime64(f'2017-{i[0]:02d}-{i[1]:02d} {j[0]:02d}:00:00') + np.timedelta64(j[1], 'h')]) for i in date for j in h])
    return periods


class date:

    __date = np.empty((0,2),dtype=np.datetime64)
    __data:pd.DataFrame = pd.DataFrame()
    __type:str = ''

    def get_data(self, date:list[list[int, int]], hours:list[int], type:str):
        date = merge_date(date, hours)        
        if (date.shape == self.__date.shape):
            if (date == self.__date).all() and (type == self.__type):
                return self.__data
        self.__date = date
        self.__type = type
        self.__data = update_data(self.__date, self.__type)
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


    def k_min_isochrone(self, k:list[int], middle_point_coordinate:list[float, float], date:list[int], hour:list[int])->list[list[float],list[float],list[float]]:
        for i in range(len(date)):
            date[i] = index_to_month_day[date[i]][:]
        # if k[1] - k[0] < 10 or k[2] - k[1] < 10:
        #     raise('Invalid K is given in function 等时线图::某小时k分钟线!!!')
        df = d.get_data(date,hour,'departure_time')
        result = []
        #筛选起点符合要求的字段
        delta_lng = df['starting_lng'].values - middle_point_coordinate[0]
        delta_lat = df['starting_lat'].values - middle_point_coordinate[1]
        normal_times = df['normal_time'].values
        bases = np.array([np.array([np.cos(np.radians(i)), np.sin(np.radians(i))]) for i in range(0,360,20)])
        #画k[i]分钟图
        print(df)
        for i in range(len(k)):
            r = self.__默认最小半径
            max_r = k[i] * 0.0075 * 0.2
            while r <= max_r:
                #初步筛选起df点位置与时长合乎选择条件的字段
                df_index = ((delta_lng * delta_lng + delta_lat * delta_lat) < r*r) & (normal_times >= (k[i] - 5)) & (normal_times < (k[i] + 5))
                if np.sum(df_index) > self.__一个等时线最少点数:
                    data = df[df_index]
                    vectors = (data[['dest_lng','dest_lat']].values - data[['starting_lng','starting_lat']].values) / data['normal_time'].values.reshape(data.shape[0],1) * k[i]
                    bases_index = (np.floor((np.arctan2(vectors[:,1],vectors[:,0]) / np.pi * 180 + 10) % 360) / 20).astype(np.int8)
                    bases_product = np.sum(bases[bases_index]*vectors,axis=1)
                    result_i = np.zeros(18)
                    for j in range(18):
                        result_i[j] = np.mean(bases_product[np.equal(bases_index,j)])
                    result_i[np.isnan(result_i)] = 0
                    result.append(result_i.tolist())
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
        for i in range(len(date)):
            date[i] = index_to_month_day[date[i]][:]
        df = d.get_data(date, hour, 'departure_time')
        lngs = df['starting_lng'].values - middle_point_coordinate[0]
        lats = df['starting_lat'].values - middle_point_coordinate[1]
        satisfied_indexs = lngs * lngs + lats * lats < self.__半径 * self.__半径
        return df[satisfied_indexs][['starting_lng','starting_lat']].values.tolist()

    #已调试
    def dest(self, date:list[int], hour:list[int], middle_point_coordinate:list[float, float]):
        for i in range(len(date)):
            date[i] = index_to_month_day[date[i]][:]
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
        if date is None:
            return self.out_degree(list(range(184)), hour, middle_point_coordinate, enlarge_factor)
        if hour is None:
            return self.out_degree(date, list(range(24)), middle_point_coordinate, enlarge_factor)
        for i in range(len(date)):
            date[i] = index_to_month_day[date[i]][:]
        result = []
        df = d.get_data(date, hour, 'departure_time')
        print('get_data')
        print(df)
        l = 0.31 / enlarge_factor
        array = df[['starting_lng','starting_lat']].values
        array_index = (array[:,0] <= middle_point_coordinate[0] + l) & (array[:,0] > middle_point_coordinate[0] - l) & (array[:,1] <= middle_point_coordinate[1] + l) & (array[:,1] > middle_point_coordinate[1] - l)
        # print(df[array_index])
        thermodynamic_diagram.subdivided(middle_point_coordinate, l, self.__边细分次数, array[array_index],result)
        # with open(r"D:\Users\geshy\Desktop\tmp.txt",'w',encoding='utf-8') as f:
        #     f.write(str(result))
        print('result:',len(result))
        return result

    def in_degree(self, date:list[int], hour:list[int], middle_point_coordinate:list[float, float], enlarge_factor:int)->list[dict['lat':float, 'lng':float, 'count':int]]:
        if date is None:
            return self.out_degree(list(range(184)), hour, middle_point_coordinate, enlarge_factor)
        if hour is None:
            return self.out_degree(date, list(range(24)), middle_point_coordinate, enlarge_factor)
        for i in range(len(date)):
            date[i] = index_to_month_day[date[i]][:]
        result = []
        df = d.get_data(date, hour, 'arrive_time')
        l = 0.31 / enlarge_factor
        array = df[['starting_lng','starting_lat']].values
        array_index = (array[:,0] <= middle_point_coordinate[0] + l) & (array[:,0] > middle_point_coordinate[0] - l) & (array[:,1] <= middle_point_coordinate[1] + l) & (array[:,1] > middle_point_coordinate[1] - l)
        # print(df[array_index])
        thermodynamic_diagram.subdivided(middle_point_coordinate, l, self.__边细分次数, array[array_index],result)
        # with open(r"D:\Users\geshy\Desktop\tmp.txt",'w',encoding='utf-8') as f:
        #     f.write(str(result))
        return result

class time_map:

    def traffic_flow_in_degree_graph(self, towns:list[int]) -> list[list[float]]:
        data = np.zeros(184 * 24).reshape(184,24)
        for town in towns:
            data = np.add(data, time_map_departure[district_town_id_to_index[str(town)]])
        total_max = np.max(np.max(data))
        total_min = np.min(np.min(data))
        total_k = 1.0 / total_max - total_min
        data = (data - total_min) * total_k
        return data.tolist()

    def traffic_flow_out_degree_graph(self, towns:list[int])->list[list[float]]:
        data = np.zeros(184 * 24).reshape(184,24)
        for town in towns:
            data = np.add(data, time_map_arrive[district_town_id_to_index[str(town)]])
        total_max = np.max(np.max(data))
        total_min = np.min(np.min(data))
        total_k = 1.0 / total_max - total_min
        data = (data - total_min) * total_k
        return data.tolist()