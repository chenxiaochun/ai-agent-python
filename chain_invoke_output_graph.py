from get_model import get_model
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import (
    RunnableMap,
    RunnableLambda,
    RunnableWithMessageHistory,
)

load_dotenv()

model = get_model()

prompt_template_zh = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Translate the following from English to Chinese",
        ),
        ("user", "{text}"),
    ]
)

prompt_template_fr = ChatPromptTemplate.from_messages(
    [("system", "Translate the following from English to French"), ("user", "{text}")]
)

parser = StrOutputParser()

chain_zh = prompt_template_zh | model | parser
chain_fr = prompt_template_fr | model | parser

parallel_chain = RunnableMap({"zh_translation": chain_zh, "fr_translation": chain_fr})

final_chain = parallel_chain | RunnableLambda(
    lambda x: f"Chinese: {x['zh_translation']}\n{x['fr_translation']}"
)

print(final_chain.invoke({"text": "nice to meet you"}))

final_chain.get_graph().print_ascii()
