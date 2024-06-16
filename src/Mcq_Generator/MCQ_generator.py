import os
import ast
import pandas as pd
import streamlit as st
from langchain import LLMChain, PromptTemplate
from langchain.chains import SequentialChain
from langchain_community.llms import Ollama


llm = Ollama(model="llama3")


TEMPLATE = """
Text:{paragraph}
generate mcq from above paragraph
You are an expert MCQ maker. Given the above text, it is your job to \
create a quiz of {count} multiple choice questions for {topic} students in {complexity} tone. 
Make sure the questions are not repeated and check all the questions to be conforming the text as well.
Make sure to format your response like RESPONSE_JSON below and use it as a guide. \
Ensure to make {count} MCQs
### RESPONSE_JSON
{response_json}
only give MCQS as json with proper format complete json data not give any starting line which is not part of mcqs not give any extra line like here are mcq
complete json data not miss any single bracket and give complete mcqs with proper choices each has 4 choices and 1 correct 
"""

quiz_prompt = PromptTemplate(
    input_variables=["count", "complexity", "topic", "response_json", "paragraph"],
    template=TEMPLATE
)

TEMPLATE1 = """
You are an expert english grammarian and writer. Given a Multiple Choice Quiz for {topic} students.\
You need to evaluate the complexity of the question and give a complete analysis of the quiz. Only use at max 50 words for complexity analysis. 
if the quiz is not at per with the cognitive and analytical abilities of the students,\
update the quiz questions which needs to be changed and change the tone such that it perfectly fits the student abilities
Quiz_MCQs:
{quiz}

Check from an expert English Writer of the above quiz:

only give short explanation of bove quiz whereter it is easy or complex and anything about that
"""

gram_prompt = PromptTemplate(
    input_variables=["quiz", "topic"],
    template=TEMPLATE1
)

quiz_chain = LLMChain(llm=llm, prompt=quiz_prompt, output_key="quiz")
gram_chain = LLMChain(llm=llm, prompt=gram_prompt, output_key="review")

final_chain = SequentialChain(
    chains=[quiz_chain, gram_chain],
    input_variables=["count", "complexity", "topic", "response_json", "paragraph"],
    output_variables=["quiz", "review"]
)
