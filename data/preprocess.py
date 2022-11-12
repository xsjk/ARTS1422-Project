import pandas as pd
import numpy as np
import numba as nb
import json
import time

np.seterr(divide='ignore', invalid='ignore')

@nb.njit(fastmath=True)
def in_polygon_nb(points:np.ndarray,poly:np.ndarray)->np.ndarray:
    n = len(poly)
    res = np.zeros(len(points), dtype=np.bool_)
    for i in range(len(points)):
        p = points[i]
        j = n - 1
        for k in range(n):
            if (poly[k,1] - p[1]) * (poly[j,1] - p[1]) < 0 and p[0] < (poly[j,0] - poly[k,0]) * (p[1] - poly[k,1]) / (poly[j,1] - poly[k,1]) + poly[k,0]:
                res[i] = not res[i]
            j = k
    return res

def in_polygon_np(points:np.ndarray,poly:np.ndarray)->np.ndarray:
    p = np.expand_dims(poly, axis=0) - np.expand_dims(points, axis=1)
    d = p[:,1:,:] - p[:,:-1,:]
    return np.sum((p[:,:-1,1] * p[:,1:,1]<=0) & (p[:,:-1,0] - p[:,:-1,1] * d[:,:,0] / d[:,:,1] >0), axis=1) & 1 == 1

in_polygon = in_polygon_nb

def run(i:int):

    data = pd.read_csv(f'./taxi/dwv_order_make_haikou_{i}.txt', sep='\t')
    data.rename(columns={c:c[24:] for c in data.columns}, inplace=True)
    data['arrive_time'].replace('0000-00-00 00:00:00',None, inplace=True)
    data['departure_time'] = pd.to_datetime(data['arrive_time'])
    data['arrive_time'] = data['departure_time'] + pd.to_timedelta(data['normal_time'], 'm')
    data = data[['county', 'traffic_type', 'start_dest_distance', 'departure_time', 'arrive_time','normal_time', 'product_1level', 'dest_lng', 'dest_lat', 'starting_lng', 'starting_lat']]

    for county_code in range(460105,460109):
        geo_json = json.load(open(f'./geojson/{county_code}.json',encoding='utf-8'))
        for j, feature in enumerate(geo_json['features']):
            start_time = time.time()
            polygons = np.array(feature['geometry']['coordinates'][0])
            in_poly = in_polygon(data[['starting_lng','starting_lat']].to_numpy(),polygons)
            data.loc[in_poly,'starting_district'] = f'{county_code}{j:02d}'
            print(f'dwv_order_make_haikou_{i} {county_code}{j:02d} {feature["properties"]["name"]:<5} {time.time() - start_time:.2f}s, {np.sum(in_poly)} records')
            start_time = time.time()
            in_poly = in_polygon(data[['dest_lng','dest_lat']].to_numpy(),polygons)
            data.loc[in_poly,'dest_district'] = f'{county_code}{j:02d}'
            print(f'dwv_order_make_haikou_{i} {county_code}{j:02d} {feature["properties"]["name"]:<5} {time.time() - start_time:.2f}s, {np.sum(in_poly)} records')
    
    data.to_pickle(f'./data_{i}.pkl')
    


if __name__ == '__main__':

    from multiprocessing import Pool
    pool = Pool(8)
    pool.map(run, range(1,9))
    pool.close()
    pool.join()

    print('merge')

    pd.to_pickle(pd.concat([pd.read_pickle(f'./data_{i}.pkl') for i in range(1,9)]), './data.pkl')

    print('done')

    from os import remove
    for i in range(1,9):
        remove(f'./data_{i}.pkl')

    
    # import matplotlib.pyplot as plt
    # points_np = 5*(np.random.rand(1000,2)-.5)
    # polygon_np = np.array([
    #     [0,0],
    #     [2,0],
    #     [2,2],
    #     [1,1],
    #     [0,2],
    #     [-1,4],
    #     [0,0]
    # ]).astype(float)

    # # print(polygon_np)
    # in_poly_np = in_polygon(points_np,polygon_np)
    # import time
    # start = time.time()
    # in_poly_np = in_polygon(points_np,polygon_np)
    # end = time.time()
    # print(end-start)
    # # print(in_poly_np.shape)
    # # print(points_np)

    # plt.scatter(points_np[:,0],points_np[:,1],c=in_poly_np)
    # plt.show()
