import os
import re
import io
import sys
import contextlib
import warnings
from typing import Optional, Tuple, Any, List
from PIL import Image
import streamlit as st
import pandas as pd
import base64
from io import BytesIO
import google.generativeai as genai
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

warnings.filterwarnings("ignore", category=UserWarning, module="pydantic")

# Regex to extract python code blocks from LLM response
pattern = re.compile(r"```python\n(.*?)\n```", re.DOTALL)


def run_local_code(code: str, local_vars: dict) -> Optional[dict]:
    """Execute Python code locally and capture stdout/errors."""
    stdout_capture = io.StringIO()
    try:
        with contextlib.redirect_stdout(stdout_capture), contextlib.redirect_stderr(stdout_capture):
            exec(code, {}, local_vars)
    except Exception as e:
        st.error(f"⚠️ Code Execution Error: {e}")
        output = stdout_capture.getvalue()
        if output:
            st.text_area("🖨️ Partial Output / Trace", output, height=200)
        return None

    output = stdout_capture.getvalue()
    if output:
        st.text_area("🖨️ Code Output", output, height=200)
    return local_vars


def match_code_blocks(llm_response: str) -> str:
    match = pattern.search(llm_response)
    return match.group(1) if match else ""


def chat_with_llm(user_message: str, dataset_name: str) -> Tuple[Optional[str], str]:
    """Generate Python analysis code using Gemini."""
    system_prompt = f"""
You are a helpful Python data scientist and visualization expert.
You are given a dataset named '{dataset_name}' uploaded through Streamlit.
Write clean, runnable Python code that uses the DataFrame variable 'df' already loaded in memory.
Use pandas, matplotlib/seaborn, or plotly for analysis or visualization.
Wrap only the Python code in triple backticks like:
```python
# code here
```
Do not reload the CSV from disk — use 'df' directly.
Do not include long explanations — return runnable code in the code block.
"""

    messages = f"{system_prompt}\n\nUser query: {user_message}"

    with st.spinner('🤖 Asking Gemini...'):
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(messages)
        response_text = response.text if hasattr(response, 'text') else str(response)
        python_code = match_code_blocks(response_text)
        return python_code, response_text


def main():
    st.set_page_config(page_title="AI Data Visualization Agent (Gemini + Local)", layout="wide")
    st.title("📊 AI Data Visualization Agent (Gemini + Local)")
    st.write("Upload a CSV and ask questions — Gemini will generate Python code which runs locally.")

    if 'gemini_api_key' not in st.session_state:
        st.session_state.gemini_api_key = ''

    with st.sidebar:
        st.header("🔑 Gemini API Key")
        st.session_state.gemini_api_key = st.text_input("Enter your Google Gemini API Key", type="password")
        st.markdown("[Get a free Gemini API key](https://aistudio.google.com/app/apikey)")
        st.markdown("---")
        st.write("This app executes model-generated code locally. Do not use on untrusted multi-user hosts.")

    if not st.session_state.gemini_api_key:
        st.warning("Please enter your Gemini API key in the sidebar to continue.")
        st.stop()

    genai.configure(api_key=st.session_state.gemini_api_key)

    uploaded_file = st.file_uploader("📂 Choose a CSV file", type=["csv"])

    if uploaded_file is None:
        st.info("Upload a CSV file to get started. Example: titanic.csv, iris.csv, etc.")
        return

    try:
        df = pd.read_csv(uploaded_file)
    except Exception as e:
        st.error(f"Failed to read CSV: {e}")
        return

    st.subheader("📁 Dataset Preview")
    if st.checkbox("Show full dataset"):
        st.dataframe(df)
    else:
        st.dataframe(df.head())

    query = st.text_area("💬 What would you like to know about your data?",
                         value="Group by class or category and compare averages.")

    if st.button("🚀 Analyze"):
        dataset_name = uploaded_file.name

        python_code, llm_response = chat_with_llm(query, dataset_name)

        st.subheader("🤖 Gemini Response (raw)")
        st.write(llm_response)

        if not python_code:
            st.warning("Gemini did not return a Python code block. Try rephrasing the query.")
            return

        st.subheader("🧩 Generated Python Code")
        st.code(python_code, language="python")

        local_vars = {
            'pd': pd,
            'plt': plt,
            'sns': sns,
            'px': px,
            'df': df,
        }

        with st.spinner("⚙️ Running generated code locally..."):
            result_vars = run_local_code(python_code, local_vars)

        if result_vars is None:
            st.error("Execution failed. See output above for errors.")
            return

        try:
            if plt.get_fignums():
                for fig_num in plt.get_fignums():
                    fig = plt.figure(fig_num)
                    st.pyplot(fig)
                plt.close('all')
        except Exception:
            pass

        for v in result_vars.values():
            try:
                if hasattr(v, 'to_html'):
                    st.plotly_chart(v)
            except Exception:
                continue

        for name, val in result_vars.items():
            if isinstance(val, (pd.DataFrame, pd.Series)) and name != 'df':
                st.write(f"**{name}**")
                st.dataframe(val)

        st.success("✅ Analysis complete. You can modify the query or regenerate more insights.")


if __name__ == '__main__':
    main()