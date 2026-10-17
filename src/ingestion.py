import json
from langchain_core.documents import Document
from src import config


def load_documents():
    path = config.DATA_DIR / "humaneval.json"
    with open(path, encoding="utf-8") as f:
        rows = json.load(f)

    docs = []
    for row in rows:
        text = "Question:\n" + row["prompt"] + "\nSolution:\n" + row["canonical_solution"]
        metadata = {
            "source": "humaneval",
            "task_id": row["task_id"],
            "entry_point": row["entry_point"],
        }
        docs.append(Document(page_content=text, metadata=metadata))
    return docs