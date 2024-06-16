import os
import ast
import pandas as pd
import streamlit as st
from src.Mcq_Generator.MCQ_generator import final_chain  # Importing the final_chain
import traceback

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
