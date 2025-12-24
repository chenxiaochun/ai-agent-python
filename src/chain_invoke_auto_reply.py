from get_model import get_model
from langchain.agents import create_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

model = get_model()

prompt_template = ChatPromptTemplate(
    [
        ("system", "你是一名专业翻译，请将后面的文字翻译成{language}"),
        ("user", "{text}"),
    ]
)

analysis_prompt_template = ChatPromptTemplate(
    [("user", "我该怎么回答这句话？{talk}，请给我一个五个字的示例")]
)

parser = StrOutputParser()

chain = prompt_template | model | parser
chain.invoke({"text": "见你很高兴", "language": "英文"})

chain2 = {"talk": chain} | analysis_prompt_template | model | parser
resp = chain2.invoke({"text": "你是谁", "language": "英文"})

print(resp)
