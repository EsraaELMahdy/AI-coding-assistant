from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from src import vectorstore, evaluator
from src.llm import llm

NOT_FOUND_MESSAGE = (
    "I couldn't find relevant knowledge for your request. "
    "Could you provide the correct solution or reference so I can learn it for future interactions?"
)

prompt = ChatPromptTemplate.from_messages([
    ("system", """You are an expert programming assistant.
Write complete, well-structured code that answers the user's request.
Use the retrieved examples as reference.
Respect the user's preferences and the conversation memory below.
Include comments, follow best practices, and handle errors.
Put the code inside Markdown code blocks and add a short explanation after the code.

Conversation memory:
{memory}"""),
    ("human", "User request:\n{question}\n\nRetrieved examples:\n{context}"),
])

chain = prompt | llm | StrOutputParser()


def retrieve(question):
    results = vectorstore.search(question)
    docs = [doc for doc, score in results]
    if evaluator.is_relevant(question, docs):
        return docs
    return None


def stream_code(question, docs, memory_text=""):
    context = evaluator.format_context(docs)
    return chain.stream({"question": question, "context": context, "memory": memory_text})