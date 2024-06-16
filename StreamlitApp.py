import os
import ast
import pandas as pd
import streamlit as st
from langchain import LLMChain, PromptTemplate
from langchain.chains import SequentialChain
from langchain_community.llms import Ollama

# Set up the LLM chain
llm = Ollama(model="llama3")
response_json = {
    "1": {
        "mcq": "multiple choice question",
        "options": {
            "a": "choice here",
            "b": "choice here",
            "c": "choice here",
            "d": "choice here",
        },
        "correct": "correct answer",
    },
    "2": {
        "mcq": "multiple choice question",
        "options": {
            "a": "choice here",
            "b": "choice here",
            "c": "choice here",
            "d": "choice here",
        },
        "correct": "correct answer",
    },
    "3": {
        "mcq": "multiple choice question",
        "options": {
            "a": "choice here",
            "b": "choice here",
            "c": "choice here",
            "d": "choice here",
        },
        "correct": "correct answer",
    },
}

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

only give MCQS as json data with proper format complete json data not give any starting line which is not part of mcqs not give any extra line like here are mcq
complete json data not miss any single bracket and give complete mcqs with proper choices each has 4 choices and 1 correct 
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

def mcqs_to_dataframe(mcqs):
    data = []
    for q_num, mcq_data in mcqs.items():
        question = mcq_data['mcq']
        option_a = mcq_data['options']['a']
        option_b = mcq_data['options']['b']
        option_c = mcq_data['options']['c']
        option_d = mcq_data['options']['d']
        correct_answer = mcq_data['options'][mcq_data['correct']]
        data.append({
            'Question Number': q_num,
            'Question': question,
            'Option A': option_a,
            'Option B': option_b,
            'Option C': option_c,
            'Option D': option_d,
            'Correct Answer': correct_answer
        })
    return pd.DataFrame(data)

# Streamlit app
st.title("MCQ Generator")

uploaded_file = st.file_uploader("Choose a text file", type="txt")
if uploaded_file is not None:
    data = uploaded_file.read().decode("utf-8")
    st.text_area("File Content", value=data, height=300)

    count = st.number_input("Number of MCQs", min_value=1, max_value=10, value=3)
    complexity = st.selectbox("Complexity Level", ["simple", "medium", "hard"])
    topic = st.text_input("Topic", "Machine learning")

    if st.button("Generate MCQs"):
        input_data = {
            "count": str(count),
            "complexity": complexity,
            "topic": topic,
            "paragraph": data,
            "response_json": f"{response_json}"
        }
        
        try:
            result = final_chain(input_data)
            mcq_string = result.get("quiz")

            # Remove the introductory text to isolate the dictionary part
            mcq_data_str = mcq_string.split('{', 1)[1].rsplit('}', 1)[0]
            mcq_data_dict = ast.literal_eval('{' + mcq_data_str + '}')

            df = mcqs_to_dataframe(mcq_data_dict)
            st.write(df)

            # Provide download link for the CSV
            csv = df.to_csv(index=False)
            st.download_button(label="Download MCQs as CSV", data=csv, file_name="mcqs.csv", mime="text/csv")
        
        except Exception as e:
            st.error(f"An error occurred: {e}")
            st.error(traceback.format_exc())
