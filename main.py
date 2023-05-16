from typing import Set

import streamlit as st
from streamlit_chat import message
from backend.core import run_llm

st.header("🦜️Langchain Documentation ChatBot")


def sourcesListfunc(source_urls: Set[str]) -> str:
    if not source_urls:
        return ""
    source_list = list(source_urls)
    source_list.sort()
    sources_string = "sources:\n"
    for i, url in enumerate(source_list):
        sources_string += f"{i+1}.{url}\n"
    return sources_string


prompt = st.text_input("Prompt", placeholder="Enter you Prompt Here")

# Initializations
if "user_prompt_history" not in st.session_state:
    st.session_state["user_prompt_history"] = []

if "chat_answers_history" not in st.session_state:
    st.session_state["chat_answers_history"] = []


if prompt:
    with st.spinner(text="In progress"):
        response = run_llm(query=prompt)
        sources = set([doc.metadata["source"] for doc in response["source_documents"]])

        formatted_response = f"{response['result']} \n\n  {sourcesListfunc(sources)}"

        st.session_state["user_prompt_history"].append(prompt)
        st.session_state["chat_answers_history"].append(formatted_response)


if st.session_state["chat_answers_history"]:
    for user_ques, model_reply in zip(
        st.session_state["user_prompt_history"],
        st.session_state["chat_answers_history"],
    ):
        message(user_ques, is_user=True)
        message(model_reply)
