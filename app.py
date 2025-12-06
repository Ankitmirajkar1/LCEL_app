## Import necessary libraries

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough ##Pass raw input (context+ question)

import langsmith
client = langsmith.Client()
import streamlit as st

load_dotenv()


## Streamlit configurations
st.set_page_config(
    page_title = "LCEL application",
    layout = "centered"
)

st.write("""This app answers the questions strictly on the context provided""")


allowed_text = st.text_area("Paste your context here",
height = 150)

question = st.text_input("Enter your question here")

prompt = PromptTemplate.from_template("""
You must answer the questions strictly based on the context provided. You must not use any prior knowledge, assumptions, or information not contained in the context.
If the answer is not contained within the context, respond with "I don't know the answer. I can Only answer based on the context provided.
Questions:{question}

""")

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

## LCEL App Chain

chain = ({"context": RunnablePassthrough(), "question": RunnablePassthrough()} | prompt | llm | StrOutputParser())

## Execute the chain on user button click

if st.button("Submit"):
    if not allowed_text.strip():
        st.error("Please provide the context")
    elif not question.strip():
        st.error("Please provide the question")
    else:
        with st.spinner("Thinking.."):
            response = chain.invoke({"context": allowed_text, "question": question})
        
        st.subheader("Anwer")
        st.success(response)