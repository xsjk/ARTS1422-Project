# -- deco stuff --

import functools
import inspect
from flask import Flask, request

app = Flask(__name__)

@app.after_request
def after_request(res):
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res

def apiDeco(rule):
    def deco(func):
        @app.route(rule, methods=["GET"])
        @functools.wraps(func)
        def decoratedFunc():
            argsDict = inspect.get_annotations(func)
            if "return" in argsDict:
                del argsDict["return"]
            for argKey, argType in argsDict.items():
                argsDict[argKey] = list(map(eval, request.args.getlist(f"{argKey}[]") if argType.__name__ == "list" else request.args.get(argKey)))
            return func(**argsDict)
        return decoratedFunc
    return deco

# ----------------

# integration with gsy's api

import API
isochrone_graph = API.isochrone_graph()
order_scatter_diagram = API.order_scatter_diagram()
thermodynamic_diagram = API.thermodynamic_diagram()
time_map = API.time_map()

@apiDeco("/k")
def k_min_isochrone(k:list[int], m:list[float, float], d:list[int], h:list[int]):
    return isochrone_graph.k_min_isochrone(k, m, d, h)

@apiDeco("/o")
def origin(d:list[int], h:list[int], m:list[float, float]):
    return order_scatter_diagram.origin(d, h, m)

@apiDeco("/d")
def dest(d:list[int], h:list[int], m:list[float, float]):
    return order_scatter_diagram.dest(d, h, m)

@apiDeco("/od")
def out_degree(d:list[int], h:list[int], m:list[float, float], e:int):
    return thermodynamic_diagram.out_degree(d, h, m, e)

@apiDeco("/id")
def in_degree(d:list[int], h:list[int], m:list[float, float], e:int):
    return thermodynamic_diagram.in_degree(d, h, m, e)

@apiDeco("/tfi")
def traffic_flow_in_degree_graph(t:list[int]):
    return time_map.traffic_flow_in_degree_graph(t)

@apiDeco("/tfo")
def traffic_flow_out_degree_graph(t:list[int]):
    return time_map.traffic_flow_out_degree_graph(t)