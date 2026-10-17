import re

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from src import config

llm = ChatOpenAI(
    model=config.LLM_MODEL,
    base_url=config.LLM_BASE_URL,
    api_key=config.openrouter_api_key,
    temperature=0,
)

prompt = ChatPromptTemplate.from_messages([
    ("system", """You are an intent classifier for an AI coding assistant.
Classify the user's request into exactly one category:
generate - the user wants new code written, or existing code changed or fixed.
explain - the user wants existing code, its output, or a programming concept explained.
other - the request has nothing to do with programming or code.
If the message contains code, it is never other.

Examples:
Write a function that reverses a string -> generate
Create a program that adds two numbers -> generate
Fix the bug in this code -> generate
اكتبلي كود يحسب مجموع رقمين -> generate
What does this code do? -> explain
Explain recursion -> explain
اشرحلي الكود ده -> explain
What is the capital of France? -> other
Tell me a joke -> other

Return one word only: generate, explain or other."""),
    ("human", "{user_input}"),
])

chain = prompt | llm | StrOutputParser()

LABELS = ("generate", "explain", "other")

GENERATE_STARTS = (
    "write", "create", "generate", "make", "build", "implement", "code",
    "اكتب", "اعمل", "انشئ", "ابني", "اعملي", "اكتبلي",
)


def classify(user_input):
    output = chain.invoke({"user_input": user_input}).strip().lower()
    label = "explain"
    for word in re.findall(r"[a-z]+", output):
        if word in LABELS:
            label = word
            break

    text = user_input.strip().lower()
    has_code = "```" in user_input
    if label == "explain" and not has_code and text.startswith(GENERATE_STARTS):
        return "generate"
    return label
    