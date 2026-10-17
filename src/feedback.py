import uuid
from datetime import datetime
from langchain_core.documents import Document
from src import vectorstore


def save_solution(question, solution):
    text = "Question:\n" + question + "\nSolution:\n" + solution
    doc_id = "user-" + uuid.uuid4().hex[:8]
    metadata = {
        "source": "user_feedback",
        "task_id": doc_id,
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }
    store = vectorstore.load_vectorstore()
    store.add_documents([Document(page_content=text, metadata=metadata)], ids=[doc_id])
    return doc_id