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
            print("\033[1;32;40m>>>>>>>>")
            print(func.__name__, "\033[1;31;40m")
            print(argsDict)
            if "return" in argsDict:
                del argsDict["return"]
            for argKey, argType in argsDict.items():
                argsDict[argKey] = list(map(eval, request.args.getlist(f"{argKey}[]"))) if argType.__name__ == "list" else eval(request.args.get(argKey))
            print(argsDict)
            print("\033[1;31;40m<<<<<<<<\033[0m")
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
topological_graph = API.topological_graph()

@apiDeco("/kd")
def k_min_isochrone_by_departure_time(k:list[int], m:list[float, float], d:list[int], h:list[int]):
    return isochrone_graph.k_min_isochrone_by_departure_time(k, m, d, h)

@apiDeco("/ka")
def k_min_isochrone_by_arrival_time(k:list[int], m:list[float, float], d:list[int], h:list[int]):
    return isochrone_graph.k_min_isochrone_by_arrival_time(k, m, d, h)

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

@apiDeco("/drwd")
def draw_topological_graph_by_departure_time(d:list[int], h:list[int]):
    return topological_graph.draw_topological_graph_by_departure_time(d, h)

@apiDeco("/drwa")
def draw_topological_graph_by_arrival_time(d:list[int], h:list[int]):
    return topological_graph.draw_topological_graph_by_arrival_time(d, h)

@app.route("/")
def test_connection():
    return "Connected!"

app.run(host="0.0.0.0", port=5000, debug=True)