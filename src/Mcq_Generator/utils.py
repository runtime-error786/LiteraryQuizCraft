import os
import ast
import json
import pandas as pd
import streamlit as st
from src.Mcq_Generator.MCQ_generator import final_chain  # Importing the final_chain
import traceback


# Read response_json from a file
def load_response_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)
    


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
