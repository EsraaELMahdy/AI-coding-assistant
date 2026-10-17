# AI Coding Assistant

This is my Cellula NLP internship project (Project 2, week 4). It is a chat assistant built with Streamlit that can explain code and generate code.

## How it works

Every message goes through an LLM intent classifier that decides if the user wants to explain code or generate code.

**Explain**
The LLM reads the code and explains it directly. No retrieval is used here.

**Generate**
1. The question is searched in a Chroma vector store (top 3 results).
2. An LLM evaluator checks if the retrieved results are relevant to the question.
3. If they are relevant, the LLM generates the code using them as context.
4. If not, the assistant does not guess. It asks the user to provide the correct solution, then embeds it with metadata and saves it in Chroma so it can be used next time.

**Memory**
Previous questions, the generated code, and preferences such as the programming language and framework are saved in a JSON file and sent to the LLM with every message.

**Code runner**
A separate tool runs Python code and shows stdout and stderr. The LLM never runs code itself. It is not a full sandbox.

## Data

The knowledge base is the HumanEval dataset, 164 problems. Each problem is one chunk made of the question and its solution, embedded with `sentence-transformers/all-MiniLM-L6-v2`.

## Project structure

```
app.py
requirements.txt
data/
src/
  config.py
  download_data.py
  ingestion.py
  vectorstore.py
  classifier.py
  explain.py
  evaluator.py
  generate.py
  feedback.py
  memory.py
  code_runner.py
  llm.py
```

## Setup

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Create a file named `app.env` in the project root:

```
OPENROUTER_API_KEY=your_key_here
```

## Run

```
python -m src.download_data
python -c "from src.vectorstore import build_vectorstore; build_vectorstore()"
python -m streamlit run app.py
```

The first two commands only need to run once.

## Tools

Python, Streamlit, LangChain, Chroma, HuggingFace embeddings, OpenRouter.