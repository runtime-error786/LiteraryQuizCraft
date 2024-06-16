import os
import ast
import json
import pandas as pd
import streamlit as st
from src.Mcq_Generator.MCQ_generator import final_chain  # Importing the final_chain
import traceback
from src.Mcq_Generator.utils import load_response_json,mcqs_to_dataframe
from src.Mcq_Generator.logger import log_task

response_json_path = 'response.json'
response_json = load_response_json(response_json_path)


# Streamlit app
st.title("Quiz MCQ Generator Using langchain")

uploaded_file = st.file_uploader("Choose a text file", type="txt")
if uploaded_file is not None:
    data = uploaded_file.read().decode("utf-8")
    st.text_area("File Content", value=data, height=300)

    count = st.number_input("Number of MCQs", min_value=1, max_value=10, value=3)
    complexity = st.selectbox("Complexity Level", ["simple", "medium", "hard"])
    topic = st.text_input("Topic", "Write Here")

    if st.button("Generate MCQs"):
        input_data = {
            "count": str(count),
            "complexity": complexity,
            "topic": topic,
            "paragraph": data,
            "response_json": json.dumps(response_json)
        }
        
        try:
            result = final_chain(input_data)
            mcq_string = result.get("quiz")

            # Remove the introductory text to isolate the dictionary part
            mcq_data_str = mcq_string.split('{', 1)[1].rsplit('}', 1)[0]
            mcq_data_dict = ast.literal_eval('{' + mcq_data_str + '}')

            df = mcqs_to_dataframe(mcq_data_dict)
            st.write(df)
            log_task("mcqs retrieve from LLM model")

            # Provide download link for the CSV
            csv = df.to_csv(index=False)
            st.download_button(label="Download MCQs as CSV", data=csv, file_name="mcqs.csv", mime="text/csv")
            log_task("User download csv file")

        
        except Exception as e:
            st.error(f"An error occurred: {e}")
            st.error(traceback.format_exc())
