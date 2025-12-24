import os
from langchain_openai import ChatOpenAI
from langchain_core.tools import Tool
from dotenv import load_dotenv
from langchain_core.prompts import (
    PromptTemplate,
    ChatPromptTemplate,
    ChatMessagePromptTemplate,
    FewShotPromptTemplate,
)

load_dotenv()


def add(a, b):
    return a + b


llm = ChatOpenAI(
    model_name="qwen3-max",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    openai_api_base="https://dashscope.aliyuncs.com/compatible-mode/v1",
    streaming=True,
)

system_template_message = ChatMessagePromptTemplate.from_template(
    template="你是一位{role}专家，擅长回答{topic}领域的问题", role="system"
)

user_template_message = ChatMessagePromptTemplate.from_template(
    template="用户的问题：{question}", role="user"
)

chat_prompt_message = ChatPromptTemplate.from_messages(
    [system_template_message, user_template_message]
)

# 将函数转变为 langchain 可以理解的函数
# name 必须是全局唯一，不能重复
add_tools = Tool.from_function(func=add, name="add", description="add two numbers")

# 将大模型和 tool 对象绑定
llm_with_tools = llm.bind_tools([add_tools])

chain = chat_prompt_message | llm_with_tools
resp = chain.invoke(input={"role": "计算", "topic": "数学", "question": "100+100=?"})

tool_dict = {"add": add}

# 大模型不会自动调用自定义函数工具，需要我们自己实现调用
for tool_calls in resp.tool_calls:
    func_args = tool_calls["args"]
    func_name = tool_calls["name"]

    print(tool_calls)

    tool_func = tool_dict[func_name]
    # 教程中的第二个参数是 __arg2，但我的代码中输出的是 example_parameter_2。没搞明白是为啥
    tool_content = tool_func(
        int(func_args["__arg1"]), int(func_args["example_parameter_2"])
    )
    print(tool_content)
