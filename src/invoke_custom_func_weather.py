from get_weather import get_weather
from langchain_core.tools import tool
from get_model import get_model
from langchain_core.tools import StructuredTool

model = get_model()


weather_tool = StructuredTool.from_function(
    func=get_weather, description="获取某个城市的天气"
)

tool_dict = {"get_weather": weather_tool}

model_with_tools = model.bind_tools([get_weather])

messages = ["北京今天的天气怎么样啊？"]

resp = model_with_tools.invoke(messages)

for tool_calls in resp.tool_calls:
    func_args = tool_calls["args"]
    func_name = tool_calls["name"]

    tool_func = tool_dict[func_name]
    tool_content = tool_func.invoke(func_args)
    print(tool_content)
