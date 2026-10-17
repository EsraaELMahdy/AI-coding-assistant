from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from src.llm import llm

prompt = ChatPromptTemplate.from_messages([
    ("system", """You are an expert programming tutor.
You only help with programming: explaining code or programming concepts.
If the user's request is NOT about programming or code, do not answer it.
Reply only with: "I can only help with programming questions: explaining code or generating code."
Otherwise, explain the code or concept in the user's request clearly and accurately.
If code is provided, explain it step by step and point out any bugs.
Use Markdown and put code inside code blocks.
Use the conversation memory below to understand follow-up requests.

Conversation memory:
{memory}"""),
    ("human", "{question}"),
])

chain = prompt | llm | StrOutputParser()


def explain_code(question, memory_text=""):
    return chain.invoke({"question": question, "memory": memory_text})


def stream_explanation(question, memory_text=""):
    return chain.stream({"question": question, "memory": memory_text})