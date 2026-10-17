import re

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from src.llm import llm

judge = llm.bind(temperature=0)

prompt = ChatPromptTemplate.from_messages([
    ("system", """You check if retrieved knowledge can help answer a coding request.
You get a user request and some retrieved coding problems with their solutions.
Answer relevant if at least one retrieved item solves the same task or a very similar one, even if the wording is different.
Answer not_relevant only if none of the retrieved items is useful for the request.
Return one word only: relevant or not_relevant."""),
    ("human", "Request:\n{question}\n\nRetrieved knowledge:\n{context}"),
])

chain = prompt | judge | StrOutputParser()


def format_context(docs):
    parts = []
    for i, doc in enumerate(docs, start=1):
        parts.append("[" + str(i) + "]\n" + doc.page_content)
    return "\n\n".join(parts)


def is_relevant(question, docs):
    output = chain.invoke({"question": question, "context": format_context(docs)})
    words = re.findall(r"[a-z_]+", output.strip().lower())
    if not words:
        return False
    return words[0] == "relevant"