#热力图相关接口:根据d3待定
#
import typing
import pandas as pd

class color:  ...

class 控制点:  ...

class API:

    __日期: list
    __小时: list
    __data: pd.DataFrame

    __异步时间预处理结果: dict['流量图','热力图'] 
    




    class 订单散点图:

        def 起点(self, 日期:list, 小时:list, 地图中心坐标)->list[dict['lat':float, 'lng':float]]:
            '''
            实时计算
            '''
            ...

        def 终点(self, 日期:list, 小时:list, 地图中心坐标)->list[dict['lat':float, 'lng':float]]:
            '''
            实时计算
            '''
            ...


    class 等时线图:
        
        def 平均k分钟线(self, k:list[int], 中心坐标)->dict[int:list[控制点]]:
            '''
            实时计算
            '''
            ...

        def 某小时k分钟线(self, k:list[int], 中心坐标, 日期:list, 小时:list):
            '''
            实时计算
            '''
            ...

        __半径:float
        
        
    class 流量图:

        def 画图(self, 日期:list, 小时:list) -> list[list[int]]: 
            '''
            实时计算
            '''
            ...


    class 时间地图:
        
        def 车流图(self, 街区:list[int]) -> list[list[color]]:
            '''
            提前计算
            '''
            ...

        def 降雨图(self) -> list[list[color]]:
            '''
            提前计算
            '''
            ...

        def 温度图(self) -> list[list[color]]:
            '''
            提前计算
            '''
            ...

    class 热力图:

        def 画图(self, 日期:list, 小时:list)->list[dict['x':float, 'y':float, 'value':float]]:
            '''
            实时计算
            '''
            ...
