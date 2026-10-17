import streamlit as st
from src import classifier, code_runner, explain, feedback, generate
from src.memory import Memory

OFF_TOPIC_MESSAGE = "I can only help with programming questions: explaining code or generating code."

st.set_page_config(page_title="Coding Assistant", layout="wide")
st.title("Coding Assistant")

if "memory" not in st.session_state:
    st.session_state.memory = Memory()
if "messages" not in st.session_state:
    st.session_state.messages = []
if "pending_question" not in st.session_state:
    st.session_state.pending_question = None

memory = st.session_state.memory


def read_upload(file):
    if file is None:
        return ""
    text = file.getvalue().decode("utf-8", errors="replace")
    return "\n\nAttached file (" + file.name + "):\n```\n" + text + "\n```"


def show_result(result):
    if result["returncode"] == 0:
        st.success("Executed successfully")
    else:
        st.error("Execution failed")
    if result["stdout"]:
        st.caption("Output")
        st.code(result["stdout"], language="text")
    if result["stderr"]:
        st.caption("Errors")
        st.code(result["stderr"], language="text")


with st.sidebar:
    st.header("Upload")
    uploaded = st.file_uploader("Code file (optional)", type=["py", "txt", "md"])
    st.header("Memory")
    if memory.preferences:
        st.json(memory.preferences)
    else:
        st.caption("No preferences saved yet")
    st.caption(str(len(memory.history)) + " messages remembered")
    with st.expander("Last messages"):
        for item in memory.history[-6:]:
            st.write(item["role"] + ": " + item["content"][:150])
    if st.button("Clear memory"):
        memory.clear()
        st.session_state.messages = []
        st.session_state.pending_question = None
        st.rerun()

for i, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message.get("sources"):
            st.caption("Sources: " + ", ".join(message["sources"]))
        if message["role"] == "assistant":
            code = code_runner.extract_code(message["content"])
            if code and st.button("Run code", key="run_" + str(i)):
                show_result(code_runner.run_code(code))

pending = st.session_state.pending_question
if pending:
    st.info("Your next message will be saved as the solution for: " + pending[:100])
    if st.button("Skip"):
        st.session_state.pending_question = None
        st.rerun()

question = st.chat_input("Ask a programming question...")

if question:
    full_question = question + read_upload(uploaded)
    with st.chat_message("user"):
        st.markdown(question)

    memory.update_preferences(question)
    memory_text = memory.get_context()
    answer = None
    sources = []
    remember = True

    with st.chat_message("assistant"):
        try:
            if pending:
                feedback.save_solution(pending, full_question)
                st.session_state.pending_question = None
                answer = "Thanks, I saved your solution and I will use it for similar requests."
                st.markdown(answer)
            else:
                intent = classifier.classify(full_question)
                st.caption("Intent: " + intent)
                if intent == "other":
                    answer = OFF_TOPIC_MESSAGE
                    st.markdown(answer)
                    remember = False
                elif intent == "explain":
                    answer = st.write_stream(explain.stream_explanation(full_question, memory_text))
                else:
                    with st.spinner("Searching the knowledge base..."):
                        docs = generate.retrieve(full_question)
                    if docs is None:
                        answer = generate.NOT_FOUND_MESSAGE
                        st.markdown(answer)
                        st.session_state.pending_question = full_question
                    else:
                        answer = st.write_stream(generate.stream_code(full_question, docs, memory_text))
                        sources = [doc.metadata["task_id"] for doc in docs]
        except Exception as error:
            st.error("Something went wrong: " + str(error))

    if answer:
        if remember:
            memory.add("user", question)
            memory.add("assistant", answer)
        st.session_state.messages.append({"role": "user", "content": question})
        st.session_state.messages.append({"role": "assistant", "content": answer, "sources": sources})
        st.rerun()