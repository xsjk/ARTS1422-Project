import pandas as pd

data = pd.read_csv("./data/weather/daily/weatherData.csv", names = ["date", "weather", "temperature", "wind"], encoding="utf-8")

del data["wind"]
del data["temperature"]

data["date"] = data["date"].map(lambda d: d.replace("年", "/").replace("月", "/").replace("日", " UTC"))

weatherMap = {
    "多云": 0.0,
    "小到中雨": 0.2,
    "阵雨": 0.3,
    "中雨": 0.4,
    "雷阵雨": 0.5,
    "中到大雨": 0.6,
    "大雨": 0.7,
    "大到暴雨": 0.8,
    "暴雨": 0.9,
    "大暴雨": 1.0,
}
data["weather"] = data["weather"].map(lambda w: sum(map(lambda ww: weatherMap[ww], w.split("/"))) / 2)

data.to_csv("./data/weather/daily/data.csv")