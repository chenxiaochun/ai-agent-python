import os
import requests
from dotenv import load_dotenv

load_dotenv()

dict_city_id = {"北京": "101010100"}


def get_weather(city: str):
    """获取某个城市的天气
    Args:
        city: 具体城市
    """

    url = "https://m54jab6qp5.re.qweatherapi.com/v7/weather/now"
    city_id = dict_city_id[city]

    params = {"location": city_id, "key": os.getenv("QWEATHER_API_KEY")}

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data["code"] == "200":
            weather_info = data["now"]
            info = f"城市：{city}\n天气状况：{weather_info['text']}\n温度：{weather_info['temp']}"
            print(info)
            return info
        else:
            print(f"错误：，状态码：{data['code']}")
    else:
        print(f"请求失败，状态码：{response.status_code}")


# get_weather("101010100")
