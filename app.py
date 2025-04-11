import streamlit as st
import requests
import os

# Page config
st.set_page_config(page_title="AI Code Review Assistant", layout="wide")
st.title("🧠 AI Code Review Assistant")
st.markdown("Paste your code below to get a smart code review using Mistral-7B.")

# Get Hugging Face token
HF_TOKEN = os.environ.get("HF_TOKEN")
if not HF_TOKEN:
    st.error("❌ HF_TOKEN not found. Add it in Settings → Secrets in your Hugging Face Space.")
    st.stop()

# Hugging Face Inference API
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

# Prompt template
prompt_template = """Review the following code snippet: {message}
Identify any syntax or logical errors, assess adherence to best practices, and suggest improvements."""

# User input
code_input = st.text_area("📥 Paste your Python or Java code here:", height=300)

# Analyze button
if st.button("🧪 Analyze Code"):
    if code_input.strip():
        with st.spinner("Analyzing with Mistral-7B..."):
            prompt = prompt_template.format(message=code_input)
            payload = {"inputs": prompt}

            try:
                response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
                data = response.json()
                
                if response.status_code == 200 and isinstance(data, list):
                    result = data[0]["generated_text"]
                    st.subheader("📋 Code Review Result")
                    st.code(result)
                else:
                    st.error("❌ Unexpected API response:")
                    st.json(data)

            except requests.exceptions.RequestException as e:
                st.error("❌ Request failed")
                st.text(str(e))
    else:
        st.warning("⚠️ Please paste some code before running.")
